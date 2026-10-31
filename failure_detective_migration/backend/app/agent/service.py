"""Groq-powered tool-using mechanical diagnostic agent.

Conversation history is supplied by the client for this first agent milestone;
server-side persistent memory is intentionally deferred to the Supabase milestone.
"""
from __future__ import annotations

import json
import os
from typing import Any

import requests

from app.diagnostics.engine import FAILURES, extract_symptoms_from_text, rank_failures, select_next_check

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MAX_TOOL_ROUNDS = 5

SYSTEM_PROMPT = """You are Failure Detective AI, an engineering-focused mechanical fault investigation agent.
You must investigate systematically, not merely chat. Understand the machine, operating context,
symptoms, recent changes and available measurements. Use diagnostic tools when they can add evidence.
You may call tools iteratively, inspect their results, and call another tool if useful. Ask concise,
targeted follow-up questions when important information is missing. Never invent measurements,
inspection results, tool outputs, sources, or certainty.

The built-in diagnostic engine covers 18 fault categories. Its scores are heuristic evidence scores,
NOT probabilities. Explain that candidate rankings are preliminary. Do not state a definitive root
cause without sufficient evidence. Distinguish observed evidence, inferred possibilities and unknowns.
For safety-critical symptoms (severe vibration, overheating, smoke, leakage, abnormal pressure,
structural cracking), advise following site procedures and qualified personnel; do not recommend
bypassing guards/interlocks or inspecting running machinery unsafely.

When useful, use list_fault_catalog to inspect available categories and diagnose_machine to rank
faults. For each investigation, tell the user what evidence would discriminate between leading
candidates. Keep responses clear, technically grounded and appropriately cautious."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_fault_catalog",
            "description": "Retrieve the supported mechanical fault categories, symptoms and recommended checks.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "diagnose_machine",
            "description": "Run the deterministic 18-category fault-ranking engine using a problem description, recognised symptoms and recorded inspection outcomes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Machine and fault description."},
                    "symptoms": {"type": "array", "items": {"type": "string"}, "description": "Recognised symptom labels from the fault catalog."},
                    "inspection_results": {"type": "object", "additionalProperties": {"type": "string"}, "description": "Inspection names mapped to Finding observed, Finding not observed, or Inconclusive."},
                },
                "required": ["description"],
                "additionalProperties": False,
            },
        },
    },
]


def _run_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "list_fault_catalog":
        return {
            "faults": [
                {"name": fault, "symptoms": data["symptoms"], "checks": data["checks"]}
                for fault, data in FAILURES.items()
            ]
        }
    if name == "diagnose_machine":
        description = str(arguments.get("description", ""))[:10000]
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
            "ranked_failures": ranked[:8],
            "next_check": select_next_check(ranked, inspections),
            "scoring_note": "Heuristic evidence scores, not probabilities or confirmed diagnoses.",
        }
    return {"error": f"Tool not found: {name}"}


def run_agent(message: str, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured on the backend.")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
    if not message.strip():
        raise ValueError("Message cannot be empty.")

    safe_history = []
    for item in (history or [])[-20:]:
        role, content = item.get("role"), item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str):
            safe_history.append({"role": role, "content": content[:12000]})

    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(safe_history)
    messages.append({"role": "user", "content": message[:12000]})
    tool_log: list[dict[str, Any]] = []

    for _ in range(MAX_TOOL_ROUNDS + 1):
        response = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "tools": TOOLS, "tool_choice": "auto", "temperature": 0.2, "max_tokens": 1400},
            timeout=60,
        )
        if response.status_code >= 400:
            detail = response.text[:1000]
            raise RuntimeError(f"Groq API returned HTTP {response.status_code}: {detail}")
        data = response.json()
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
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": json.dumps(result, ensure_ascii=False)[:12000]})

    # One final model turn after exhausting tool rounds, without additional tools.
    response = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages + [{"role": "system", "content": "Tool-call limit reached. Summarise only the evidence collected, state uncertainty and give the most useful next step."}], "temperature": 0.2, "max_tokens": 1400},
        timeout=60,
    )
    response.raise_for_status()
    return {"reply": response.json()["choices"][0]["message"].get("content", ""), "model": model, "tool_calls": tool_log, "agent_type": "groq_tool_using_diagnostic_agent", "memory_mode": "client_supplied_conversation_history", "tool_limit_reached": True}
