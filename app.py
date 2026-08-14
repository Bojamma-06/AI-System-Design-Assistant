from flask import Flask, render_template, request, jsonify

from services.system_design_service import generate_system_design


app = Flask(__name__)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html"
    )


# =========================================================
# REQUIREMENT ANALYSIS
# =========================================================

@app.route("/requirements")
def requirements():

    return render_template(
        "requirements.html"
    )


# =========================================================
# SYSTEM ARCHITECTURE
# =========================================================

@app.route("/architecture")
def architecture():

    return render_template(
        "architecture.html"
    )


# =========================================================
# DATABASE DESIGN
# =========================================================

@app.route("/database")
def database():

    return render_template(
        "database.html"
    )


# =========================================================
# AI DESIGN CRITIC
# =========================================================

@app.route("/critique")
def critique():

    return render_template(
        "critique.html"
    )


# =========================================================
# GENERATE COMPLETE SYSTEM DESIGN
# =========================================================

@app.route(
    "/generate",
    methods=["POST"]
)
def generate():

    try:

        # -------------------------------------------------
        # GET JSON FROM FRONTEND
        # -------------------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400


        # -------------------------------------------------
        # GET REQUIREMENT
        # -------------------------------------------------

        requirement = (
            data
            .get("requirement", "")
            .strip()
        )


        if not requirement:

            return jsonify({
                "success": False,
                "error":
                    "Please enter a software requirement."
            }), 400


        print(
            "\n========================================"
        )

        print(
            "USER REQUIREMENT"
        )

        print(
            "========================================"
        )

        print(
            requirement
        )


        # -------------------------------------------------
        # CALL GEMINI
        # -------------------------------------------------

        print(
            "\nGenerating complete system design..."
        )


        design = generate_system_design(
            requirement
        )


        print(
            "System design generated successfully."
        )


        # -------------------------------------------------
        # VERIFY DESIGN
        # -------------------------------------------------

        if not isinstance(
            design,
            dict
        ):

            raise ValueError(
                "AI returned an invalid system design."
            )


        # -------------------------------------------------
        # ENSURE REQUIRED SECTIONS EXIST
        # -------------------------------------------------

        design.setdefault(
            "requirements",
            {}
        )

        design.setdefault(
            "architecture",
            {}
        )

        design.setdefault(
            "database",
            {}
        )

        design.setdefault(
            "critique",
            {}
        )


        # -------------------------------------------------
        # PRINT STATUS
        # -------------------------------------------------

        print(
            "\n========================================"
        )

        print(
            "SYSTEM DESIGN GENERATION COMPLETE"
        )

        print(
            "========================================"
        )


        print(
            "Requirements:",
            "Generated"
            if design["requirements"]
            else "Missing"
        )


        print(
            "Architecture:",
            "Generated"
            if design["architecture"]
            else "Missing"
        )


        print(
            "Database:",
            "Generated"
            if design["database"]
            else "Missing"
        )


        print(
            "Critique:",
            "Generated"
            if design["critique"]
            else "Missing"
        )


        print(
            "========================================\n"
        )


        # -------------------------------------------------
        # RETURN COMPLETE DESIGN TO SCRIPT.JS
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                "System design generated successfully.",

            "design":
                design

        })


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        print(
            "\n========================================"
        )

        print(
            "AI ERROR"
        )

        print(
            "========================================"
        )

        print(
            str(e)
        )

        print(
            "========================================\n"
        )


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True

    )