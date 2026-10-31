# Milestone 5 — Persistent conversation memory and engineering knowledge

This update adds two capabilities while keeping Supabase optional:

- A curated mechanical engineering knowledge library for cavitation, shaft misalignment, bearing damage, rotor imbalance, mechanical looseness and lubrication failure.
- A `search_mechanical_knowledge` tool the Groq agent can call during investigations.
- Optional server-side conversation persistence using Supabase PostgREST.
- Session IDs returned by `/api/agent/chat` and accepted on follow-up requests.
- The sensor-assisted endpoint accepts an optional `session_id` form field and persists the turn when configured.
- `GET /api/memory/status` reports whether Supabase persistence is configured without exposing secrets or conversation content.
- Without Supabase credentials, the API retains client-supplied history behaviour.

## Enable Supabase persistence

1. Create a Supabase project (Free plan is sufficient for initial testing).
2. Open SQL Editor and run `supabase_schema.sql` from this backend folder.
3. In Supabase project settings, copy the Project URL and the `service_role` secret key.
4. In Render > your service > Environment, add:
   - `SUPABASE_URL` = your Supabase Project URL
   - `SUPABASE_SERVICE_ROLE_KEY` = your service_role secret key
5. Save changes and allow Render to redeploy.
6. Check `/api/memory/status`; it should report `persistent_memory_configured: true`.

Security:
- Never put the service_role key in frontend code, GitHub, or a committed `.env` file.
- The SQL enables RLS and intentionally defines no anon/authenticated policies. The backend uses the service role key server-side.
- Session IDs are UUIDs, but this milestone does not yet implement user authentication or per-user ownership/authorization. Do not treat session IDs as a substitute for accounts or confidential multi-tenant access. Authentication and ownership enforcement are part of the next security milestone before sensitive production use.

## Conversation API

`POST /api/agent/chat` accepts `message`, optional `history`, and optional `session_id`.
- First request: omit `session_id`; response returns a generated UUID.
- Follow-up: send that returned `session_id`; when Supabase is configured, the backend loads recent turns and stores the new user/assistant turn.
- When Supabase is not configured, the backend uses the supplied `history` array as before.

The knowledge library is curated starter material, not a complete engineering handbook. Machine-specific OEM manuals, operating limits, standards and qualified inspection remain authoritative.
