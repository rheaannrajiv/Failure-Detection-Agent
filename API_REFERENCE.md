# API Reference — Failure Detective AI

**Base URL (deployed backend):** `https://failure-detection-agent.onrender.com`

The routes below reflect the API surface observed during project development. For exact request bodies, response models, authentication requirements and current availability, consult the deployed FastAPI OpenAPI interface:

`https://failure-detection-agent.onrender.com/docs`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Backend health/status |
| GET | `/api/faults` | Available fault catalogue |
| POST | `/api/diagnose` | Rule-based mechanical fault diagnosis |
| POST | `/api/sensors/analyse` | Sensor-data analysis |
| POST | `/api/agent/chat` | Conversational AI interaction |
| POST | `/api/agent/investigate-with-sensor` | Agent investigation using sensor input |
| GET | `/api/memory/status` | Memory-service status |
| POST | `/api/reports/generate` | Diagnostic report generation |
| POST | `/api/auth/guest-session` | Guest session creation |
| POST | `/api/auth/user-session` | User session creation |

## Example health check

```bash
curl https://failure-detection-agent.onrender.com/api/health
```

## Notes

- This file intentionally does not invent request or response schemas.
- Use `/docs` to inspect the live schema and test endpoints.
- Do not send private API keys or service-role credentials from the browser.
- Treat diagnostic rankings as decision-support evidence, not confirmed faults.
