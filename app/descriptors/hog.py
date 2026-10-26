import cv2
import numpy as np
from skimage.feature import hog


def extract_hog_descriptor(
    image_path,
    orientations=9,
    pixels_per_cell=(8, 8),
    cells_per_block=(2, 2)
):
    """
    Extrait le descripteur HOG d'une image.

    Parameters
    ----------
    image_path : str ou Path
        Chemin vers l'image.

    orientations : int
        Nombre de bins d'orientation du gradient.

    pixels_per_cell : tuple
        Taille d'une cellule HOG.

    cells_per_block : tuple
        Nombre de cellules par bloc.

    Returns
    -------
    numpy.ndarray
        Vecteur HOG normalisé.
    """

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(
            f"Impossible de lire l'image : {image_path}"
        )

    # OpenCV : BGR → RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Calcul HOG
    features = hog(
        image,
        orientations=orientations,
        pixels_per_cell=pixels_per_cell,
        cells_per_block=cells_per_block,
        block_norm="L2-Hys",
        channel_axis=-1
    )

    return features.astype(np.float32)