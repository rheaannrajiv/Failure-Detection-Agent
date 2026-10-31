from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api.routes import router

app = FastAPI(title="Failure Detective AI API", version="0.3.0", description="Agentic mechanical fault diagnosis, diagnostic tools and sensor analysis API")
origins = [item.strip() for item in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if item.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["*"])
app.include_router(router)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "failure-detective-api", "version": app.version}
