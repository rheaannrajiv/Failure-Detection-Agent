# Milestone 6 — Expanded engineering intelligence and diagnostic reports

This update builds on Milestone 5. It adds curated knowledge topics, a deterministic shaft-speed frequency calculator available to the Groq tool loop, and a Markdown diagnostic report endpoint.

## New API

`POST /api/reports/generate` accepts machine, operating_conditions, symptoms, findings, ranked_faults, sensor_findings, recommended_actions and limitations. It returns a Markdown report generated from the submitted facts. It does not independently verify them or assert a confirmed root cause.

## New agent tool

`calculate_rotational_frequency` converts RPM to Hz and returns 1x/2x/3x running-speed components. These frequencies are not diagnostic by themselves.

## Knowledge expansion

Added curated retrieval entries for gear wear, belt-drive problems, seal failure, compressor surge, thermal expansion constraint, fatigue cracking, corrosion damage, motor electrical faults, hydraulic restriction and structural resonance.

## Important scope note

This milestone does not yet implement user authentication or per-user ownership of stored conversations. The existing Supabase session store is service-role-only and uses possession of a UUID session ID; it must not be treated as authenticated user isolation. Authentication, user ownership, RLS policy design and migration of existing session records remain a separate security-critical implementation before public multi-user launch.

## Deploy

Keep `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `GROQ_API_KEY`, and `GROQ_MODEL` configured in Render. Replace the backend folder, commit and push. Render should redeploy.
