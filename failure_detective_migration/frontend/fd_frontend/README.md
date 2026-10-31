# Failure Detective AI — Next.js frontend

A dark industrial diagnostic workspace for the Failure Detective AI FastAPI backend.

## Requirements
- Node.js LTS (Node 20 or newer recommended)
- npm

## Environment
Create `.env.local` from `.env.example` and set:

```env
NEXT_PUBLIC_API_BASE_URL=https://failure-detection-agent.onrender.com
NEXT_PUBLIC_SUPABASE_URL=YOUR_SUPABASE_PROJECT_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_SUPABASE_PUBLISHABLE_OR_ANON_KEY
```

Do not place service-role or Groq secrets in frontend variables.

## Run locally (optional)
```bash
npm install
npm run dev
```
Open http://localhost:3000.

## Deploy publicly
Push this folder to GitHub and import the repository in Vercel. Set the Vercel Root Directory to the path of this folder in the repository (currently expected: `failure_detective_migration/frontend/fd_frontend`). Use the Next.js preset and add the three environment variables above. Then add the Vercel origin to Render `CORS_ORIGINS` and Supabase Auth URL Configuration. See `DEPLOYMENT_CHECKLIST.md`.

Visitors use the Vercel-hosted site; they do not need Node.js, localhost, or your computer to be running.
