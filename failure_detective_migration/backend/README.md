# Failure Detective AI – Backend (Milestone 2 – Agent foundation)

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
- `POST /api/agent/chat` (Groq-powered tool-calling agent; pass recent conversation history in each request)
- `GET /api/faults`
- `POST /api/diagnose`
- `POST /api/sensors/analyse` (multipart upload; currently compares against the configured CWRU healthy reference)

## Important engineering limitations

- The 18-fault catalog and heuristic weights are preserved from the legacy prototype.
- Scores are evidence scores, not calibrated probabilities.
- Sensor comparison is empirical and is not a universal threshold or standalone fault classifier.
- The CWRU reference represents a specific laboratory bearing setup; arbitrary machinery signals may not be comparable.
- The Groq-powered agent can call the deterministic fault catalog and diagnosis engine. Conversation context is currently client-supplied and is not persisted by the backend. Supabase-backed persistent memory and authentication are later milestones. Configure `GROQ_API_KEY` and optionally `GROQ_MODEL` as Render environment variables. The default model is `openai/gpt-oss-20b`.

## Tests

```bash
pytest -q
```

Set `CORS_ORIGINS` to the exact frontend origin(s) at deployment. Store secrets in the hosting provider's secret manager.
