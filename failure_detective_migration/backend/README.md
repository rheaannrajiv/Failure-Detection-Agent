# Failure Detective AI Backend

FastAPI backend for mechanical fault diagnosis, sensor analysis and the Groq-powered tool-using diagnostic agent.

## Local setup

Use Python 3.12 (see `.python-version`). From this directory:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Set `GROQ_API_KEY` and optionally `GROQ_MODEL` in your environment before using `/api/agent/chat`. Never commit real API keys. `.env.example` contains placeholders only.

## API endpoints

- `GET /api/health` — health/version check.
- `GET /api/faults` — supported fault catalog.
- `POST /api/diagnose` — deterministic fault ranking.
- `POST /api/sensors/analyse` — uploaded sensor CSV analysis against the configured CWRU healthy reference.
- `POST /api/agent/chat` — Groq-powered agent with bounded tool calling.
- `GET /docs` — interactive API documentation.

## Agent behaviour and limits

The agent can inspect the supported fault catalog and invoke the deterministic diagnostic engine. It uses a bounded tool loop and client-supplied conversation history. It does not yet have Supabase persistent memory or direct sensor-analysis tool invocation. Heuristic diagnostic scores are not probabilities or confirmed diagnoses.

Groq free-tier limits still apply. The agent limits prompt history, tool output and completion tokens to reduce usage. Provider HTTP 429 errors are surfaced as API HTTP 429 with a `Retry-After` header when available. Wait before retrying; repeated immediate requests will not increase quota.

See `AGENT_TOKEN_OPTIMISATION.md` and `DEPLOY_TO_RENDER.md` for deployment details.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```
