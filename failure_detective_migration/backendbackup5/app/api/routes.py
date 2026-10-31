from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from uuid import uuid4
from app.api.schemas import DiagnosisRequest, DiagnosisResponse, SensorAnalysisResponse
from app.diagnostics.engine import extract_symptoms_from_text, rank_failures, select_next_check, FAILURES
from app.signal_processing.service import read_sensor_bytes, load_builtin_cwru_recordings, analyse_against_healthy

router = APIRouter(prefix="/api")

@router.get("/faults")
def list_faults():
    return [{"name": name, "symptoms": details["symptoms"], "checks": details["checks"]} for name, details in FAILURES.items()]

@router.post("/diagnose", response_model=DiagnosisResponse)
def diagnose(payload: DiagnosisRequest):
    extracted = extract_symptoms_from_text(payload.description)
    used = sorted(set(extracted) | set(payload.symptoms))
    unknown = sorted(set(used) - {s for f in FAILURES.values() for s in f["symptoms"]})
    if unknown:
        raise HTTPException(status_code=422, detail={"message": "One or more supplied symptoms are not recognised labels.", "unknown_symptoms": unknown})
    ranked = rank_failures(used, payload.inspection_results)
    next_check = select_next_check(ranked, payload.inspection_results)
    return DiagnosisResponse(extracted_symptoms=extracted, symptoms_used=used, ranked_failures=ranked, next_check=next_check, scoring_note="Scores are transparent heuristic evidence scores, not probabilities or confirmed diagnoses.")

@router.post("/sensors/analyse", response_model=SensorAnalysisResponse)
async def analyse_sensor(file: UploadFile = File(...), healthy_reference: str = Form(default="cwru")):
    try:
        test = read_sensor_bytes(file.filename or "upload.csv", await file.read())
        if healthy_reference != "cwru":
            raise HTTPException(status_code=400, detail="Only the configured CWRU reference is currently supported.")
        recordings = load_builtin_cwru_recordings()
        result = analyse_against_healthy(test, recordings["healthy"])
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

# Agent endpoint is added separately to keep the existing deterministic APIs intact.
from app.api.chat_schemas import AgentChatRequest, AgentChatResponse
from app.agent.service import run_agent, GroqProviderError
from app.memory.supabase_store import memory_store, MemoryUnavailable

@router.post("/agent/chat", response_model=AgentChatResponse)
def agent_chat(payload: AgentChatRequest):
    session_id = payload.session_id or uuid4()
    try:
        supplied_history = [item.model_dump() for item in payload.history]
        history = memory_store.load_history(str(session_id)) if memory_store.enabled else supplied_history
        result = run_agent(payload.message, history)
        result["session_id"] = session_id
        if memory_store.enabled:
            memory_store.append_turn(str(session_id), payload.message, result.get("reply", ""), {"tool_calls": result.get("tool_calls", [])})
            result["memory_mode"] = "supabase_persistent_session"
        else:
            result["memory_mode"] = "client_supplied_history_fallback"
        return result
    except MemoryUnavailable as exc:
        raise HTTPException(status_code=503, detail=f"Conversation memory is temporarily unavailable: {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GroqProviderError as exc:
        headers = {"Retry-After": str(max(1, int(exc.retry_after)))} if exc.retry_after else None
        status = 429 if exc.status_code == 429 else (503 if exc.status_code >= 500 else 502)
        detail = "Groq rate limit reached. Wait before retrying; the backend has not lost your diagnostic session." if status == 429 else f"Groq provider error: {exc}"
        raise HTTPException(status_code=status, detail=detail, headers=headers) from exc
    except RuntimeError as exc:
        message = str(exc)
        status = 503 if "not configured" in message else 502
        raise HTTPException(status_code=status, detail=message) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Agent provider request failed: {exc}") from exc


@router.post("/agent/investigate-with-sensor")
async def agent_investigate_with_sensor(
    message: str = Form(..., min_length=1, max_length=12000),
    history: str = Form(default="[]"),
    session_id: str = Form(default=""),
    file: UploadFile = File(...),
):
    """Run the agent with an uploaded CSV/TXT/MAT sensor recording attached."""
    import json
    from functools import lru_cache

    try:
        conversation = json.loads(history)
        active_session = session_id.strip() or str(uuid4())
        from uuid import UUID
        active_session = str(UUID(active_session))
        if not isinstance(conversation, list):
            raise ValueError("history must be a JSON array")
        raw = await file.read()
        if len(raw) > 15 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Sensor file exceeds the 15 MB upload limit.")
        channels = read_sensor_bytes(file.filename or "upload.csv", raw)
        # Cache the selected public CWRU reference in this process to avoid
        # downloading the same reference recordings for every request.
        recordings = _cached_cwru_recordings()
        sensor_result = analyse_against_healthy(channels, recordings["healthy"])
        effective_history = memory_store.load_history(active_session) if memory_store.enabled else conversation
        result = run_agent(message, effective_history, sensor_analysis=sensor_result)
        result["session_id"] = active_session
        if memory_store.enabled:
            memory_store.append_turn(active_session, message, result.get("reply", ""), {"tool_calls": result.get("tool_calls", []), "sensor_attached": True})
            result["memory_mode"] = "supabase_persistent_session"
        else:
            result["memory_mode"] = "client_supplied_history_fallback"
        return result
    except MemoryUnavailable as exc:
        raise HTTPException(status_code=503, detail=f"Conversation memory is temporarily unavailable: {exc}") from exc
    except HTTPException:
        raise
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=422, detail="history must contain valid JSON.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GroqProviderError as exc:
        headers = {"Retry-After": str(max(1, int(exc.retry_after)))} if exc.retry_after else None
        status = 429 if exc.status_code == 429 else (503 if exc.status_code >= 500 else 502)
        detail = "Groq rate limit reached. Wait before retrying; your uploaded file was processed but the AI response was not completed." if status == 429 else f"Groq provider error: {exc}"
        raise HTTPException(status_code=status, detail=detail, headers=headers) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Sensor-assisted agent request failed: {exc}") from exc


from functools import lru_cache

@lru_cache(maxsize=1)
def _cached_cwru_recordings():
    return load_builtin_cwru_recordings()


@router.get("/memory/status")
def memory_status():
    return {"persistent_memory_configured": memory_store.enabled, "provider": "supabase" if memory_store.enabled else "client_supplied_history_fallback", "note": "No conversation content is returned by this endpoint."}
