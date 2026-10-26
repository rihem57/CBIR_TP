from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from app.descriptors.hog import extract_hog_descriptor


IMAGE_DIR = PROJECT_ROOT / "data" / "test"
FEATURE_DIR = PROJECT_ROOT / "data" / "features" / "hog"


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


def extract_all_hog_features():

    FEATURE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    images = [
        image
        for image in IMAGE_DIR.iterdir()
        if image.is_file()
        and image.suffix.lower() in IMAGE_EXTENSIONS
    ]

    print("=" * 60)
    print("EXTRACTION DES DESCRIPTEURS HOG")
    print("=" * 60)

    print(f"Dossier images : {IMAGE_DIR}")
    print(f"Dossier features : {FEATURE_DIR}")
    print(f"Nombre d'images : {len(images)}")

    print("=" * 60)

    success = 0
    errors = 0

    for index, image_path in enumerate(
        images,
        start=1
    ):

        try:

            feature = extract_hog_descriptor(
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
                f"[{index:04d}/{len(images):04d}] "
                f"{image_path.name} → "
                f"{feature.shape}"
            )

        except Exception as e:

            errors += 1

            print(
                f"[ERREUR] {image_path.name} : {e}"
            )

    print("=" * 60)
    print("EXTRACTION TERMINÉE")
    print("=" * 60)

    print(f"Images traitées : {success}")
    print(f"Erreurs         : {errors}")
    print("=" * 60)


if __name__ == "__main__":

    extract_all_hog_features()