# Failure Detective AI

**AI-assisted mechanical fault diagnosis and investigation platform.**

Failure Detective AI helps users investigate possible mechanical faults using natural-language symptom descriptions, diagnostic rules, sensor data and a conversational AI assistant. The project is structured as a web application with a separate API backend.

## Project architecture

| Layer | Technology | Responsibility |
|---|---|---|
| Frontend | Next.js / React | Chat interface, symptom input, sensor upload, investigation history and reports |
| Backend | Python / FastAPI | API endpoints and coordination of diagnostic services |
| AI | Groq-hosted language model | Conversational interpretation and tool-assisted explanations |
| Engineering logic | Fault catalogue and diagnostic modules | Fault ranking, evidence and inspection guidance |
| Persistence | Supabase / PostgreSQL | Session and investigation data, as implemented |
| Hosting | Vercel and Render | Frontend and backend deployment |
| Source control | GitHub | Version control and deployment integration |

The repository also retains the earlier Streamlit prototype as a fallback/demo version, if that folder is present.

## Main capabilities

- Conversational mechanical troubleshooting.
- Rule-based ranking of possible mechanical faults.
- Sensor-data analysis through the backend API.
- Guest and authenticated session flows.
- Investigation memory/persistence through Supabase.
- Diagnostic report generation.
- Web deployment with a separate frontend and backend.

> **Important:** A ranked fault is a diagnostic hypothesis, not a confirmed failure. Rule-based evidence scores are heuristic rankings, not calibrated probabilities. Sensor results depend on the data, units, sampling conditions and analysis methods supplied.

## Repository structure

The exact folder layout can vary between project revisions. The migrated application is organized around:
- `frontend/` — Next.js application.
- `backend/` — FastAPI application and engineering services.
- `app.py` — earlier Streamlit prototype, where retained.
- `requirements.txt` — Python backend dependencies.
- `DEVELOPMENT_SCHEMA.md` — system architecture and development overview.
- `API_REFERENCE.md` — currently documented API surface.

Check the actual repository tree before running commands; use the relevant folder as the working directory.

## Running the backend locally

1. Install Python 3.10 or newer.
2. Open a terminal in the backend project directory.
3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Create a local `.env` file using `.env.example` as a reference. Add the required credentials locally; do not commit the real `.env` file.
6. Start the API using the entry point configured in the backend. For the previously used FastAPI entry point:

   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

7. Open `http://127.0.0.1:8000/docs` to inspect the interactive API documentation.

If the backend package or entry-point layout has changed, use the module path in the current backend source rather than assuming the example command still applies.

## Running the frontend locally

1. Open a separate terminal in the frontend application directory (the project previously used `frontend/fd_frontend/`).
2. Install JavaScript dependencies:

   ```bash
   npm install
   ```

3. Configure the public frontend variables in `.env.local` using the variable names in `.env.example`.
4. Start the development server:

   ```bash
   npm run dev
   ```

5. Open `http://localhost:3000`.

## Environment variables and secrets

The frontend may use public configuration values such as:
- `NEXT_PUBLIC_API_BASE_URL`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

The backend may require private values such as:
- `GROQ_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `GUEST_SESSION_SECRET`

Use the actual variable names referenced by the current backend code and deployment settings. Never commit real keys, tokens, service-role credentials or `.env` files. The Supabase service-role key and Groq key must remain server-side.

## Deployment

- **Frontend:** Vercel. Set the frontend root directory to the directory containing its `package.json` (previously `frontend/fd_frontend/`).
- **Backend:** Render. Configure the Python service's working directory, start command and environment variables to match the backend layout.
- Configure backend CORS to allow the deployed frontend origin.
- Keep production secrets in the hosting provider's environment-variable settings.

## API overview

The documented backend routes include health, fault catalogue, diagnosis, sensor analysis, agent chat, memory status, report generation and guest/user session creation. See [`API_REFERENCE.md`](API_REFERENCE.md). Confirm request and response schemas in the live OpenAPI page at `/docs`.

## Safety and limitations

- This is an educational/engineering decision-support prototype, not a certified industrial safety or diagnostic system.
- The fault catalogue covers only the fault categories encoded in the application.
- Rule-based rankings are heuristic and may omit faults not represented in the knowledge base.
- AI-generated explanations can be incorrect; verify findings with measurements and qualified inspection.
- Simulated or manually entered readings are not measurements from connected equipment.
- Follow site safety procedures and use qualified personnel when inspecting rotating, electrical, hot or pressurized machinery.

## Development documentation

- [`DEVELOPMENT_SCHEMA.md`](DEVELOPMENT_SCHEMA.md) — architecture, modules, workflow and development sequence.
- [`API_REFERENCE.md`](API_REFERENCE.md) — API route summary.
- [`.env.example`](.env.example) — variable-name reference only; contains no credentials.
