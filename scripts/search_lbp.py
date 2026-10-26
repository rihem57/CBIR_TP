from pathlib import Path
import sys
import numpy as np

# ============================================================
# Configuration du projet
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.descriptors.lbp import extract_lbp_histogram
from app.search.distance import l1_distance


IMAGE_DIR = PROJECT_ROOT / "data" / "test"
FEATURE_DIR = PROJECT_ROOT / "data" / "features" / "lbp"


# ============================================================
# Recherche LBP
# ============================================================

def search_lbp(query_image, top_k=10):
    """
    Recherche les images les plus similaires à une image requête
    en utilisant le descripteur LBP et la distance L1.
    """

    # Extraction du descripteur LBP de l'image requête
    query_feature = extract_lbp_histogram(query_image)

    results = []

    # Parcours des descripteurs LBP pré-calculés
    for feature_file in FEATURE_DIR.glob("*.npy"):

        # Chargement du descripteur
        feature = np.load(feature_file)

        # Calcul de la distance L1
        distance = l1_distance(query_feature, feature)

        # Nom de l'image correspondant au descripteur
        image_stem = feature_file.stem

        # Recherche de l'image originale
        matching_images = list(
            IMAGE_DIR.glob(f"{image_stem}.*")
        )

        if not matching_images:
            continue

        image_name = matching_images[0].name

        results.append({
            "image": image_name,
            "distance": float(distance)
        })

    # Tri par distance croissante
    results.sort(key=lambda x: x["distance"])

    # Retour des Top-K résultats
    return results[:top_k]


# ============================================================
# Programme principal
# ============================================================

if __name__ == "__main__":

    # Image utilisée comme requête
    query_image = IMAGE_DIR / "202.jpg"

    # Nombre de résultats souhaités
    top_k = 10

    print("=" * 60)
    print("RECHERCHE CBIR PAR LBP")
    print("=" * 60)

    print(f"Image requête : {query_image.name}")
    print(f"Descripteur  : LBP")
    print(f"Distance     : L1")
    print(f"Top-K        : {top_k}")

    print("=" * 60)
    print("TOP 10 DES IMAGES LES PLUS SIMILAIRES")
    print("=" * 60)

    # Exécution de la recherche
    results = search_lbp(query_image, top_k=top_k)

    # Affichage des résultats
    for index, result in enumerate(results, start=1):

        print(
            f"{index:02d}. "
            f"{result['image']} | "
            f"distance L1 = {result['distance']:.6f}"
        )

    print("=" * 60)
    print(f"Nombre de résultats : {len(results)}")
    print("=" * 60)