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
- `POST /api/agent/investigate-with-sensor` — multipart endpoint that lets the agent invoke analysis of an uploaded CSV/TXT/MAT recording against the configured CWRU healthy reference.
- `GET /docs` — interactive API documentation.

## Agent behaviour and limits

The agent can inspect the supported fault catalog and invoke the deterministic diagnostic engine. It uses a bounded tool loop and client-supplied conversation history. When a sensor file is attached through `/api/agent/investigate-with-sensor`, the agent can invoke the sensor-analysis tool and use its measured features and conservative inferred symptoms in its investigation. It does not yet have Supabase persistent memory. Heuristic diagnostic scores are not probabilities or confirmed diagnoses.

Groq free-tier limits still apply. The agent limits prompt history, tool output and completion tokens to reduce usage. Provider HTTP 429 errors are surfaced as API HTTP 429 with a `Retry-After` header when available. Wait before retrying; repeated immediate requests will not increase quota.

See `AGENT_TOKEN_OPTIMISATION.md` and `DEPLOY_TO_RENDER.md` for deployment details.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```


## Sensor-assisted agent workflow

Use `POST /api/agent/investigate-with-sensor` as multipart form data:
- `message`: the user's machine description and question.
- `history`: optional JSON array of `{role, content}` conversation messages.
- `file`: CSV, TXT or MATLAB MAT sensor recording (maximum 15 MB).

The endpoint computes features against the configured CWRU healthy reference and exposes the resulting evidence to the LLM as a tool. The agent must call `analyze_uploaded_sensor_data` before claiming it inspected the file. The comparison is empirical and dataset-specific; it is not a universal threshold or standalone fault classifier. Sampling rate, units, sensor mounting and operating conditions matter when interpreting vibration measurements.
