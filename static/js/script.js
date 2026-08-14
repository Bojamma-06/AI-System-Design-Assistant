const generateButton =
    document.getElementById("generate-btn");

const requirementInput =
    document.getElementById("requirement");


if (generateButton && requirementInput) {

    generateButton.addEventListener("click", async () => {

        const requirement =
            requirementInput.value.trim();


        if (!requirement) {

            alert(
                "Please describe your software system first."
            );

            return;
        }


        generateButton.disabled = true;

        generateButton.textContent =
            "Analyzing...";


        try {

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


            const data =
                await response.json();


            console.log(
                "AI RESPONSE:",
                data
            );


            if (!response.ok || !data.success) {

                throw new Error(
                    data.error ||
                    "Unable to generate system design."
                );

            }


            /*
             * Store the COMPLETE structured design.
             *
             * This allows the dashboard pages to use
             * the design generated for the CURRENT requirement.
             */

            sessionStorage.setItem(
                "systemDesign",
                JSON.stringify(data.design)
            );


            sessionStorage.setItem(
                "requirement",
                requirement
            );


            /*
             * Keep individual sections as well.
             * This provides backward compatibility.
             */

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


            /*
             * Move to dashboard.
             */

            window.location.href =
                "/dashboard";

        }


        catch (error) {

            console.error(
                "AI ERROR:",
                error
            );


            alert(
                "Unable to generate the system design.\n\n" +
                error.message
            );


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

    window.addEventListener("load", () => {

        navigator.serviceWorker
            .register("/static/service-worker.js")
            .then(() => {
                console.log("SysDesign AI service worker registered.");
            })
            .catch(error => {
                console.error(
                    "Service worker registration failed:",
                    error
                );
            });

    });

}