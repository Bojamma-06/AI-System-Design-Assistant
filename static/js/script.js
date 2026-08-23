 // =====================================================
// GENERATE SYSTEM DESIGN
// =====================================================

const generateButton =
    document.getElementById("generate-btn");

const requirementInput =
    document.getElementById("requirement");


if (generateButton && requirementInput) {

    generateButton.addEventListener("click", async () => {

        const requirement =
            requirementInput.value.trim();


        // -------------------------------------------------
        // VALIDATE REQUIREMENT
        // -------------------------------------------------

        if (!requirement) {

            alert(
                "Please describe your software system first."
            );

            return;
        }


        // -------------------------------------------------
        // DISABLE BUTTON WHILE GENERATING
        // -------------------------------------------------

        generateButton.disabled = true;

        generateButton.textContent =
            "Analyzing...";


        try {

            // -------------------------------------------------
            // SEND REQUIREMENT TO FLASK
            // -------------------------------------------------

            const response = await fetch(
                "/generate",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        requirement: requirement
                    })
                }
            );


            // -------------------------------------------------
            // CHECK RESPONSE TYPE
            // -------------------------------------------------

            const contentType =
                response.headers.get(
                    "content-type"
                ) || "";


            let data;


            // -------------------------------------------------
            // JSON RESPONSE
            // -------------------------------------------------

            if (
                contentType
                    .toLowerCase()
                    .includes("application/json")
            ) {

                data =
                    await response.json();

            }


            // -------------------------------------------------
            // NON-JSON RESPONSE
            // -------------------------------------------------

            else {

                const serverResponse =
                    await response.text();


                console.error(
                    "SERVER RETURNED NON-JSON RESPONSE:",
                    serverResponse
                );


                if (response.status === 404) {

                    throw new Error(
                        "The /generate endpoint was not found on the server."
                    );

                }


                if (response.status === 500) {

                    throw new Error(
                        "The server encountered an internal error while generating the system design."
                    );

                }


                if (response.status === 502) {

                    throw new Error(
                        "The server temporarily failed to respond. Please try again."
                    );

                }


                if (response.status === 503) {

                    throw new Error(
                        "The AI service is temporarily unavailable. Please try again in a moment."
                    );

                }


                throw new Error(
                    `Server returned an unexpected response (HTTP ${response.status}).`
                );

            }


            // -------------------------------------------------
            // CHECK HTTP RESPONSE
            // -------------------------------------------------

            if (!response.ok) {

                throw new Error(
                    data &&
                    data.error
                        ? data.error
                        : `Server error (HTTP ${response.status}).`
                );

            }


            // -------------------------------------------------
            // CHECK APPLICATION RESPONSE
            // -------------------------------------------------

            if (
                !data ||
                data.success !== true
            ) {

                throw new Error(
                    data &&
                    data.error
                        ? data.error
                        : "Unable to generate the system design."
                );

            }


            // -------------------------------------------------
            // VERIFY DESIGN OBJECT
            // -------------------------------------------------

            if (
                !data.design ||
                typeof data.design !== "object"
            ) {

                throw new Error(
                    "The server returned an invalid system design."
                );

            }


            // -------------------------------------------------
            // LOG COMPLETE AI RESPONSE
            // -------------------------------------------------

            console.log(
                "AI RESPONSE:",
                data
            );


            // =================================================
            // STORE COMPLETE SYSTEM DESIGN
            // =================================================

            sessionStorage.setItem(
                "systemDesign",
                JSON.stringify(
                    data.design
                )
            );


            // =================================================
            // STORE CURRENT REQUIREMENT
            // =================================================

            sessionStorage.setItem(
                "requirement",
                requirement
            );


            // =================================================
            // STORE INDIVIDUAL SECTIONS
            // =================================================
            // These are kept for backward compatibility
            // with the existing dashboard pages.
            // =================================================

            sessionStorage.setItem(
                "requirements",
                JSON.stringify(
                    data.design.requirements || {}
                )
            );


            sessionStorage.setItem(
                "architecture",
                JSON.stringify(
                    data.design.architecture || {}
                )
            );


            sessionStorage.setItem(
                "database",
                JSON.stringify(
                    data.design.database || {}
                )
            );


            sessionStorage.setItem(
                "critique",
                JSON.stringify(
                    data.design.critique || {}
                )
            );


            // =================================================
            // GENERATION SUCCESSFUL
            // =================================================

            console.log(
                "System design generated successfully."
            );


            // -------------------------------------------------
            // MOVE TO DASHBOARD
            // -------------------------------------------------

            window.location.href =
                "/dashboard";

        }


        // =====================================================
        // ERROR HANDLING
        // =====================================================

        catch (error) {

            console.error(
                "AI ERROR:",
                error
            );


            alert(
                "Unable to generate the system design.\n\n" +
                (
                    error.message ||
                    "An unexpected error occurred."
                )
            );


            // -------------------------------------------------
            // RE-ENABLE BUTTON
            // -------------------------------------------------

            generateButton.disabled = false;

            generateButton.textContent =
                "Generate System Design";

        }

    });

}


// =====================================================
// SERVICE WORKER
// =====================================================

if ("serviceWorker" in navigator) {

    window.addEventListener(
        "load",
        () => {

            navigator.serviceWorker
                .register(
                    "/static/service-worker.js"
                )

                .then(() => {

                    console.log(
                        "SysDesign AI service worker registered."
                    );

                })

                .catch(error => {

                    console.error(
                        "Service worker registration failed:",
                        error
                    );

                });

        }
    );

}