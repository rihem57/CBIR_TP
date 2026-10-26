from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ============================================================
# ROUTERS
# ============================================================

from app.api.routes.search import router as search_router
from app.api.routes.images import router as images_router


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CBIR Image Retrieval",
    description="Content-Based Image Retrieval System",
    version="1.0.0"
)


# ============================================================
# API ROUTES
# ============================================================

app.include_router(
    search_router
)

app.include_router(
    images_router
)


# ============================================================
# STATIC IMAGES
# ============================================================

app.mount(
    "/images",
    StaticFiles(
        directory=str(PROJECT_ROOT / "data" / "test")
    ),
    name="images"
)


# ============================================================
# FRONTEND
# ============================================================

app.mount(
    "/",
    StaticFiles(
        directory=str(PROJECT_ROOT / "frontend"),
        html=True
    ),
    name="frontend"
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "ok",
        "message": "CBIR API is running"
    }