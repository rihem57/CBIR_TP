from pathlib import Path
import sys

from fastapi import APIRouter, HTTPException, Query


# app/api/routes/search.py
PROJECT_ROOT = Path(__file__).resolve().parents[3]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from app.search.color_search import search_color
from app.search.lbp_search import search_lbp
from app.search.hog_search import search_hog

router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)


# ============================================================
# SEARCH BY COLOR
# ============================================================

@router.get("/color")
def search_by_color(
    image: str,
    top_k: int = Query(
        default=10,
        ge=1,
        le=50
    )
):

    image_path = PROJECT_ROOT / "data" / "test" / image

    # Vérifier que le fichier existe
    if not image_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Image introuvable : {image}"
        )

    results = search_color(
        image_path,
        top_k=top_k
    )

    return {
        "query": image,
        "descriptor": "HSV Color Histogram",
        "distance": "L1",
        "results": results
    }


# ============================================================
# SEARCH BY LBP
# ============================================================

@router.get("/lbp")
def search_by_lbp(
    image: str,
    top_k: int = Query(
        default=10,
        ge=1,
        le=50
    )
):

    image_path = PROJECT_ROOT / "data" / "test" / image

    # Vérifier que le fichier existe
    if not image_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Image introuvable : {image}"
        )

    results = search_lbp(
        image_path,
        top_k=top_k
    )

    return {
        "query": image,
        "descriptor": "LBP",
        "distance": "L1",
        "results": results
    }
    
    
# ============================================================
# SEARCH BY HOG
# ============================================================

@router.get("/hog")
def search_by_hog(
    image: str,
    top_k: int = Query(
        default=10,
        ge=1,
        le=50
    )
):

    image_path = PROJECT_ROOT / "data" / "test" / image

    # Vérifier que le fichier existe
    if not image_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Image introuvable : {image}"
        )

    results = search_hog(
        image_path,
        top_k=top_k
    )

    return {
        "query": image,
        "descriptor": "HOG",
        "distance": "L1",
        "results": results
    }
    
# ============================================================
# UNIFIED SEARCH
# ============================================================

@router.get("")
def unified_search(
    image: str,
    descriptor: str = Query(
        default="color"
    ),
    top_k: int = Query(
        default=10,
        ge=1,
        le=50
    )
):

    image_path = PROJECT_ROOT / "data" / "test" / image

    # Vérifier que l'image existe
    if not image_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Image introuvable : {image}"
        )

    # Normaliser le nom du descripteur
    descriptor = descriptor.lower().strip()

    # --------------------------------------------------------
    # COLOR
    # --------------------------------------------------------

    if descriptor == "color":

        results = search_color(
            image_path,
            top_k=top_k
        )

        descriptor_name = "HSV Color Histogram"

    # --------------------------------------------------------
    # LBP
    # --------------------------------------------------------

    elif descriptor == "lbp":

        results = search_lbp(
            image_path,
            top_k=top_k
        )

        descriptor_name = "LBP"

    # --------------------------------------------------------
    # HOG
    # --------------------------------------------------------

    elif descriptor == "hog":

        results = search_hog(
            image_path,
            top_k=top_k
        )

        descriptor_name = "HOG"

    # --------------------------------------------------------
    # DESCRIPTEUR INCONNU
    # --------------------------------------------------------

    else:

        raise HTTPException(
            status_code=400,
            detail=(
                "Descripteur invalide. "
                "Utilisez : color, lbp ou hog."
            )
        )

    return {
        "query": image,
        "descriptor": descriptor_name,
        "distance": "L1",
        "results": results
    }