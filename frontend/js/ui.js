/* ============================================================
   CBIR STUDIO
   USER INTERFACE
   ============================================================ */


/* ============================================================
   DOM HELPERS
   ============================================================ */

function getElement(id) {
    return document.getElementById(id);
}


/* ============================================================
   QUERY PREVIEW
   ============================================================ */

function updateQueryPreview(filename) {

    const image = getElement("query-image");
    const placeholder = document.querySelector(
        ".preview-placeholder"
    );

    const filenameElement =
        getElement("query-filename");


    if (!filename) {

        image.classList.add("hidden");

        if (placeholder) {
            placeholder.classList.remove("hidden");
        }

        if (filenameElement) {
            filenameElement.textContent =
                "Aucune image sélectionnée";
        }

        return;
    }


    image.src = getImageUrl(filename);

    image.alt =
        `Image requête ${filename}`;


    image.classList.remove("hidden");


    if (placeholder) {
        placeholder.classList.add("hidden");
    }


    if (filenameElement) {
        filenameElement.textContent = filename;
    }
}


/* ============================================================
   IMAGE SELECT
   ============================================================ */

function populateImageSelector(images) {

    const select =
        getElement("image-select");


    if (!select) {
        return;
    }


    select.innerHTML = "";


    if (!images || images.length === 0) {

        const option =
            document.createElement("option");

        option.value = "";

        option.textContent =
            "Aucune image disponible";

        select.appendChild(option);

        return;
    }


    images.forEach((filename) => {

        const option =
            document.createElement("option");

        option.value = filename;

        option.textContent = filename;

        select.appendChild(option);
    });


    /*
     * Première image sélectionnée par défaut.
     */

    select.selectedIndex = 0;

    updateQueryPreview(
        select.value
    );
}


/* ============================================================
   DESCRIPTOR
   ============================================================ */

function updateDescriptorUI(descriptor) {

    const options =
        document.querySelectorAll(
            ".descriptor-option"
        );


    options.forEach((option) => {

        const currentDescriptor =
            option.dataset.descriptor;


        if (
            currentDescriptor === descriptor
        ) {

            option.classList.add("active");

        } else {

            option.classList.remove("active");
        }

    });


    /*
     * Mise à jour du résumé des résultats.
     */

    const activeDescriptor =
        getElement("active-descriptor");


    if (activeDescriptor) {

        activeDescriptor.textContent =
            formatDescriptorName(
                descriptor
            );
    }
}


/* ============================================================
   DESCRIPTOR NAME
   ============================================================ */

function formatDescriptorName(
    descriptor
) {

    const names = {

        color: "COLOR",

        lbp: "LBP",

        hog: "HOG"

    };


    return (
        names[descriptor] ||
        descriptor.toUpperCase()
    );
}


/* ============================================================
   TOP K
   ============================================================ */

function updateTopKUI(value) {

    const display =
        getElement("top-k-display");

    const indicator =
        getElement("top-k-value");


    if (display) {
        display.textContent = value;
    }


    if (indicator) {
        indicator.textContent = value;
    }
}


/* ============================================================
   RESULTS COUNT
   ============================================================ */

function updateResultsCount(count) {

    const element =
        getElement("results-count");


    if (element) {
        element.textContent = count;
    }
}


/* ============================================================
   SEARCH STATUS
   ============================================================ */

function setSearchStatus(
    type,
    message
) {

    const status =
        getElement("search-status");

    const messageElement =
        getElement("status-message");

    const dot =
        getElement("status-dot");


    if (!status) {
        return;
    }


    status.classList.remove(
        "loading",
        "error"
    );


    if (type === "loading") {

        status.classList.add("loading");

    }


    if (type === "error") {

        status.classList.add("error");
    }


    if (messageElement) {
        messageElement.textContent = message;
    }


    if (dot) {

        if (type === "error") {

            dot.style.background =
                "var(--danger)";

        } else if (type === "loading") {

            dot.style.background =
                "var(--warning)";

        } else {

            dot.style.background =
                "var(--success)";
        }
    }
}


/* ============================================================
   SEARCH BUTTON LOADING
   ============================================================ */

function setSearchButtonLoading(
    loading
) {

    const button =
        getElement("search-button");


    if (!button) {
        return;
    }


    if (loading) {

        button.disabled = true;

        button.dataset.originalText =
            button.textContent;

        button.innerHTML = `
            <span class="loading-spinner"></span>
            <span>Recherche en cours...</span>
        `;

    } else {

        button.disabled = false;

        button.innerHTML = `
            <span class="button-icon">→</span>
            <span>Lancer la recherche</span>
        `;
    }
}


/* ============================================================
   EMPTY RESULTS
   ============================================================ */

