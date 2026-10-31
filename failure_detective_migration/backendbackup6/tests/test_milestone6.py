from app.knowledge.library import search_knowledge
from app.agent.service import _run_tool
from app.api.report_schemas import DiagnosticReportRequest

def test_expanded_knowledge_finds_gear_wear():
    results = search_knowledge("gear tooth pitting backlash", limit=3)
    assert results and results[0]["topic"] == "gear wear"

def test_expanded_knowledge_finds_structural_resonance():
    results = search_knowledge("structural resonance natural frequency", limit=3)
    assert results and results[0]["topic"] == "structural resonance"

def test_rotational_frequency_calculation():
    result = _run_tool("calculate_rotational_frequency", {"rpm": 1450})
    assert result["rotational_frequency_hz"] == 24.16667
    assert result["running_speed_components_hz"]["2x"] == 48.33333

def test_rotational_frequency_rejects_invalid_speed():
    assert "error" in _run_tool("calculate_rotational_frequency", {"rpm": 0})

def test_report_schema_accepts_investigation_data():
    report = DiagnosticReportRequest(machine="Centrifugal pump", symptoms=["vibration"], recommended_actions=["Check alignment"])
    assert report.machine == "Centrifugal pump"
