# Failure Detective AI — Frontend update and Vercel deployment

## What this update changes
- Renders agent Markdown using GitHub-flavoured Markdown, including real headings, lists, code blocks and responsive tables.
- Adds an **Export report** action to an active investigation. It sends the current chat transcript to the existing `POST /api/reports/generate` endpoint and downloads the returned Markdown report.
- Keeps the existing guest/auth session creation, chat, sensor upload and Supabase Auth integration.

## Update your existing GitHub project
1. Stop the local Next.js server with `Ctrl+C` if it is running.
2. Extract this package. It contains a folder named `fd_frontend`.
3. In your repository, open `failure_detective_migration/frontend/`.
4. Make a backup copy of the existing `fd_frontend` folder, then replace it with the package's updated `fd_frontend` folder. Do not replace or edit `backend/`.
5. In GitHub Desktop, review the changed files, commit as `Improve diagnostic rendering and report export`, then **Push origin**.

## Deploy directly to Vercel (no localhost required for visitors)
1. Open https://vercel.com/ and import the existing `Failure-Detection-Agent` GitHub repository.
2. Set **Root Directory** to `failure_detective_migration/frontend/fd_frontend` (use the exact path shown in your repository).
3. Framework preset: **Next.js**. Build command: `npm run build`. Install command: `npm install`. Output directory: leave the default.
4. Add these environment variables in Vercel for Production (and Preview if desired):
   - `NEXT_PUBLIC_API_BASE_URL` = `https://failure-detection-agent.onrender.com`
   - `NEXT_PUBLIC_SUPABASE_URL` = your Supabase Project URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = your Supabase **publishable** key (`sb_publishable_...`) or legacy anon key.
5. Deploy. Vercel will build from GitHub; your laptop does not need to stay on. Local `.env.local` is not needed for the hosted site.

## Connect browser security settings after Vercel deploys
1. Copy the production Vercel URL, e.g. `https://your-project.vercel.app`.
2. In Render → backend service → Environment, append that exact origin to `CORS_ORIGINS`. Preserve any existing origins such as `http://localhost:3000`; use comma-separated origins if the backend configuration expects a comma-separated value.
3. Save and wait for Render to redeploy.
4. In Supabase → Authentication → URL Configuration, set **Site URL** to the Vercel production URL and add it to **Redirect URLs**. Add the Vercel preview URL pattern only if you intend to test preview deployments.

## Production smoke test
- Open the Vercel URL in an incognito window.
- Confirm backend status changes to operational (first Render request may be slow while a free instance wakes).
- Start a guest session and send a short diagnostic question.
- Confirm headings, bullet lists and Markdown tables are rendered as formatted content.
- Upload a small supported CSV/TXT/MAT sensor file and test the sensor-investigation flow.
- Use **Export report** and confirm a `.md` report downloads.
- Test Supabase sign-up/sign-in after configuring Supabase redirect URLs.

## Important
- Never add the Supabase service-role/secret key or Groq key to Vercel `NEXT_PUBLIC_` variables or frontend source. Only the Supabase publishable/anon key belongs in the browser.
- This report export uses the existing backend report endpoint and sends the current chat as reported symptoms/findings. It is a draft assembled from conversation text, not an independently verified engineering assessment.
- The app currently stores the active session token in browser `sessionStorage`. Closing the browser tab may end that browser-side session; persistent cross-device history UI is a later feature and is not claimed by this update.
- Keep your existing Streamlit application and Render backend as fallback. Do not delete backups until the hosted website has passed the smoke tests.