function showEmptyResults() {

    const grid =
        getElement("results-grid");


    if (!grid) {
        return;
    }


    grid.innerHTML = `
        <div
            id="results-empty"
            class="results-empty"
        >

            <div class="empty-icon">
                ◌
            </div>

            <h3>
                Aucun résultat pour le moment
            </h3>

            <p>
                Sélectionnez une image et lancez
                une recherche pour afficher les
                images similaires.
            </p>

        </div>
    `;


    updateResultsCount(0);
}


/* ============================================================
   ERROR RESULTS
   ============================================================ */

function showResultsError(message) {

    const grid =
        getElement("results-grid");


    if (!grid) {
        return;
    }


    grid.innerHTML = `
        <div class="error-message">

            <strong>
                Erreur de recherche
            </strong>

            <br><br>

            ${escapeHtml(message)}

        </div>
    `;


    updateResultsCount(0);
}


/* ============================================================
   RESULTS
   ============================================================ */

function displayResults(results) {

    const grid =
        getElement("results-grid");


    if (!grid) {
        return;
    }


    /*
     * Selon le backend, les résultats peuvent
     * être directement un tableau ou se trouver
     * dans data.results.
     */

    let items = results;


    if (
        results &&
        Array.isArray(results.results)
    ) {
        items = results.results;
    }


    if (!Array.isArray(items)) {
        items = [];
    }


    /*
     * Nettoyage.
     */

    grid.innerHTML = "";


    if (items.length === 0) {

        showEmptyResults();

        return;
    }


    updateResultsCount(
        items.length
    );


    /*
     * Création des cartes.
     */

    items.forEach(
        (item, index) => {

            const card =
                createResultCard(
                    item,
                    index
                );

            grid.appendChild(card);
        }
    );
}


/* ============================================================
   RESULT CARD
   ============================================================ */

function createResultCard(
    item,
    index
) {

    /*
     * On accepte plusieurs noms possibles
     * pour le fichier.
     */

    const filename =
        item.image ||
        item.filename ||
        item.name ||
        item.file ||
        "";


    /*
     * Distance.
     */

    const distance =
        item.distance !== undefined
            ? Number(item.distance)
            : null;


    const card =
        document.createElement("article");


    card.className =
        "result-card";


    /*
     * La première image est la requête
     * lorsqu'elle apparaît dans les résultats.
     */

    if (index === 0 && distance === 0) {

        card.classList.add(
            "is-query"
        );
    }


    card.dataset.filename =
        filename;


    const imageWrapper =
        document.createElement("div");

    imageWrapper.className =
        "result-image-wrapper";


    const image =
        document.createElement("img");

    image.className =
        "result-image";

    image.src =
        getImageUrl(filename);

    image.alt =
        `Résultat ${index + 1} - ${filename}`;

    image.loading =
        "lazy";


    /*
     * Rank
     */

    const rank =
        document.createElement("span");

    rank.className =
        "result-rank";

    rank.textContent =
        `#${String(index + 1).padStart(2, "0")}`;


    /*
     * Distance badge
     */

    const distanceBadge =
        document.createElement("span");

    distanceBadge.className =
        "result-distance";


    if (distance !== null) {

        distanceBadge.textContent =
            `L1 ${distance.toFixed(6)}`;

    } else {

        distanceBadge.textContent =
            "L1 —";
    }


    imageWrapper.appendChild(image);

    imageWrapper.appendChild(rank);

    imageWrapper.appendChild(
        distanceBadge
    );


    /*
     * Information
     */

    const information =
        document.createElement("div");

    information.className =
        "result-information";


    const filenameElement =
        document.createElement("span");

    filenameElement.className =
        "result-filename";

    filenameElement.textContent =
        filename;


    const description =
        document.createElement("div");

    description.className =
        "result-description";


    const descriptor =
        document.createElement("span");

    descriptor.textContent =
        "Image similaire";


    const action =
        document.createElement("span");

    action.textContent =
        "↗ Nouvelle requête";


    description.appendChild(
        descriptor
    );

    description.appendChild(
        action
    );


    information.appendChild(
        filenameElement
    );

    information.appendChild(
        description
    );


    card.appendChild(
        imageWrapper
    );

    card.appendChild(
        information
    );


    /*
     * Cliquer sur une image permet de
     * l'utiliser comme nouvelle requête.
     */

    card.addEventListener(
        "click",
        () => {

            if (
                typeof selectImageAndSearch ===
                "function"
            ) {

                selectImageAndSearch(
                    filename
                );
            }
        }
    );


    return card;
}


/* ============================================================
   HTML ESCAPE
   ============================================================ */

function escapeHtml(value) {

    if (value === null ||
        value === undefined) {

        return "";
    }


    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}