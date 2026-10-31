# Milestone 7 — Session security and authentication integration

## What this adds
- Signed, expiring guest-session tokens.
- Supabase access-token verification through the Supabase Auth `/user` endpoint.
- Server-side ownership checks before agent chat and sensor-assisted investigation.
- Separate session records for authenticated users and guests.
- No browser access to the service-role key; RLS remains enabled without public table policies.

## Important authentication design
Email signup, password login, password reset and logout are handled by Supabase Auth from the frontend using the Supabase publishable key. The frontend sends its short-lived Supabase access token to `POST /api/auth/user-session` as a Bearer token to create an owned diagnostic session. Guest users call `POST /api/auth/guest-session` and retain the returned `session_id` and `guest_token`.

For `POST /api/agent/chat`, send `session_id` in JSON and `X-Guest-Token` for a guest, or `Authorization: Bearer <supabase_access_token>` for an authenticated user. For `POST /api/agent/investigate-with-sensor`, send the same credentials as headers and `session_id` as a multipart field.

## Required Render environment variables
- `SUPABASE_URL` — existing value
- `SUPABASE_SERVICE_ROLE_KEY` — existing value, server only
- `SUPABASE_ANON_KEY` — Supabase publishable key (`sb_publishable_...`) or legacy anon key; server-side Auth token verification uses this as `apikey`
- `GUEST_SESSION_SECRET` — generate a random secret of at least 32 characters

Keep all keys out of GitHub and frontend code. Do not share them in chat.

## Database migration
Run `supabase_milestone7_security.sql` in Supabase SQL Editor after the existing `supabase_schema.sql`. This creates `diagnostic_sessions`. Existing pre-M7 conversations are not automatically assigned to an owner and will not be accessible through the new protected agent endpoints. Keep a database backup before applying the migration.

## Deploy
Use the same Render root directory, build command and start command. No new Python dependencies are required.

## Scope and limitations
This milestone secures agent session ownership. Signup/login UI is supplied by Supabase Auth and will be implemented in the frontend phase. It does not add a custom password store. Rate limiting should be enforced at the hosting edge/API gateway for multi-instance production; in-process counters are intentionally not presented as production-grade protection.
