from pathlib import Path
import sys
import numpy as np

# Racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.descriptors.color import extract_color_histogram
from app.search.distance import l1_distance


IMAGE_DIR = PROJECT_ROOT / "data" / "test"
FEATURE_DIR = PROJECT_ROOT / "data" / "features" / "color"


def search(query_image, top_k=10):

    # 1. Calculer le descripteur de l'image requête
    query_feature = extract_color_histogram(query_image)

    results = []

    # 2. Charger les descripteurs des images de la base
    for feature_file in FEATURE_DIR.glob("*.npy"):

        feature = np.load(feature_file)

        # 3. Calculer la distance L1
        distance = l1_distance(
            query_feature,
            feature
        )

        # Nom de l'image correspondante
        image_name = feature_file.stem

        results.append(
            (image_name, distance)
        )

    # 4. Trier par distance croissante
    results.sort(
        key=lambda x: x[1]
    )

    # 5. Retourner les top-k
    return results[:top_k]


if __name__ == "__main__":

    # Prendre une image comme requête
    query_image = next(
        p for p in IMAGE_DIR.iterdir()
        if p.is_file()
    )

    print("=" * 60)
    print("RECHERCHE CBIR PAR COULEUR")
    print("=" * 60)

    print()
    print("Image requête :", query_image.name)

    results = search(
        query_image,
        top_k=10
    )

    print()
    print("TOP 10 DES IMAGES LES PLUS SIMILAIRES")
    print("-" * 60)

    for rank, (image_name, distance) in enumerate(
        results,
        start=1
    ):

        print(
            f"{rank:02d}. "
            f"{image_name} "
            f"| distance L1 = {distance:.6f}"
        )