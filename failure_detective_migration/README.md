# Failure Detective AI – Migration Starter

This package starts the migration from the existing single-file Streamlit prototype to a modular public website architecture.

- `legacy/app.py`: preserved Streamlit source as a fallback.
- `backend/`: FastAPI backend with the original 18-fault ranking engine and sensor-analysis endpoint.
- `docs/`: migration notes.

## Current milestone

The backend runs locally and has passed its five automated tests. It is ready for the first cloud deployment to Render, subject to the GitHub upload and deployment steps in `backend/DEPLOY_TO_RENDER.md`.

The frontend (Next.js), database, authentication, agent orchestration, persistent memory, and expanded knowledge base are later milestones and are not represented as completed.
