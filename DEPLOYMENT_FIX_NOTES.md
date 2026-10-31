# Deployment Fix Notes — 1 November 2026

## Changes in this update

1. **Vercel CORS support:** the FastAPI app now accepts HTTPS origins hosted on `*.vercel.app`, including changing Vercel preview deployment hostnames, while retaining explicitly configured `CORS_ORIGINS`.
2. **Network error clarity:** frontend API calls now show a useful message when the browser cannot reach the Render backend, instead of only showing the browser's generic `Failed to fetch`.
3. **Composer text contrast:** typed text is now light (`#F1F3F5`), the caret uses the orange accent, and placeholder text is a softer grey (`#A7ADB7`).

## Apply the update

1. Extract this ZIP and copy the updated `failure_detective_migration` folder contents into your existing repository, allowing the updated files to replace the old versions.
2. Commit and push the changes to GitHub.
3. Wait for **both** deployments:
   - Render should redeploy the backend because `backend/app/main.py` changed.
   - Vercel should redeploy the frontend because `frontend/fd_frontend` changed.
4. Open the backend health endpoint:
   `https://failure-detection-agent.onrender.com/api/health`
5. Open the Vercel site in a private/incognito tab and send a short test message.

## If the request still fails

- In Render, open the backend service's **Logs** and check whether the service starts successfully.
- In the browser, inspect the failed request in Developer Tools → Network and note its URL, status and response (do not share secrets).
- Confirm the Vercel frontend's `NEXT_PUBLIC_API_BASE_URL` is exactly:
  `https://failure-detection-agent.onrender.com`
- Keep private credentials only in Render environment variables. This ZIP deliberately excludes `.env.local`, `.env` files and Git history.

## Verification note

Python backend source compilation and the Vercel-origin regular-expression checks passed locally. A full Next.js production build could not be completed in this environment because the Next.js SWC binary needed to be downloaded from npm and network access to the npm registry was unavailable. Render and Vercel deployment success must therefore be confirmed after pushing.
