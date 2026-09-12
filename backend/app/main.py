from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import Base, engine
from .routers import auth, scans, analysis

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RedFlag AI API", version="0.1.0")
allowed_origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(scans.router, prefix="/api", tags=["scans"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])

@app.get("/api/health")
def health():
    return {"status": "ok", "prototype_model": True}