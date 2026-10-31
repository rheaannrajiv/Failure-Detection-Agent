# Failure Detective AI – Backend (Milestone 1)

This FastAPI service extracts the existing mechanical fault ranking and sensor-analysis helpers from the Streamlit application. The original Streamlit application is preserved in `../legacy/app.py` as a fallback.

## Run locally

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

## Endpoints

- `GET /api/health`
- `GET /api/faults`
- `POST /api/diagnose`
- `POST /api/sensors/analyse` (multipart upload; currently compares against the configured CWRU healthy reference)

## Important engineering limitations

- The 18-fault catalog and heuristic weights are preserved from the legacy prototype.
- Scores are evidence scores, not calibrated probabilities.
- Sensor comparison is empirical and is not a universal threshold or standalone fault classifier.
- The CWRU reference represents a specific laboratory bearing setup; arbitrary machinery signals may not be comparable.
- No LLM agent, persistent memory, authentication, or production database is implemented in this milestone.

## Tests

```bash
pytest -q
```

Set `CORS_ORIGINS` to the exact frontend origin(s) at deployment. Store secrets in the hosting provider's secret manager.
