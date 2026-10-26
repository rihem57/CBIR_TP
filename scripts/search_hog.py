from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from app.search.hog_search import search_hog


IMAGE_DIR = PROJECT_ROOT / "data" / "test"


if __name__ == "__main__":

    query_image = IMAGE_DIR / "202.jpg"

    top_k = 10

    print("=" * 60)
    print("RECHERCHE CBIR PAR HOG")
    print("=" * 60)

    print(
        f"Image requête : {query_image.name}"
    )

    print(
        "Descripteur  : HOG"
    )

    print(
        "Distance     : L1"
    )

    print(
        f"Top-K        : {top_k}"
    )

    print("=" * 60)

    print(
        "TOP 10 DES IMAGES LES PLUS SIMILAIRES"
    )

    print("=" * 60)

    results = search_hog(
        query_image,
        top_k=top_k
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"{index:02d}. "
            f"{result['image']} | "
            f"distance L1 = "
            f"{result['distance']:.6f}"
        )

    print("=" * 60)

    print(
        f"Nombre de résultats : "
        f"{len(results)}"
    )

    print("=" * 60)