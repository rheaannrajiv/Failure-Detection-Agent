from fastapi import APIRouter, HTTPException, UploadFile, File, Form
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

@router.post("/agent/chat", response_model=AgentChatResponse)
def agent_chat(payload: AgentChatRequest):
    try:
        return run_agent(payload.message, [item.model_dump() for item in payload.history])
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
