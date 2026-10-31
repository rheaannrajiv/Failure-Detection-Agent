# Failure Detective AI Backend

FastAPI backend for agentic mechanical fault diagnosis, deterministic fault ranking, vibration/sensor analysis and optional persistent conversation memory.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Set `GROQ_API_KEY` and optionally `GROQ_MODEL` in your environment. Supabase conversation persistence is optional; see `MILESTONE_5_MEMORY_KNOWLEDGE.md` and `supabase_schema.sql`.

## Main endpoints

- `GET /api/health`
- `GET /api/faults`
- `POST /api/diagnose`
- `POST /api/sensors/analyse`
- `POST /api/agent/chat`
- `POST /api/agent/investigate-with-sensor`
- `GET /api/memory/status`

Interactive API documentation: `/docs`.

## Important diagnostic limitations

Fault scores are heuristic evidence scores, not probabilities. Sensor comparison is empirical against the configured healthy CWRU reference and is not a universal threshold or standalone fault classifier. Verify findings against machine-specific OEM documentation and safe inspection procedures.

## Render

Root directory: `failure_detective_migration/backend`
Build command: `pip install -r requirements.txt`
Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
