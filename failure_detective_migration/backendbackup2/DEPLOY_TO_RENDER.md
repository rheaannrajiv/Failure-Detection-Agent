# Deploy the Failure Detective AI API to Render

This deploys the **FastAPI backend only**. It does not replace or modify the existing Streamlit app. Keep the Streamlit deployment as your fallback.

## 1. Put the migration folder in GitHub

1. Open your existing GitHub repository: `https://github.com/rheaannrajiv/Failure-Detection-Agent`.
2. Upload the complete `failure_detective_migration` folder from this package into the repository root. Keep the existing root-level Streamlit files; do not delete or overwrite them.
3. Confirm that GitHub shows this path:
   `failure_detective_migration/backend/app/main.py`
4. Commit the upload to your repository's main branch.

If you already uploaded this folder, do not upload a second copy. Just check that the path above exists and that the latest backend files are committed.

## 2. Create the Render web service

1. Sign in at https://render.com/ using GitHub.
2. Choose **New** → **Web Service**.
3. Connect `rheaannrajiv/Failure-Detection-Agent`.
4. Use these settings:

   - **Name:** `failure-detective-api` (or another available name)
   - **Branch:** `main` (or the branch where you committed the folder)
   - **Root Directory:** `failure_detective_migration/backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free (for the first deployment)

5. Click **Create Web Service** and wait for the first build to finish.

The `.python-version` file asks Render to use Python 3.12.10. The runtime requirements intentionally use standard Uvicorn rather than `uvicorn[standard]` to avoid unnecessary optional build dependencies.

## 3. Test the deployed API

Render will assign a public URL similar to `https://failure-detective-api-xxxx.onrender.com`.

Open these URLs, replacing the example host with your actual Render URL:

- `https://YOUR-RENDER-URL.onrender.com/api/health`
- `https://YOUR-RENDER-URL.onrender.com/docs`

The health endpoint should return JSON with `"status": "ok"`. In `/docs`, open `POST /api/diagnose`, click **Try it out**, and use:

```json
{
  "description": "An industrial centrifugal pump is producing intermittent crackling noise and noticeable vibration. The discharge flow is fluctuating.",
  "symptoms": [
    "crackling pump noise",
    "fluctuating flow",
    "pump vibration"
  ],
  "inspection_results": {}
}
```

A successful response should show HTTP 200 and a ranked fault list.

## 4. Environment variables

No API key is required for this first backend milestone. Do not add or paste your Groq key yet: the current FastAPI milestone does not call Groq. When the hosted AI agent is implemented, add `GROQ_API_KEY` through Render's **Environment** page as a secret. Never commit a real key to GitHub or put it in frontend code.

`CORS_ORIGINS` is currently set in the app to allow `http://localhost:3000`. When the Next.js website is deployed, update this Render environment variable to the exact public frontend origin. Multiple origins can be comma-separated.

## 5. Free-tier behaviour and limitations

- A free Render service can spin down after inactivity. The first request after a quiet period may take around a minute to wake up.
- The free service's local filesystem is ephemeral. Do not use it for permanent user accounts, conversation memory, or uploaded-file storage.
- This milestone has no database, login, persistent memory, or LLM agent yet. Those are separate implementation steps.
- Keep the Streamlit app online until the Render health check and diagnosis test both work.

## Troubleshooting

- **Build fails:** open Render's deploy log and check that Root Directory is exactly `failure_detective_migration/backend` and that the folder was committed to GitHub.
- **Module not found:** check that `app/main.py` is inside the selected root directory in GitHub.
- **Service starts but URL fails:** check the deploy log for `Application startup complete`; confirm the start command includes `$PORT` and `--host 0.0.0.0`.
- **Health works but diagnosis fails:** open `/docs`, copy the JSON example above, and share the HTTP status and error text (not any secret keys).
