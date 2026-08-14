from services.gemini_client import generate_ai_response


def analyze_requirements(requirement):
    """
    Analyze the user's software requirement
    and return a structured system-design analysis.
    """

    prompt = f"""
You are an expert software architect helping design a software system.

Analyze the following software requirement:

{requirement}

Provide the analysis in exactly these four sections:

1. FUNCTIONAL REQUIREMENTS
List the important functions the system must provide.

2. NON-FUNCTIONAL REQUIREMENTS
List requirements related to performance, scalability, security,
availability, reliability, and maintainability.

3. SYSTEM ACTORS
Identify the main users, administrators, external systems,
or third-party services involved.

4. KEY CONSTRAINTS
Identify important technical, business, security,
regulatory, or operational constraints.

Keep the response concise, structured, and suitable
for a software engineering student.

Do not add unnecessary explanations.
"""

    return generate_ai_response(prompt)


if __name__ == "__main__":
    result = analyze_requirements(
        "Design an online food delivery application where users can browse restaurants, order food, make payments and track deliveries."
    )

    print(result)