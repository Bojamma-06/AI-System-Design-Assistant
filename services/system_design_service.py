from services.gemini_client import generate_ai_response

import json
import re


# =========================================================
# JSON EXTRACTION
# =========================================================

def extract_json(response):
    """
    Extract a JSON object from Gemini's response.

    Gemini may sometimes return JSON inside:
        ```json
        {...}
        ```

    This function removes the markdown wrapper and
    extracts the JSON object safely.
    """

    if not response:
        raise ValueError("Gemini returned an empty response.")

    response = response.strip()

    # Remove ```json opening fence
    response = re.sub(
        r"^\s*```json\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    # Remove ``` closing fence
    response = re.sub(
        r"\s*```\s*$",
        "",
        response
    )

    # Find JSON object
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "Gemini did not return a valid JSON object."
        )

    json_text = response[start:end + 1]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as error:

        raise ValueError(
            "Gemini returned malformed JSON."
        ) from error


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def ensure_list(value):
    """
    Make sure a value is always a list.
    """

    if isinstance(value, list):
        return value

    return []


def ensure_dict(value):
    """
    Make sure a value is always a dictionary.
    """

    if isinstance(value, dict):
        return value

    return {}


# =========================================================
# NORMALIZE REQUIREMENTS
# =========================================================

def normalize_requirements(requirements):
    """
    Normalize the requirements section so that
    requirements.html always receives the expected structure.
    """

    requirements = ensure_dict(requirements)

    functional = ensure_list(
        requirements.get("functional")
    )

    non_functional = ensure_list(
        requirements.get("non_functional")
    )

    actors = ensure_list(
        requirements.get("actors")
    )

    constraints = ensure_list(
        requirements.get("constraints")
    )

    # -----------------------------------------------------
    # Normalize functional requirements
    # -----------------------------------------------------

    normalized_functional = []

    for item in functional:

        if not isinstance(item, dict):
            continue

        normalized_functional.append({
            "title": str(
                item.get("title", "Requirement")
            ),
            "description": str(
                item.get("description", "")
            )
        })

    # -----------------------------------------------------
    # Normalize non-functional requirements
    # -----------------------------------------------------

    normalized_non_functional = []

    for item in non_functional:

        if not isinstance(item, dict):
            continue

        normalized_non_functional.append({
            "title": str(
                item.get("title", "Requirement")
            ),
            "description": str(
                item.get("description", "")
            )
        })

    # -----------------------------------------------------
    # Normalize actors
    # -----------------------------------------------------

    normalized_actors = []

    for item in actors:

        if not isinstance(item, dict):
            continue

        # Use title consistently because requirements.html
        # expects item.title
        title = (
            item.get("title")
            or item.get("name")
            or "System Actor"
        )

        normalized_actors.append({
            "title": str(title),
            "description": str(
                item.get("description", "")
            )
        })

    # -----------------------------------------------------
    # Normalize constraints
    # -----------------------------------------------------

    normalized_constraints = []

    for item in constraints:

        if not isinstance(item, dict):
            continue

        normalized_constraints.append({
            "title": str(
                item.get("title", "Constraint")
            ),
            "description": str(
                item.get("description", "")
            )
        })

    return {
        "functional": normalized_functional,
        "non_functional": normalized_non_functional,
        "actors": normalized_actors,
        "constraints": normalized_constraints
    }


# =========================================================
# NORMALIZE ARCHITECTURE
# =========================================================

def normalize_architecture(architecture):
    """
    Normalize the architecture section.
    """

    architecture = ensure_dict(architecture)

    components = ensure_list(
        architecture.get("components")
    )

    relationships = ensure_list(
        architecture.get("relationships")
    )

    technologies = ensure_list(
        architecture.get("technologies")
    )

    normalized_components = []

    for item in components:

        if not isinstance(item, dict):
            continue

        component_id = str(
            item.get("id", "")
        ).strip()

        component_name = str(
            item.get("name", "")
        ).strip()

        if not component_id:
            continue

        if not component_name:
            component_name = component_id

        normalized_components.append({
            "id": component_id,
            "name": component_name,
            "description": str(
                item.get("description", "")
            )
        })

    valid_ids = {
        item["id"]
        for item in normalized_components
    }

    normalized_relationships = []

    for item in relationships:

        if not isinstance(item, dict):
            continue

        source = str(
            item.get("from", "")
        ).strip()

        target = str(
            item.get("to", "")
        ).strip()

        if (
            source not in valid_ids
            or target not in valid_ids
        ):
            continue

        normalized_relationships.append({
            "from": source,
            "to": target,
            "label": str(
                item.get("label", "")
            )
        })

    normalized_technologies = []

    for item in technologies:

        if not isinstance(item, dict):
            continue

        normalized_technologies.append({
            "category": str(
                item.get("category", "")
            ),
            "technology": str(
                item.get("technology", "")
            )
        })

    return {
        "title": str(
            architecture.get(
                "title",
                "System Architecture"
            )
        ),
        "components": normalized_components,
        "relationships": normalized_relationships,
        "technologies": normalized_technologies
    }


