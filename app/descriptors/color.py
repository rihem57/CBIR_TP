import cv2
import numpy as np


def extract_color_histogram(image_path, bins=(16, 16, 16)):
    """
    Extrait un histogramme HSV normalisé d'une image.

    Parameters
    ----------
    image_path : str
        Chemin vers l'image.
    bins : tuple
        Nombre de bins pour H, S et V.

    Returns
    -------
    np.ndarray
        Vecteur représentant la signature couleur.
    """

    # Lire l'image
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Impossible de lire l'image : {image_path}")

    # Conversion BGR -> HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Histogramme HSV
    histogram = cv2.calcHist(
        [hsv],
        [0, 1, 2],
        None,
        list(bins),
        [0, 180, 0, 256, 0, 256]
    )

    # Normalisation
    histogram = cv2.normalize(
        histogram,
        histogram,
        norm_type=cv2.NORM_L1
    )

    # Transformation en vecteur 1D
    feature_vector = histogram.flatten()

    return feature_vector