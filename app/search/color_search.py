from pathlib import Path
import numpy as np

from app.descriptors.color import extract_color_histogram
from app.search.distance import l1_distance


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

IMAGE_DIR = PROJECT_ROOT / "data" / "test"
FEATURE_DIR = PROJECT_ROOT / "data" / "features" / "color"


# ============================================================
# COLOR SEARCH
# ============================================================

def search_color(query_image, top_k=10):

    # --------------------------------------------------------
    # 1. Extract descriptor of query image
    # --------------------------------------------------------

    query_feature = extract_color_histogram(query_image)

    results = []

    # --------------------------------------------------------
    # 2. Compare query with every indexed image
    # --------------------------------------------------------

    for feature_file in FEATURE_DIR.glob("*.npy"):

        feature = np.load(feature_file)

        distance = l1_distance(
            query_feature,
            feature
        )

        # ----------------------------------------------------
        # Find original image corresponding to feature
        # ----------------------------------------------------

        image_stem = feature_file.stem

        matching_images = list(
            IMAGE_DIR.glob(f"{image_stem}.*")
        )

        if not matching_images:
            continue

        image_name = matching_images[0].name

        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        results.append({
            "image": image_name,
            "distance": float(distance)
        })

    # --------------------------------------------------------
    # 3. Sort by increasing dissimilarity
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x["distance"]
    )

    # --------------------------------------------------------
    # 4. Return Top-K
    # --------------------------------------------------------

    return results[:top_k]