# =========================================================
# NORMALIZE DATABASE
# =========================================================

def normalize_database(database):
    """
    Normalize the database section.
    """

    database = ensure_dict(database)

    entities = ensure_list(
        database.get("entities")
    )

    relationships = ensure_list(
        database.get("relationships")
    )

    normalized_entities = []

    entity_names = set()

    for entity in entities:

        if not isinstance(entity, dict):
            continue

        name = str(
            entity.get("name", "")
        ).strip()

        if not name:
            continue

        columns = ensure_list(
            entity.get("columns")
        )

        normalized_columns = []

        for column in columns:

            if not isinstance(column, dict):
                continue

            column_name = str(
                column.get("name", "")
            ).strip()

            if not column_name:
                continue

            normalized_columns.append({
                "name": column_name,
                "type": str(
                    column.get(
                        "type",
                        "VARCHAR"
                    )
                ),
                "key": str(
                    column.get("key", "")
                )
            })

        normalized_entities.append({
            "name": name,
            "columns": normalized_columns
        })

        entity_names.add(name)

    normalized_relationships = []

    for relationship in relationships:

        if not isinstance(relationship, dict):
            continue

        source = str(
            relationship.get("from", "")
        ).strip()

        target = str(
            relationship.get("to", "")
        ).strip()

        if (
            source not in entity_names
            or target not in entity_names
        ):
            continue

        relationship_type = str(
            relationship.get(
                "type",
                "ONE_TO_MANY"
            )
        )

        if relationship_type not in {
            "ONE_TO_ONE",
            "ONE_TO_MANY",
            "MANY_TO_MANY"
        }:
            relationship_type = "ONE_TO_MANY"

        normalized_relationships.append({
            "from": source,
            "to": target,
            "type": relationship_type,
            "label": str(
                relationship.get(
                    "label",
                    ""
                )
            )
        })

    return {
        "entities": normalized_entities,
        "relationships": normalized_relationships
    }


# =========================================================
# NORMALIZE CRITIQUE
# =========================================================

def normalize_critique(critique):
    """
    Normalize the AI design critique.
    """

    critique = ensure_dict(critique)

    score = critique.get("score", 0)

    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0

    # Keep score between 1 and 10
    score = max(1, min(10, score))

    categories = [
        "scalability",
        "performance",
        "security",
        "reliability",
        "database",
        "architecture"
    ]

    normalized = {
        "score": score
    }

    for category in categories:

        normalized[category] = ensure_list(
            critique.get(category)
        )

    recommendations = ensure_list(
        critique.get("recommendations")
    )

    normalized_recommendations = []

    for item in recommendations:

        if isinstance(item, dict):

            normalized_recommendations.append({
                "issue": str(
                    item.get(
                        "issue",
                        "Design improvement"
                    )
                ),
                "recommendation": str(
                    item.get(
                        "recommendation",
                        ""
                    )
                )
            })

        elif isinstance(item, str):

            normalized_recommendations.append({
                "issue": "Design improvement",
                "recommendation": item
            })

    normalized["recommendations"] = (
        normalized_recommendations
    )

    normalized["summary"] = str(
        critique.get(
            "summary",
            ""
        )
    )

    return normalized


# =========================================================
# MAIN SYSTEM DESIGN GENERATOR
# =========================================================

