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
