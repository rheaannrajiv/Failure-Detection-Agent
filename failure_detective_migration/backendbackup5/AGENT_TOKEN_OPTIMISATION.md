# Agent token optimisation update

This update reduces avoidable Groq token use and makes provider rate limits visible to API clients.

## Changes

- Shortened the system instructions while retaining diagnostic and safety requirements.
- Reduced completion budget from 1,400 to 700 tokens for normal turns and 450 tokens for final synthesis.
- Reduced tool loop from five rounds to three, followed by a concise synthesis turn.
- Limited client-supplied history to the latest eight messages, with per-message and total character caps.
- Kept the fault catalogue tool complete (18 categories) while limiting each category to concise symptom/check labels.
- Limited diagnostic tool results to the five leading candidates.
- Converts Groq HTTP 429 responses into API HTTP 429 and returns a `Retry-After` header when the provider supplies a retry estimate.
- Converts connectivity failures into HTTP 503 rather than a generic 502.

## Important limitations

These changes reduce avoidable prompt and completion size; they do not increase Groq's free-tier quota or guarantee every request will fit within the remaining rolling TPM allowance. A request can still receive HTTP 429. The client should wait for `Retry-After` (or at least the provider's stated wait) before retrying. Do not automatically retry a 429 in a tight loop.

Conversation memory remains client-supplied in this milestone. Supabase-backed persistent memory is a later milestone. Sensor analysis remains available through `/api/sensors/analyse`; direct agent invocation of the sensor tool is not included in this update.

## Deploy

Render is configured to deploy from `failure_detective_migration/backend`. Commit and push the updated contents of that backend directory to the existing `main` branch. Render should deploy automatically. No environment variable changes are required; keep `GROQ_API_KEY` and `GROQ_MODEL` configured in Render.

## Verify

1. Open `/api/health`; expected API version is `0.3.0`.
2. Open `/docs` and call `POST /api/agent/chat`.
3. Check successful responses for `token_efficiency`.
4. If Groq is rate-limited, the API should return HTTP 429 (not 502) and may include `Retry-After`.
5. Run `python -m pytest -q` from this backend directory; the included tests should pass.
