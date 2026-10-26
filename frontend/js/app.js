/* ============================================================
   CBIR STUDIO
   APPLICATION
   ============================================================ */


/* ============================================================
   APPLICATION INITIALIZATION
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        console.log(
            "CBIR Studio — Initialisation..."
        );


        /*
         * Initialiser la logique de recherche.
         */

        initializeSearch();


        /*
         * Vérifier l'API.
         */

        await initializeApiStatus();


        /*
         * Charger les images.
         */

        await loadImages();


        /*
         * Navigation.
         */

        initializeNavigation();


        console.log(
            "CBIR Studio — Application prête."
        );
    }
);


/* ============================================================
   API STATUS
   ============================================================ */

async function initializeApiStatus() {

    const statusContainers =
        document.querySelectorAll(
            ".api-status"
        );


    const online =
        await checkApiStatus();


    statusContainers.forEach(
        (container) => {

            const indicator =
                container.querySelector(
                    ".status-indicator"
                );

            const text =
                container.querySelector(
                    ".status-text"
                );


            if (online) {

                if (indicator) {

                    indicator.style.background =
                        "var(--success)";
                }


                if (text) {

                    text.textContent =
                        "API Online";
                }

            } else {

                if (indicator) {

                    indicator.style.background =
                        "var(--danger)";

                    indicator.style.boxShadow =
                        "0 0 10px rgba(239, 109, 122, 0.65)";
                }


                if (text) {

                    text.textContent =
                        "API Offline";
                }
            }
        }
    );
}


/* ============================================================
   NAVIGATION
   ============================================================ */

function initializeNavigation() {

    const links =
        document.querySelectorAll(
            ".nav-link"
        );


    links.forEach(
        (link) => {

            link.addEventListener(
                "click",
                () => {

                    links.forEach(
                        item =>
                            item.classList.remove(
                                "active"
                            )
                    );


                    link.classList.add(
                        "active"
                    );
                }
            );
        }
    );
}