def generate_system_design(requirement):
    """
    Generate the complete system design using ONE Gemini API call.

    The generated design contains:

    1. Requirement Analysis
    2. System Architecture
    3. Database Design
    4. AI Design Critique

    Everything is generated specifically for the CURRENT
    software requirement.
    """

    if not requirement:
        raise ValueError(
            "Software requirement cannot be empty."
        )

    requirement = requirement.strip()

    # =====================================================
    # GEMINI PROMPT
    # =====================================================

    prompt = f"""
You are an expert software architect, database designer,
requirements analyst, and system design reviewer.

The user has provided the following CURRENT software
requirement:

================ CURRENT REQUIREMENT ================

{requirement}

=======================================================

IMPORTANT:

Design the system ONLY for the CURRENT requirement above.

The current requirement is the source of truth.

Do NOT assume that the system is a food delivery system.

Do NOT reuse architecture, database entities, modules,
actors, relationships, or technologies from previous requests.

Every part of your answer must be relevant to the CURRENT
requirement.

For example:

If the requirement is a Hospital Management System,
possible domain modules could include Patient Management,
Doctor Management, Appointment Management, Medical Records,
Laboratory, Pharmacy, Billing, Staff Management, etc.

If the requirement is a Library Management System,
possible domain modules could include Book Management,
Member Management, Borrowing, Returning, Fine Management,
Catalog/Search, etc.

If the requirement is a Course Registration System,
possible domain modules could include Student Management,
Course Management, Registration, Enrollment Validation,
Faculty Management, etc.

These are ONLY examples.

Do NOT automatically include these modules.

Select components based entirely on the CURRENT requirement.

The final design must clearly demonstrate that the AI
understood the user's software domain.

Keep the system realistic for a 5th-semester CSE mini project.

Do not over-engineer.

Avoid unnecessary technologies such as Kubernetes, Kafka,
microservices, service meshes, complex load balancers,
event buses, or distributed infrastructure unless the
CURRENT requirement genuinely requires them.

Prefer a practical and understandable architecture.

Return ONLY valid JSON.

Do not use Markdown.

Do not add any explanation outside the JSON.

=======================================================
REQUIRED JSON STRUCTURE
=======================================================

{{
  "requirements": {{
    "functional": [
      {{
        "title": "Requirement title",
        "description": "Short explanation"
      }}
    ],

    "non_functional": [
      {{
        "title": "Requirement title",
        "description": "Short explanation"
      }}
    ],

    "actors": [
      {{
        "title": "Actor name",
        "description": "Short explanation"
      }}
    ],

    "constraints": [
      {{
        "title": "Constraint title",
        "description": "Short explanation"
      }}
    ]
  }},

  "architecture": {{

    "title": "System Architecture",

    "components": [
      {{
        "id": "unique_component_id",
        "name": "Component Name",
        "description": "Responsibility of this component"
      }}
    ],

    "relationships": [
      {{
        "from": "component_id",
        "to": "component_id",
        "label": "HTTPS / REST"
      }}
    ],

    "technologies": [
      {{
        "category": "Frontend",
        "technology": "HTML CSS JavaScript"
      }}
    ]
  }},

  "database": {{

    "entities": [
      {{
        "name": "ENTITY_NAME",
        "columns": [
          {{
            "name": "id",
            "type": "BIGINT",
            "key": "PK"
          }}
        ]
      }}
    ],

    "relationships": [
      {{
        "from": "ENTITY_A",
        "to": "ENTITY_B",
        "type": "ONE_TO_MANY",
        "label": "has"
      }}
    ]
  }},

  "critique": {{

    "score": 8.5,

    "scalability": [
      "Short scalability observation"
    ],

    "performance": [
      "Short performance observation"
    ],

    "security": [
      "Short security observation"
    ],

    "reliability": [
      "Short reliability observation"
    ],

    "database": [
      "Short database observation"
    ],

    "architecture": [
      "Short architecture observation"
    ],

    "recommendations": [
      {{
        "issue": "Short issue",
        "recommendation": "Short actionable recommendation"
      }}
    ],

    "summary": "Short overall design review"
  }}
}}

=======================================================
REQUIREMENT RULES
=======================================================

1. Generate 5-10 functional requirements.

2. Generate 4-6 non-functional requirements.

3. Generate only actors that are actually relevant to the
   CURRENT software system.

4. Generate realistic constraints based on the CURRENT
   requirement.

5. Do not invent unrelated actors.

=======================================================
ARCHITECTURE RULES
=======================================================

1. Architecture MUST be domain-specific.

2. Do NOT create a generic architecture that could apply
   equally to any software system.

3. Include:

   - A suitable frontend/client
   - A backend/application layer
   - Domain-specific modules
   - A suitable database
   - External services only when genuinely required

4. Domain-specific modules are extremely important.

5. For a Hospital Management System, do not simply return:

   Frontend
   Backend
   Database
   Notification

   Instead identify appropriate hospital-related modules
   based on the requirement.

6. For a Library Management System, do not return hospital
   or food-delivery modules.

7. For a Food Delivery System, restaurant/order/delivery
   modules may be appropriate.

8. The architecture must change when the user's requirement
   changes.

9. Component IDs must be unique.

10. Relationship "from" and "to" values MUST exactly match
    existing component IDs.

11. Relationships must represent realistic communication
    or data flow.

12. Do not add a Notification Module unless notifications
    are actually relevant.

13. Do not add Payment Gateway unless payment functionality
    is actually required.

14. Do not add Maps/Geolocation unless location functionality
    is actually required.

15. Do not add Redis unless caching or real-time functionality
    genuinely benefits from it.

16. Keep the architecture simple enough for a
    5th-semester CSE mini project.

=======================================================
DATABASE RULES
=======================================================

1. Database entities MUST match the CURRENT requirement.

2. Do NOT reuse database tables from previous systems.

3. Do NOT include food-delivery tables unless the CURRENT
   requirement requires them.

4. Do NOT include hospital tables unless the CURRENT
   requirement requires them.

5. Do NOT include library tables unless the CURRENT
   requirement requires them.

6. Every entity should contain 3-10 useful columns.

7. Use:

   PK = Primary Key
   FK = Foreign Key
   UK = Unique Key
   "" = Normal field

8. Relationships must reference actual entity names.

9. Relationship types must be one of:

   ONE_TO_ONE
   ONE_TO_MANY
   MANY_TO_MANY

10. Avoid unnecessary tables.

=======================================================
CRITIQUE RULES
=======================================================

The AI must evaluate the design that it JUST generated.

Score the design from 1 to 10.

The critique must consider:

- Scalability
- Performance
- Security
- Reliability
- Database design
- Architecture quality

IMPORTANT:

The critique must NOT be generic.

The critique must refer to the CURRENT system.

For example, a hospital system should receive
hospital-specific observations.

A library system should receive library-specific
observations.

Recommendations must be practical and actionable.

Keep individual observations short.

Generate 2-4 observations for each critique category.

Generate 3-5 recommendations.

=======================================================
JSON RULES
=======================================================

1. Return valid JSON only.

2. Do not use Markdown.

3. Do not put comments inside JSON.

4. Do not use trailing commas.

5. Use double quotes for JSON strings.

6. Escape special characters correctly.

7. Do not return anything before or after the JSON object.

=======================================================
"""

    # =====================================================
    # CALL GEMINI
    # =====================================================

    response = generate_ai_response(prompt)

    # =====================================================
    # PARSE JSON
    # =====================================================

    design = extract_json(response)

    if not isinstance(design, dict):
        raise ValueError(
            "Gemini returned an invalid system design."
        )

    # =====================================================
    # NORMALIZE ALL SECTIONS
    # =====================================================

    design["requirements"] = normalize_requirements(
        design.get("requirements", {})
    )

    design["architecture"] = normalize_architecture(
        design.get("architecture", {})
    )

    design["database"] = normalize_database(
        design.get("database", {})
    )

    design["critique"] = normalize_critique(
        design.get("critique", {})
    )

    # =====================================================
    # RAW JSON OUTPUTS
    # =====================================================

    design["requirements_raw"] = json.dumps(
        design["requirements"],
        indent=2,
        ensure_ascii=False
    )

    design["architecture_raw"] = json.dumps(
        design["architecture"],
        indent=2,
        ensure_ascii=False
    )

    design["database_raw"] = json.dumps(
        design["database"],
        indent=2,
        ensure_ascii=False
    )

    design["critique_raw"] = json.dumps(
        design["critique"],
        indent=2,
        ensure_ascii=False
    )

    # =====================================================
    # DEBUG OUTPUT
    # =====================================================

    print()
    print("==============================================")
    print("SYSTEM DESIGN GENERATED")
    print("==============================================")
    print(
        json.dumps(
            design,
            indent=2,
            ensure_ascii=False
        )
    )
    print("==============================================")
    return design