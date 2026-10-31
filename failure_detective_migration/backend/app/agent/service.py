"""Token-conscious Groq tool-using mechanical diagnostic agent.

The client supplies short conversation history in this milestone. Persistent
server-side memory is intentionally deferred to the Supabase milestone.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

import requests

from app.diagnostics.engine import FAILURES, extract_symptoms_from_text, rank_failures, select_next_check

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MAX_TOOL_ROUNDS = 3
MAX_COMPLETION_TOKENS = 700
MAX_HISTORY_MESSAGES = 8
MAX_HISTORY_CHARS = 9000
MAX_TOOL_RESULT_CHARS = 5000

SYSTEM_PROMPT = """You are Failure Detective AI, a mechanical fault-investigation agent.
Investigate systematically. Understand the machine, symptoms, operating context and measurements.
Use diagnose_machine when enough symptom information exists; use list_fault_catalog only when you need
supported symptom/check labels. Interpret tool results, then ask focused follow-up questions or give
ranked hypotheses and practical next checks. Never invent measurements, inspections, sources or certainty.

The 18-category engine produces heuristic evidence scores, NOT probabilities or confirmed diagnoses.
Separate observed evidence, plausible inference and unknowns. Explain what evidence would distinguish
leading candidates. For severe vibration, overheating, smoke, leakage, abnormal pressure or cracking,
advise site safety procedures and qualified personnel. Never suggest bypassing guards/interlocks or
inspecting running machinery unsafely. Be concise and technically grounded."""

TOOLS = [
    {"type": "function", "function": {
        "name": "list_fault_catalog",
        "description": "Get the supported fault category names and concise symptom/check labels.",
        "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
    }},
    {"type": "function", "function": {
        "name": "diagnose_machine",
        "description": "Run the deterministic 18-category fault-ranking engine using machine description, symptom labels and inspection findings.",
        "parameters": {"type": "object", "properties": {
            "description": {"type": "string", "description": "Machine and fault description."},
            "symptoms": {"type": "array", "items": {"type": "string"}, "description": "Recognised symptom labels from the catalog."},
            "inspection_results": {"type": "object", "additionalProperties": {"type": "string"}, "description": "Inspection names mapped to Finding observed, Finding not observed, or Inconclusive."},
        }, "required": ["description"], "additionalProperties": False},
    }},
]


class GroqProviderError(RuntimeError):
    def __init__(self, status_code: int, detail: str, retry_after: float | None = None):
        super().__init__(detail)
        self.status_code = status_code
        self.retry_after = retry_after


def _retry_after(response: requests.Response, detail: str) -> float | None:
    header = response.headers.get("Retry-After")
    if header:
        try:
            return max(1.0, float(header))
        except ValueError:
            pass
    match = re.search(r"try again in ([0-9.]+)s", detail, re.IGNORECASE)
    return max(1.0, float(match.group(1))) if match else None


def _post_groq(payload: dict[str, Any], api_key: str) -> dict[str, Any]:
    try:
        response = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=45,
        )
    except requests.RequestException as exc:
        raise GroqProviderError(503, f"Could not reach Groq: {exc}") from exc
    if response.status_code >= 400:
        detail = response.text[:1200]
        raise GroqProviderError(response.status_code, detail, _retry_after(response, detail))
    try:
        return response.json()
    except ValueError as exc:
        raise GroqProviderError(502, "Groq returned an invalid JSON response.") from exc


def _run_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "list_fault_catalog":
        # Keep tool output small: return names and concise labels, not the full catalog prose.
        return {"faults": [
            {"name": fault, "symptoms": data["symptoms"][:5], "checks": data["checks"][:4]}
            for fault, data in FAILURES.items()
        ]}
    if name == "diagnose_machine":
        description = str(arguments.get("description", ""))[:4000]
        symptoms = arguments.get("symptoms") or []
        if not isinstance(symptoms, list) or not all(isinstance(s, str) for s in symptoms):
            return {"error": "symptoms must be a list of strings"}
        extracted = extract_symptoms_from_text(description)
        all_symptoms = sorted(set(extracted) | set(symptoms))
        valid = {s for fault in FAILURES.values() for s in fault["symptoms"]}
        unknown = sorted(set(all_symptoms) - valid)
        if unknown:
            return {"error": "Unrecognised symptom labels; use labels from list_fault_catalog.", "unknown_symptoms": unknown, "extracted_symptoms": extracted}
        inspections = arguments.get("inspection_results") or {}
        allowed = {"Finding observed", "Finding not observed", "Inconclusive"}
        if not isinstance(inspections, dict) or any(v not in allowed for v in inspections.values()):
            return {"error": "inspection_results values must be Finding observed, Finding not observed, or Inconclusive."}
        ranked = rank_failures(all_symptoms, inspections)
        return {
            "extracted_symptoms": extracted,
            "symptoms_used": all_symptoms,
            "ranked_failures": ranked[:5],
            "next_check": select_next_check(ranked, inspections),
            "scoring_note": "Heuristic evidence scores, not probabilities or confirmed diagnoses.",
        }
    return {"error": f"Tool not found: {name}"}


def _normalise_history(history: list[dict[str, str]] | None) -> list[dict[str, str]]:
    safe: list[dict[str, str]] = []
    used_chars = 0
    for item in (history or [])[-MAX_HISTORY_MESSAGES:]:
        role, content = item.get("role"), item.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str):
            continue
        content = content[:2500]
        if used_chars + len(content) > MAX_HISTORY_CHARS:
            break
        safe.append({"role": role, "content": content})
        used_chars += len(content)
    return safe


def run_agent(message: str, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured on the backend.")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
    if not message.strip():
        raise ValueError("Message cannot be empty.")

    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(_normalise_history(history))
    messages.append({"role": "user", "content": message[:4000]})
    tool_log: list[dict[str, Any]] = []
    base_payload = {"model": model, "temperature": 0.2, "max_tokens": MAX_COMPLETION_TOKENS}

    for _ in range(MAX_TOOL_ROUNDS + 1):
        payload = {**base_payload, "messages": messages, "tools": TOOLS, "tool_choice": "auto"}
        data = _post_groq(payload, api_key)
        choice = data["choices"][0]["message"]
        messages.append(choice)
        calls = choice.get("tool_calls") or []
        if not calls:
            return {
                "reply": choice.get("content") or "I couldn't produce a response. Please rephrase the problem.",
                "model": model,
                "tool_calls": tool_log,
                "agent_type": "groq_tool_using_diagnostic_agent",
                "memory_mode": "client_supplied_conversation_history",
                "token_efficiency": {"max_completion_tokens": MAX_COMPLETION_TOKENS, "history_messages_used": len(_normalise_history(history))},
            }
        for call in calls:
            fn = call.get("function", {})
            name = fn.get("name", "")
            try:
                args = json.loads(fn.get("arguments") or "{}")
                result = _run_tool(name, args)
            except Exception as exc:
                result = {"error": str(exc)}
            tool_log.append({"tool": name, "result": result})
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": json.dumps(result, ensure_ascii=False)[:MAX_TOOL_RESULT_CHARS]})

    # Final concise synthesis without tools after the bounded tool loop.
    final_messages = messages + [{"role": "system", "content": "Summarise the evidence collected in at most 5 concise bullets. State uncertainty and one best next check. Do not call tools."}]
    final_data = _post_groq({**base_payload, "max_tokens": 450, "messages": final_messages}, api_key)
    return {
        "reply": final_data["choices"][0]["message"].get("content", ""),
        "model": model,
        "tool_calls": tool_log,
        "agent_type": "groq_tool_using_diagnostic_agent",
        "memory_mode": "client_supplied_conversation_history",
        "tool_limit_reached": True,
        "token_efficiency": {"max_completion_tokens": MAX_COMPLETION_TOKENS, "history_messages_used": len(_normalise_history(history))},
    }
