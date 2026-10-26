from pathlib import Path
import sys

import numpy as np


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ============================================================
# IMPORT
# ============================================================

from app.descriptors.lbp import (
    extract_lbp_histogram
)


# ============================================================
# TEST IMAGE
# ============================================================

IMAGE_PATH = (
    PROJECT_ROOT
    / "data"
    / "test"
    / "202.jpg"
)


# ============================================================
# EXTRACT LBP
# ============================================================

feature = extract_lbp_histogram(
    IMAGE_PATH
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 60)
print("TEST LBP")
print("=" * 60)

print(
    f"Image : {IMAGE_PATH.name}"
)

print(
    f"Dimension du descripteur : {feature.shape[0]}"
)

print(
    f"Somme du histogramme : {feature.sum():.6f}"
)

print(
    f"Minimum : {feature.min():.6f}"
)

print(
    f"Maximum : {feature.max():.6f}"
)

print(
    "\nPremières valeurs :"
)

print(
    feature[:20]
)

print("=" * 60)