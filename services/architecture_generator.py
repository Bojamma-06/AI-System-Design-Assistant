from services.gemini_client import generate_ai_response


def generate_architecture(requirement):
    """
    Generate a high-level system architecture
    based on the user's software requirement.
    """

    prompt = f"""
You are an expert software architect.

Design a high-level system architecture for the following
software requirement:

{requirement}

Provide the architecture in exactly these sections:

1. ARCHITECTURE COMPONENTS

List the major components or services required.
For each component, briefly explain its responsibility.

2. COMPONENT RELATIONSHIPS

Explain which components communicate with each other
and how they are connected.

3. DATA FLOW

Explain how data moves through the system from the user
to the backend services and database.

4. RECOMMENDED TECHNOLOGIES

Suggest suitable technologies for:
- Frontend
- Backend
- Database
- Cache
- Authentication
- Messaging
- Deployment

5. ARCHITECTURE SUMMARY

Provide a simple text-based representation of the architecture.

Example:

User
  |
  v
API Gateway
  |
  +---- User Service
  |
  +---- Order Service
  |
  +---- Payment Service
  |
  v
Database

Keep the architecture realistic and suitable for a
5th-semester CSE mini project.

Do not over-engineer the system.
"""

    return generate_ai_response(prompt)


if __name__ == "__main__":
    result = generate_architecture(
        "Design an online food delivery application where users can browse restaurants, order food, make payments and track deliveries."
    )

    print(result)