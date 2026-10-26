import cv2
import numpy as np


def extract_lbp_histogram(
    image_path,
    radius=1,
    n_points=8
):
    """
    Extract a Local Binary Pattern (LBP) histogram.

    Parameters
    ----------
    image_path : str or Path
        Path to the image.

    radius : int
        Radius of the circular neighborhood.

    n_points : int
        Number of neighboring points.

    Returns
    -------
    numpy.ndarray
        Normalized LBP histogram.
    """

    # --------------------------------------------------------
    # 1. Read image
    # --------------------------------------------------------

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(
            f"Impossible de lire l'image : {image_path}"
        )

    # --------------------------------------------------------
    # 2. Convert to grayscale
    # --------------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # --------------------------------------------------------
    # 3. Calculate LBP
    # --------------------------------------------------------

    lbp = np.zeros_like(
        gray,
        dtype=np.uint8
    )

    height, width = gray.shape

    for y in range(radius, height - radius):

        for x in range(radius, width - radius):

            center = gray[y, x]

            binary_value = 0

            for point in range(n_points):

                angle = (
                    2 * np.pi * point / n_points
                )

                neighbor_x = int(
                    round(
                        x + radius * np.cos(angle)
                    )
                )

                neighbor_y = int(
                    round(
                        y - radius * np.sin(angle)
                    )
                )

                neighbor = gray[
                    neighbor_y,
                    neighbor_x
                ]

                if neighbor >= center:

                    binary_value |= (
                        1 << point
                    )

            lbp[y, x] = binary_value

    # --------------------------------------------------------
    # 4. Build histogram
    # --------------------------------------------------------

    histogram, _ = np.histogram(
        lbp.ravel(),
        bins=256,
        range=(0, 256)
    )

    # --------------------------------------------------------
    # 5. Normalize histogram
    # --------------------------------------------------------

    histogram = histogram.astype(
        np.float32
    )

    histogram /= (
        histogram.sum() + 1e-8
    )

    return histogram