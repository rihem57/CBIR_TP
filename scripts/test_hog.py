from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from app.descriptors.hog import extract_hog_descriptor


IMAGE_PATH = PROJECT_ROOT / "data" / "test" / "202.jpg"


features = extract_hog_descriptor(
    IMAGE_PATH
)


print("=" * 60)
print("TEST DU DESCRIPTEUR HOG")
print("=" * 60)

print(f"Image       : {IMAGE_PATH.name}")
print(f"Dimension   : {features.shape}")
print(f"Type        : {features.dtype}")
print(f"Minimum     : {features.min():.6f}")
print(f"Maximum     : {features.max():.6f}")

print("=" * 60)