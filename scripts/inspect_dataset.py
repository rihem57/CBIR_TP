from pathlib import Path
from PIL import Image
import pandas as pd

DATASET_DIR = Path("data/test")
OUTPUT_FILE = Path("data/metadata/images.csv")

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

records = []

for image_path in sorted(DATASET_DIR.iterdir()):

    if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        continue

    try:
        with Image.open(image_path) as img:

            width, height = img.size

            records.append({
                "filename": image_path.name,
                "path": str(image_path),
                "width": width,
                "height": height,
                "format": img.format,
                "mode": img.mode,
                "valid": True
            })

    except Exception as e:

        records.append({
            "filename": image_path.name,
            "path": str(image_path),
            "width": None,
            "height": None,
            "format": None,
            "mode": None,
            "valid": False
        })

df = pd.DataFrame(records)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("=" * 60)
print("ANALYSE DU DATASET")
print("=" * 60)

print(f"Nombre total d'images : {len(df)}")
print(f"Images valides        : {df['valid'].sum()}")
print(f"Images invalides      : {(~df['valid']).sum()}")

print("\nFormats :")
print(df["format"].value_counts())

print("\nDimensions :")
print(df[["width", "height"]].describe())

print(f"\nFichier créé : {OUTPUT_FILE}")