from pathlib import Path
from fastapi import APIRouter

PROJECT_ROOT = Path(__file__).resolve().parents[3]
IMAGE_DIR = PROJECT_ROOT / "data" / "test"

router = APIRouter(
    prefix="/api/images",
    tags=["Images"]
)

@router.get("")
def get_images():
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    images = [
        image.name
        for image in sorted(IMAGE_DIR.iterdir())
        if image.is_file()
        and image.suffix.lower() in extensions
    ]

    return {
        "count": len(images),
        "images": images
    }