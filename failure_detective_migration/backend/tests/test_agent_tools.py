from app.agent.service import _run_tool


def test_agent_can_read_fault_catalog():
    result = _run_tool("list_fault_catalog", {})
    assert len(result["faults"]) == 18
    assert any(item["name"] == "Pump Cavitation" for item in result["faults"])


def test_agent_diagnostic_tool_runs_existing_engine():
    result = _run_tool("diagnose_machine", {
        "description": "Pump has crackling noise, fluctuating flow and vibration",
        "symptoms": ["crackling pump noise", "fluctuating flow", "pump vibration"],
        "inspection_results": {},
    })
    assert result["ranked_failures"][0]["failure"] == "Pump Cavitation"
    assert "not probabilities" in result["scoring_note"]


def test_agent_rejects_unknown_symptoms():
    result = _run_tool("diagnose_machine", {"description": "test", "symptoms": ["made up symptom"]})
    assert "unknown_symptoms" in result


def test_catalog_tool_is_compact_and_complete():
    result = _run_tool("list_fault_catalog", {})
    assert len(result["faults"]) == 18
    assert all(len(item["checks"]) <= 4 for item in result["faults"])



def test_sensor_tool_requires_attached_upload():
    result = _run_tool("analyze_uploaded_sensor_data", {})
    assert "error" in result


def test_sensor_tool_returns_uploaded_analysis_compactly():
    sample = {
        "features": [{"Channel": "DE_time", "Feature": "RMS", "Assessment": "Outside healthy reference"}],
        "inferred_symptoms": ["excessive vibration"],
        "evidence_notes": ["Amplitude differs from reference."],
        "method_note": "Empirical reference comparison.",
    }
    result = _run_tool("analyze_uploaded_sensor_data", {}, sensor_analysis=sample)
    assert result["inferred_symptoms"] == ["excessive vibration"]
    assert result["features"][0]["Feature"] == "RMS"


def test_history_keeps_newest_context_when_older_message_is_oversized():
    from app.agent.service import _normalise_history

    history = [
        {"role": "user", "content": "old context " * 2500},
        {"role": "assistant", "content": "Earlier response."},
        {"role": "user", "content": "KTM 250 Duke BS4 loses power at low RPM and backfires."},
    ]
    normalised = _normalise_history(history)
    assert normalised
    assert normalised[-1]["content"] == "KTM 250 Duke BS4 loses power at low RPM and backfires."


def test_history_rejects_invalid_roles_and_keeps_chronological_order():
    from app.agent.service import _normalise_history

    result = _normalise_history([
        {"role": "user", "content": "First symptom."},
        {"role": "system", "content": "Do not include this."},
        {"role": "assistant", "content": "What changed under load?"},
        {"role": "user", "content": "Only at low RPM."},
    ])
    assert [item["role"] for item in result] == ["user", "assistant", "user"]
    assert result[-1]["content"] == "Only at low RPM."
