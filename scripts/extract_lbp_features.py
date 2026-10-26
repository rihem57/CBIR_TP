from pathlib import Path
import sys

import numpy as np


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ============================================================
# IMPORT
# ============================================================

from app.descriptors.lbp import (
    extract_lbp_histogram
)


# ============================================================
# DIRECTORIES
# ============================================================

IMAGE_DIR = (
    PROJECT_ROOT
    / "data"
    / "test"
)

FEATURE_DIR = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "lbp"
)

FEATURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# IMAGE EXTENSIONS
# ============================================================

EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# ============================================================
# GET IMAGES
# ============================================================

images = sorted(
    [
        image
        for image in IMAGE_DIR.iterdir()
        if image.is_file()
        and image.suffix.lower()
        in EXTENSIONS
    ]
)


print("=" * 60)
print("EXTRACTION DES DESCRIPTEURS LBP")
print("=" * 60)

print(
    f"Images trouvées : {len(images)}"
)

print(
    f"Dossier sortie : {FEATURE_DIR}"
)

print("=" * 60)


# ============================================================
# EXTRACTION
# ============================================================

success = 0
errors = 0

for index, image_path in enumerate(images, start=1):

    try:

        feature = extract_lbp_histogram(
            image_path
        )

        output_path = (
            FEATURE_DIR
            / f"{image_path.stem}.npy"
        )

        np.save(
            output_path,
            feature
        )

        success += 1

        print(
            f"[{index}/{len(images)}] "
            f"{image_path.name} -> "
            f"{output_path.name}"
        )

    except Exception as error:

        errors += 1

        print(
            f"[ERREUR] "
            f"{image_path.name} : "
            f"{error}"
        )


# ============================================================
# SUMMARY
# ============================================================

print("=" * 60)
print("EXTRACTION TERMINÉE")
print("=" * 60)

print(
    f"Succès : {success}"
)

print(
    f"Erreurs : {errors}"
)

print(
    f"Descripteurs créés : "
    f"{len(list(FEATURE_DIR.glob('*.npy')))}"
)

print("=" * 60)