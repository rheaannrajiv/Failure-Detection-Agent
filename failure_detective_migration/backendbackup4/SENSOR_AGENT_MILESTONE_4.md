# Milestone 4 — Sensor-aware agent

This update adds `POST /api/agent/investigate-with-sensor`, a multipart endpoint that processes an uploaded CSV/TXT/MAT recording using the existing signal-processing service and selected CWRU healthy reference. The agent receives a conditional `analyze_uploaded_sensor_data` tool and can call it during its bounded reasoning loop, then use the extracted evidence in its diagnosis.

Existing `/api/sensors/analyse`, `/api/agent/chat`, `/api/diagnose` and `/api/faults` endpoints are retained. Upload limit: 15 MB. Sensor comparisons are empirical against the configured reference and must not be interpreted as universal limits or definitive fault classifications.

Deploy by replacing only `failure_detective_migration/backend` in the Git repository, committing and pushing. Render should redeploy automatically. No new environment variables are required.
