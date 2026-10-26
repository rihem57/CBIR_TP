from pathlib import Path

import numpy as np

from app.descriptors.hog import extract_hog_descriptor
from app.search.distance import l1_distance


PROJECT_ROOT = Path(__file__).resolve().parents[2]

IMAGE_DIR = PROJECT_ROOT / "data" / "test"
FEATURE_DIR = PROJECT_ROOT / "data" / "features" / "hog"


def search_hog(query_image, top_k=10):
    """
    Recherche les images les plus similaires
    selon le descripteur HOG.

    La similarité est calculée avec
    la distance L1.
    """

    # --------------------------------------------------------
    # 1. Extraire le HOG de l'image requête
    # --------------------------------------------------------

    query_feature = extract_hog_descriptor(
        query_image
    )

    results = []

    # --------------------------------------------------------
    # 2. Parcourir les descripteurs HOG pré-calculés
    # --------------------------------------------------------

    for feature_file in FEATURE_DIR.glob("*.npy"):

        feature = np.load(
            feature_file
        )

        # ----------------------------------------------------
        # 3. Calculer la distance L1
        # ----------------------------------------------------

        distance = l1_distance(
            query_feature,
            feature
        )

        # Nom de l'image correspondant
        image_stem = feature_file.stem

        matching_images = list(
            IMAGE_DIR.glob(
                f"{image_stem}.*"
            )
        )

        if not matching_images:
            continue

        image_name = matching_images[0].name

        results.append(
            {
                "image": image_name,
                "distance": float(distance)
            }
        )

    # --------------------------------------------------------
    # 4. Trier par distance croissante
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x["distance"]
    )

    # --------------------------------------------------------
    # 5. Retourner les Top-K
    # --------------------------------------------------------

    return results[:top_k]