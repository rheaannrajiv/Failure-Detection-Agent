# Failure Detective AI — Development Schema

## 1. Purpose

Failure Detective AI is a web-based mechanical fault investigation platform. It combines a conversational AI interface with mechanical fault knowledge, rule-based diagnostic logic and sensor-analysis services.

## 2. System architecture

```text
              User / Maintenance Engineer
                         |
                         v
              Next.js / React Frontend
                 (Vercel deployment)
                         |
                    HTTPS / API
                         |
                         v
                 FastAPI Backend
                 (Render deployment)
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
     AI Chat Layer   Fault Diagnosis  Sensor Analysis
      (Groq API)     and Knowledge     and Features
          |              |              |
          +--------------+--------------+
                         |
                         v
               Supabase / PostgreSQL
             Session and investigation data
                         |
                         v
               Findings and Reports
                         |
                         v
                  Frontend Display
```

## 3. Main modules

| Module | Responsibility |
|---|---|
| Frontend | Chat, symptom entry, sensor upload, history and report interface |
| Authentication | Guest and user session flows |
| AI assistant | Interprets symptoms, asks clarifying questions and explains results |
| Fault knowledge base | Stores predefined fault categories, symptoms and inspection guidance |
| Diagnostic engine | Applies rules and ranks candidate faults using heuristic evidence |
| Sensor analysis | Processes supported sensor data and returns analysis results |
| Memory/persistence | Stores relevant session and investigation data through Supabase |
| Report generation | Produces a structured investigation report |

## 4. Investigation workflow

1. User describes the equipment, symptoms and operating conditions.
2. The backend receives the request and identifies available context.
3. The AI layer interprets the problem and may request missing information.
4. Diagnostic and/or sensor-analysis tools are used when their inputs are available.
5. The system presents candidate faults, evidence and inspection recommendations.
6. Investigation context may be saved and used to generate a report.

**Implementation status note:** This is the intended tool-assisted investigation workflow. Do not describe the system as fully autonomous until end-to-end testing verifies repeated tool selection, result evaluation and continuation of an investigation.

## 5. Backend API surface

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Service health check |
| GET | `/api/faults` | Retrieve fault catalogue |
| POST | `/api/diagnose` | Run rule-based diagnosis |
| POST | `/api/sensors/analyse` | Analyse sensor data |
| POST | `/api/agent/chat` | Conversational AI interaction |
| POST | `/api/agent/investigate-with-sensor` | Agent interaction with sensor input |
| GET | `/api/memory/status` | Check memory-service status |
| POST | `/api/reports/generate` | Generate an investigation report |
| POST | `/api/auth/guest-session` | Create a guest session |
| POST | `/api/auth/user-session` | Establish a user session |

Route names are based on the API surface previously observed during development. The deployed OpenAPI documentation (`/docs`) is the source of truth for current request/response schemas.

## 6. Development sequence

1. Build the mechanical fault catalogue and rule-based diagnostic engine.
2. Expose diagnosis and fault retrieval through FastAPI.
3. Integrate the hosted language model and engineering tools.
4. Implement sensor-data ingestion and analysis.
5. Connect Supabase for persistence.
6. Add guest and authenticated session flows.
7. Generate structured diagnostic reports.
8. Deploy frontend and backend.
9. Validate integration, security, diagnostic consistency and responsive behaviour.

## 7. Testing priorities

- API status codes, input validation and error handling.
- Diagnostic ranking consistency for representative fault cases.
- Sensor format, unit, sampling and missing-data validation.
- Accuracy of AI explanations and tool-result reporting.
- Session isolation and data-access permissions.
- Report completeness and traceability.
- Frontend/backend connectivity and mobile responsiveness.

## 8. Limitations and future work

Diagnostic scores are heuristic rankings, not probabilities. Results depend on the implemented fault catalogue, rules and quality of user-supplied data. Future work includes validating a complete multi-step agent loop, expanding the knowledge base with engineering references, improving sensor-processing methods, calibrating confidence, strengthening access controls and adding automated regression tests.
