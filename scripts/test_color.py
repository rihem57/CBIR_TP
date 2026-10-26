import sys
from pathlib import Path

# Ajouter la racine du projet au chemin Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.descriptors.color import extract_color_histogram


image_path = next(Path("data/test").glob("*"))

feature = extract_color_histogram(image_path)

print("=" * 60)
print("TEST DU DESCRIPTEUR COULEUR")
print("=" * 60)

print("Image :", image_path)
print("Taille du vecteur :", feature.shape)
print("Nombre de valeurs :", len(feature))
print("Somme :", feature.sum())
print("Minimum :", feature.min())
print("Maximum :", feature.max())