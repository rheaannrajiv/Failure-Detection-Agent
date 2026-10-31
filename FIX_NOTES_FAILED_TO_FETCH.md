# Deployment fix notes — Failed to fetch

## Changes in this package
- Backend CORS now merges the configured `CORS_ORIGINS` list with `VERCEL_FRONTEND_URL`.
- If `VERCEL_FRONTEND_URL` is not set, the backend defaults to `https://failure-detection-agent.vercel.app`.
- JSON `Content-Type` is no longer added to GET requests, avoiding an unnecessary browser preflight on the health check.
- Frontend network failures now show a useful backend/CORS diagnostic instead of only `Failed to fetch`.
- Dark composer text is forced to a readable light shade (`#F1F3F5`); placeholder text uses `#A7ADB7`.
- `.env.local`, `.next`, and `node_modules` are excluded from this ZIP.

## Render environment setting to verify
In Render → backend service → Environment, set:

`VERCEL_FRONTEND_URL=https://failure-detection-agent.vercel.app`

If your actual Vercel production URL is different, use that exact origin instead (scheme included, no trailing slash). Keep existing backend secrets unchanged. The backend also retains any origins already listed in `CORS_ORIGINS`.

After pushing the backend change, wait for Render to redeploy. Then test:
`https://failure-detection-agent.onrender.com/api/health`

## Vercel environment settings to verify
- `NEXT_PUBLIC_API_BASE_URL=https://failure-detection-agent.onrender.com`
- `NEXT_PUBLIC_SUPABASE_URL` must be your actual Supabase project URL.
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` must be the project's public anon/publishable key.

The uploaded local `.env.local` had an empty `NEXT_PUBLIC_SUPABASE_URL`. This does not explain guest chat CORS by itself, but Supabase sign-in/session features will not initialise correctly from that local configuration. Set the correct value in Vercel Environment Variables and in local `.env.local` if running locally. Do not commit `.env.local`.

## Verification performed
- Backend automated tests: 21 passed.
- CORS preflight test: HTTP 200 and the expected Access-Control-Allow-Origin for the configured Vercel origin.
- Frontend TypeScript check could not complete in this environment because `react-markdown` and `remark-gfm` were absent from the supplied `node_modules`; dependency installation timed out. Run `npm ci` and then `npm run lint` from `failure_detective_migration/frontend/fd_frontend` after downloading the package.
