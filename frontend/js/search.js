/* ============================================================
   CBIR STUDIO
   SEARCH CONTROLLER
   ============================================================ */


/* ============================================================
   SEARCH STATE
   ============================================================ */

const searchState = {

    image: "",

    descriptor: "color",

    topK: 10,

    images: [],

    searching: false

};


/* ============================================================
   INITIALIZATION
   ============================================================ */

function initializeSearch() {

    console.log(
        "CBIR Search initialized"
    );


    /*
     * Descriptor buttons
     */

    const descriptorButtons =
        document.querySelectorAll(
            ".descriptor-option"
        );


    descriptorButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const descriptor =
                    button.dataset.descriptor;

                setDescriptor(descriptor);

            }
        );

    });


    /*
     * Top-K minus
     */

    const topKMinus =
        document.getElementById(
            "top-k-minus"
        );


    if (topKMinus) {

        topKMinus.addEventListener(
            "click",
            () => {

                changeTopK(-5);

            }
        );

    }


    /*
     * Top-K plus
     */

    const topKPlus =
        document.getElementById(
            "top-k-plus"
        );


    if (topKPlus) {

        topKPlus.addEventListener(
            "click",
            () => {

                changeTopK(5);

            }
        );

    }


    /*
     * Image selector
     */

    const imageSelect =
        document.getElementById(
            "image-select"
        );


    if (imageSelect) {

        imageSelect.addEventListener(
            "change",
            event => {

                searchState.image =
                    event.target.value;


                updateQueryPreview(
                    searchState.image
                );

            }
        );

    }


    /*
     * Search button
     */

    const searchButton =
        document.getElementById(
            "search-button"
        );


    if (searchButton) {

        searchButton.addEventListener(
            "click",
            executeSearch
        );

    }


    /*
     * Initial UI

     */

    updateDescriptorUI(
        searchState.descriptor
    );


    updateTopKUI(
        searchState.topK
    );

}


/* ============================================================
   DESCRIPTOR
   ============================================================ */

function setDescriptor(descriptor) {

    if (!descriptor) {
        return;
    }


    searchState.descriptor =
        descriptor;


    updateDescriptorUI(
        descriptor
    );


    console.log(
        "Descriptor:",
        descriptor
    );

}


/* ============================================================
   TOP K
   ============================================================ */

function changeTopK(delta) {

    let newValue =
        searchState.topK + delta;


    /*
     * Minimum = 5
     * Maximum = 50
     */

    newValue =
        Math.max(
            5,
            Math.min(
                50,
                newValue
            )
        );


    searchState.topK =
        newValue;


    updateTopKUI(
        newValue
    );

}


/* ============================================================
   LOAD IMAGES
   ============================================================ */

async function loadImages() {

    try {

        console.log(
            "Loading images..."
        );


        const images =
            await getImages();


        searchState.images =
            images;


        populateImageSelector(
            images
        );


        /*
         * Select first image
         */

        if (
            images.length > 0 &&
            !searchState.image
        ) {

            const firstImage =
                typeof images[0] === "string"
                    ? images[0]
                    : (
                        images[0].filename ||
                        images[0].image ||
                        images[0].name ||
                        images[0].file
                    );


            searchState.image =
                firstImage;


            const imageSelect =
                document.getElementById(
                    "image-select"
                );


            if (imageSelect) {

                imageSelect.value =
                    firstImage;

            }


            updateQueryPreview(
                firstImage
            );

        }


        console.log(
            `${images.length} images loaded`
        );


    } catch (error) {

        console.error(
            "Erreur chargement images:",
            error
        );


        setSearchStatus(
            "error",
            "Impossible de charger les images."
        );

    }

}


/* ============================================================
   EXECUTE SEARCH
   ============================================================ */

async function executeSearch() {

    if (searchState.searching) {
        return;
    }


    if (!searchState.image) {

        setSearchStatus(
            "error",
            "Veuillez sélectionner une image."
        );

        return;
    }


    searchState.searching =
        true;


    /*
     * Loading UI
     */

    setSearchButtonLoading(
        true
    );


    setSearchStatus(
        "loading",
        "Recherche des images similaires..."
    );


    try {

        console.log(
            "Search:",
            searchState.image,
            searchState.descriptor,
            searchState.topK
        );


        const data =
            await searchImages(
                searchState.image,
                searchState.descriptor,
                searchState.topK
            );


        /*
         * API response
         */

        let results = [];


        if (Array.isArray(data)) {

            results = data;

        } else if (
            Array.isArray(data.results)
        ) {

            results = data.results;

        }


        /*
         * Display results
         */

        displayResults(
            results
        );


        /*
         * Update result information
         */

        updateResultsCount(
            results.length
        );


        const activeDescriptor =
            document.getElementById(
                "active-descriptor"
            );


        if (activeDescriptor) {

            activeDescriptor.textContent =
                formatDescriptorName(
                    searchState.descriptor
                );

        }


        setSearchStatus(
            "success",
            `${results.length} images similaires trouvées.`
        );


        /*
         * Scroll to results
         */

        const resultsSection =
            document.getElementById(
                "results"
            );


        if (resultsSection) {

            resultsSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }


    } catch (error) {

        console.error(
            "Search error:",
            error
        );


        showResultsError(
            error.message
        );


        setSearchStatus(
            "error",
            error.message ||
            "Une erreur est survenue."
        );

    } finally {

        searchState.searching =
            false;


        setSearchButtonLoading(
            false
        );

    }

}


/* ============================================================
   SELECT RESULT AS NEW QUERY
   ============================================================ */

async function selectImageAndSearch(
    filename
) {

    if (!filename) {
        return;
    }


    /*
     * Update state
     */

    searchState.image =
        filename;


    /*
     * Update selector
     */

    const imageSelect =
        document.getElementById(
            "image-select"
        );


    if (imageSelect) {

        imageSelect.value =
            filename;

    }


    /*
     * Update preview
     */

    updateQueryPreview(
        filename
    );


    /*
     * Search again
     */

    await executeSearch();

}


/* ============================================================
   GLOBAL ACCESS
   ============================================================ */

window.CBIRSearch = {

    executeSearch,

    setDescriptor,

    changeTopK,

    loadImages,

    selectImageAndSearch

};