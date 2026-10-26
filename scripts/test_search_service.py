from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.search.color_search import search_color


IMAGE_DIR = PROJECT_ROOT / "data" / "test"

query_image = next(
    p for p in IMAGE_DIR.iterdir()
    if p.is_file()
)


results = search_color(
    query_image,
    top_k=10
)


print("=" * 60)
print("TEST DU SERVICE DE RECHERCHE")
print("=" * 60)

print("Requête :", query_image.name)

for i, result in enumerate(results, start=1):

    print(
        f"{i:02d}. "
        f"{result['image']} "
        f"| distance = {result['distance']:.6f}"
    )