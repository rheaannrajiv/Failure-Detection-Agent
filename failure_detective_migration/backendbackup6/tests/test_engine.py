import numpy as np
from app.diagnostics.engine import FAILURES, extract_symptoms_from_text, rank_failures, select_next_check
from app.signal_processing.service import analyse_against_healthy


def test_legacy_fault_catalog_preserved():
    assert len(FAILURES) == 18


def test_symptom_extraction():
    found = extract_symptoms_from_text("The pump has loud noise and reduced flow rate")
    assert "abnormal noise" in found
    assert "low flow rate" in found


def test_ranking_and_next_check():
    ranked = rank_failures(["low flow rate", "crackling pump noise"], {})
    assert ranked[0]["failure"] == "Pump Cavitation"
    assert select_next_check(ranked, {}) is not None


def test_sensor_analysis_returns_generic_symptom_only():
    rng = np.random.default_rng(4)
    healthy = {"DE_time": rng.normal(0, 0.1, 8192)}
    test = {"DE_time": rng.normal(0, 1.0, 8192)}
    result = analyse_against_healthy(test, healthy)
    assert "excessive vibration" in result["inferred_symptoms"]
    assert "not a universal machine threshold" in result["method_note"]


def test_api_health_and_diagnosis():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    health = client.get('/api/health')
    assert health.status_code == 200
    assert health.json()['status'] == 'ok'
    response = client.post('/api/diagnose', json={
        'description': 'The pump makes a crackling noise and has reduced flow rate',
        'symptoms': [],
        'inspection_results': {}
    })
    assert response.status_code == 200
    body = response.json()
    assert 'Pump Cavitation' in [item['failure'] for item in body['ranked_failures']]
    assert body['scoring_note'].startswith('Scores are transparent heuristic')
