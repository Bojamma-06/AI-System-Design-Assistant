from services.gemini_client import generate_ai_response


def generate_database_design(requirement):
    """
    Generate a database design based on the user's
    software requirement.
    """

    prompt = f"""
You are an expert database architect.

Design a relational database for the following software
requirement:

{requirement}

Provide the database design in exactly these sections:

1. ENTITIES

List the main entities required by the system.

2. TABLES

For each important table, provide:

- Table name
- Column name
- Data type
- Primary key
- Foreign key, if applicable
- Short description

3. RELATIONSHIPS

Explain the relationships between the tables.

Clearly mention cardinality such as:
- One-to-one
- One-to-many
- Many-to-many

4. IMPORTANT CONSTRAINTS

Suggest important:
- Primary keys
- Foreign keys
- NOT NULL constraints
- UNIQUE constraints
- CHECK constraints

5. INDEXING RECOMMENDATIONS

Suggest columns that should be indexed
and briefly explain why.

6. DATABASE SUMMARY

Provide a simple text-based representation of
the main table relationships.

Example:

USER
 |
 | 1
 |
 | N
ORDER
 |
 | N
 |
 | 1
RESTAURANT

Keep the database design realistic and suitable
for a 5th-semester CSE mini project.

Do not over-engineer the database.
"""

    return generate_ai_response(prompt)


if __name__ == "__main__":
    result = generate_database_design(
        "Design an online food delivery application where users can browse restaurants, order food, make payments and track deliveries."
    )

    print(result)