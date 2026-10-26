from pathlib import Path
import sys
import numpy as np

# Ajouter la racine du projet au chemin Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.descriptors.color import extract_color_histogram

INPUT_DIR = Path("data/test")
OUTPUT_DIR = Path("data/features/color")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


images = [
    p for p in sorted(INPUT_DIR.iterdir())
    if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
]


print("=" * 60)
print("EXTRACTION DES DESCRIPTEURS COULEUR")
print("=" * 60)

print(f"Nombre d'images : {len(images)}")


success = 0
errors = 0


for i, image_path in enumerate(images, start=1):

    try:

        feature = extract_color_histogram(image_path)

        output_path = OUTPUT_DIR / f"{image_path.stem}.npy"

        np.save(output_path, feature)

        success += 1

        print(
            f"[{i}/{len(images)}] "
            f"{image_path.name} -> {len(feature)} valeurs"
        )

    except Exception as e:

        errors += 1

        print(
            f"[ERREUR] {image_path.name} : {e}"
        )


print()
print("=" * 60)
print("TERMINÉ")
print("=" * 60)

print(f"Images traitées : {success}")
print(f"Erreurs         : {errors}")
print(f"Répertoire      : {OUTPUT_DIR}")