from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api.routes import router

app = FastAPI(
    title="Failure Detective AI API",
    version="0.4.0",
    description="Agentic mechanical fault diagnosis, diagnostic tools and sensor analysis API",
)

# Keep explicitly configured origins and always include the production frontend origin.
# Set VERCEL_FRONTEND_URL in Render if the deployed frontend uses a different domain.
configured_origins = [
    item.strip().rstrip("/")
    for item in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if item.strip()
]
frontend_origin = os.getenv(
    "VERCEL_FRONTEND_URL",
    "https://failure-detection-agent.vercel.app",
).strip().rstrip("/")
origins = list(dict.fromkeys(configured_origins + ([frontend_origin] if frontend_origin else [])))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Guest-Token", "Accept"],
)
app.include_router(router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "failure-detective-api", "version": app.version}
