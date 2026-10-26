/* ============================================================
   CBIR STUDIO
   API CLIENT
   Communication avec FastAPI
   ============================================================ */

const API_BASE_URL = "/api";
const IMAGE_BASE_URL = "/images";


/* ============================================================
   GENERIC API REQUEST
   ============================================================ */

async function apiRequest(url, options = {}) {

    const response = await fetch(url, {
        ...options,

        headers: {
            "Accept": "application/json",
            ...(options.headers || {})
        }
    });


    if (!response.ok) {

        let message = `Erreur HTTP ${response.status}`;

        try {

            const errorData = await response.json();

            if (errorData.detail) {
                message = errorData.detail;
            }

        } catch (error) {
            // Pas de réponse JSON
        }

        throw new Error(message);
    }


    return await response.json();
}


/* ============================================================
   GET AVAILABLE IMAGES
   ============================================================ */

async function getImages() {

    const data = await apiRequest(
        `${API_BASE_URL}/images`
    );


    // Cas 1 :
    // ["202.jpg", "203.jpg", ...]

    if (Array.isArray(data)) {
        return data;
    }


    // Cas 2 :
    // { images: [...] }

    if (Array.isArray(data.images)) {
        return data.images;
    }


    // Cas 3 :
    // { results: [...] }

    if (Array.isArray(data.results)) {
        return data.results;
    }


    return [];
}


/* ============================================================
   IMAGE URL
   ============================================================ */

function getImageUrl(filename) {

    if (!filename) {
        return "";
    }


    // Si l'API retourne déjà une URL complète

    if (
        filename.startsWith("http://") ||
        filename.startsWith("https://") ||
        filename.startsWith("/")
    ) {
        return filename;
    }


    // Image locale FastAPI

    return `${IMAGE_BASE_URL}/${encodeURIComponent(filename)}`;
}


/* ============================================================
   SEARCH IMAGES
   ============================================================ */

async function searchImages(
    image,
    descriptor,
    topK
) {

    if (!image) {

        throw new Error(
            "Aucune image de référence sélectionnée."
        );
    }


    if (!descriptor) {

        throw new Error(
            "Aucun descripteur sélectionné."
        );
    }


    const endpoint =
        `${API_BASE_URL}/search/${descriptor}`;


    const params = new URLSearchParams({

        image: image,

        top_k: String(topK)

    });


    return await apiRequest(
        `${endpoint}?${params.toString()}`
    );
}


/* ============================================================
   CHECK API STATUS
   ============================================================ */

async function checkApiStatus() {

    try {

        await apiRequest(
            `${API_BASE_URL}/images`
        );

        return true;

    } catch (error) {

        console.error(
            "API unavailable:",
            error
        );

        return false;
    }
}