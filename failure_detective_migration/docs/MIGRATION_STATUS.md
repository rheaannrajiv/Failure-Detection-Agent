# Migration status – Milestone 1

## Completed in this starter
- Preserved the legacy Streamlit source unchanged under `legacy/app.py`.
- Extracted the original 18-fault catalog, symptom extraction, ranking rules and inspection-selection logic.
- Extracted vibration feature, baseline and assessment helpers.
- Added FastAPI health, fault catalog, diagnosis and sensor upload endpoints.
- Added basic automated tests and backend dependency manifest.

## Not yet implemented
- Next.js frontend.
- Database or persistent memory.
- Authentication and guest/user separation.
- Agent planning, tool-calling loop or long-term memory.
- Expanded fault taxonomy.
- FFT/envelope analysis.
- Production deployment or live URL.

## Compatibility notes
The initial scoring logic is intentionally unchanged. Scores are heuristic, not probabilities. The sensor endpoint currently retrieves the CWRU reference on demand and therefore requires outbound internet access. It has no cache layer yet; production work should add a controlled cache and explicit sampling-rate/unit metadata.
