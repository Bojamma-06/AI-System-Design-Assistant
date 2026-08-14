from services.gemini_client import generate_ai_response


def critique_design(requirement, architecture, database):
    """
    Review the generated system architecture and database design
    and identify important issues and practical improvements.
    """

    prompt = f"""
You are a senior software architect reviewing a software design
created by a 5th-semester CSE student.

Your job is to critically evaluate the proposed design and provide
practical, technically accurate recommendations.

==================================================
USER REQUIREMENT
==================================================

{requirement}


==================================================
PROPOSED SYSTEM ARCHITECTURE
==================================================

{architecture}


==================================================
PROPOSED DATABASE DESIGN
==================================================

{database}


==================================================
IMPORTANT INSTRUCTIONS
==================================================

Evaluate the design based on:

- Scalability
- Performance
- Security
- Reliability
- Database design
- Maintainability
- Practicality

The project is a 5th-semester CSE mini-project.

DO NOT over-engineer the system.

Prefer practical technologies and improvements such as:

- PostgreSQL
- Redis
- Proper database indexing
- Database constraints
- Authentication
- Authorization / RBAC
- Input validation
- API security
- Caching
- Error handling
- Logging
- Backups
- Rate limiting

Do NOT recommend complex enterprise technologies such as:

- Kubernetes
- Service mesh
- Kafka clusters
- Distributed databases
- Complex microservice infrastructure

unless there is a clear and specific reason that the proposed
system actually requires them.

Do not make unsupported claims about the number of users,
transactions, or performance the system can handle.

Focus on identifying realistic problems and practical solutions.

==================================================
OUTPUT FORMAT
==================================================

Provide the review in EXACTLY these sections.

--------------------------------------------------
1. OVERALL DESIGN SCORE
--------------------------------------------------

Give a score from 1 to 10.

Format:

Score: X/10

Then provide a short explanation of the overall quality of
the architecture and database design.

--------------------------------------------------
2. SCALABILITY REVIEW
--------------------------------------------------

Identify the most important scalability problems.

For each issue use:

Issue:
Severity: Low / Medium / High

Explanation:

Recommendation:

If there are no significant problems, say:

No major scalability issues identified.

--------------------------------------------------
3. PERFORMANCE REVIEW
--------------------------------------------------

Identify possible performance problems.

Consider:

- Database queries
- API response time
- Caching
- Real-time tracking
- Heavy operations
- Indexing

For each issue use:

Issue:
Severity: Low / Medium / High

Explanation:

Recommendation:

--------------------------------------------------
4. SECURITY REVIEW
--------------------------------------------------

Review:

- Authentication
- Authorization
- Password security
- JWT/session handling
- API security
- Input validation
- Payment security
- Sensitive data protection
- Webhook security
- Common web vulnerabilities

For each important issue use:

Issue:
Severity: Low / Medium / High

Explanation:

Recommendation:

--------------------------------------------------
5. RELIABILITY REVIEW
--------------------------------------------------

Identify:

- Single points of failure
- Database failure risks
- Network failure handling
- Payment failure handling
- Real-time connection failures
- Data consistency problems
- Error recovery

For each issue use:

Issue:
Severity: Low / Medium / High

Explanation:

Recommendation:

--------------------------------------------------
6. DATABASE REVIEW
--------------------------------------------------

Review the proposed database for:

- Entity relationships
- Primary keys
- Foreign keys
- Constraints
- NULL handling
- UNIQUE constraints
- CHECK constraints
- Indexes
- Data consistency
- Financial data types
- Location data
- Potential query performance problems

For each issue use:

Issue:
Severity: Low / Medium / High

Explanation:

Recommendation:

--------------------------------------------------
7. ARCHITECTURE IMPROVEMENTS
--------------------------------------------------

List the most useful improvements that should be made
to the proposed architecture.

Use this format:

1. Improvement:
   Reason:

2. Improvement:
   Reason:

3. Improvement:
   Reason:

Keep the recommendations practical.

--------------------------------------------------
8. DATABASE IMPROVEMENTS
--------------------------------------------------

List the most useful improvements that should be made
to the proposed database design.

Use this format:

1. Improvement:
   Reason:

2. Improvement:
   Reason:

3. Improvement:
   Reason:

--------------------------------------------------
9. TOP 5 RECOMMENDATIONS
--------------------------------------------------

Provide exactly five prioritized recommendations.

Format:

1. [Highest Priority] Recommendation
2. [High Priority] Recommendation
3. [Medium Priority] Recommendation
4. [Medium Priority] Recommendation
5. [Low Priority] Recommendation

--------------------------------------------------
10. FINAL ASSESSMENT
--------------------------------------------------

Give a short final assessment of whether the proposed
design is:

- Poor
- Needs Improvement
- Good
- Very Good
- Excellent

Explain why in 2-4 sentences.

==================================================

Keep the response concise but technically meaningful.

Do not repeat the entire architecture or database design.
Only discuss problems, risks, and improvements.
"""

    return generate_ai_response(prompt)


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    requirement = """
    Design an online food delivery application where users
    can browse restaurants, order food, make payments
    and track deliveries.
    """

    architecture = """
    Frontend Client
    API Gateway
    Backend Application
    PostgreSQL
    Redis
    WebSocket Server
    Payment Gateway
    """

    database = """
    users
    restaurants
    categories
    menu_items
    orders
    order_items
    payments
    deliveries
    reviews
    """

    result = critique_design(
        requirement,
        architecture,
        database
    )

    print("\n")
    print("=" * 60)
    print("AI DESIGN CRITIC")
    print("=" * 60)
    print(result)
    print("=" * 60)