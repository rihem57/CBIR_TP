from pathlib import Path

import numpy as np

from app.descriptors.lbp import extract_lbp_histogram
from app.search.distance import l1_distance


PROJECT_ROOT = Path(__file__).resolve().parents[2]

IMAGE_DIR = PROJECT_ROOT / "data" / "test"
FEATURE_DIR = PROJECT_ROOT / "data" / "features" / "lbp"


def search_lbp(query_image, top_k=10):
    """
    Recherche les images les plus similaires
    à une image requête selon le descripteur LBP.

    Similarité :
        distance L1 entre les histogrammes LBP.

    Plus la distance est faible,
    plus les images sont similaires.
    """

    # Extraire le descripteur LBP de l'image requête
    query_feature = extract_lbp_histogram(query_image)

    results = []

    # Parcourir les descripteurs LBP pré-calculés
    for feature_file in FEATURE_DIR.glob("*.npy"):

        feature = np.load(feature_file)

        # Distance L1
        distance = l1_distance(
            query_feature,
            feature
        )

        image_stem = feature_file.stem

        # Retrouver l'image correspondante
        matching_images = list(
            IMAGE_DIR.glob(f"{image_stem}.*")
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

    # Trier par distance croissante
    results.sort(
        key=lambda x: x["distance"]
    )

    return results[:top_k]