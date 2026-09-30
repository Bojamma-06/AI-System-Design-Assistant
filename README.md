# 🤖 AI System Design Assistant

An AI-powered web application that transforms **natural-language software requirements into a structured software system design**.

The system analyzes a user's requirements and generates:

* 📋 Functional & Non-Functional Requirements
* 👥 Actors and System Constraints
* 🏗️ Software Architecture
* 🗄️ Database Design
* 🔍 AI-Based Design Critique

The goal is to help students, developers, and software teams move from an initial idea or requirement to a structured system design faster and more systematically.

---

## 🚀 Live Demo

**Live Application:**
https://sysdesign-ai-1z4i.onrender.com

**GitHub Repository:**
https://github.com/Bojamma-06/AI-System-Design-Assistant

---

## 🎯 Problem Statement

Designing a software system from a natural-language requirement usually requires multiple steps such as identifying requirements, defining system components, designing the database, and reviewing the proposed architecture.

For beginners and developers, these steps can be time-consuming and difficult to organize.

The **AI System Design Assistant** simplifies this process by using Generative AI to transform a software requirement into a structured system design.

---

## 💡 Proposed Solution

The user provides a software requirement in natural language.

For example:

> "Build an online food delivery application where customers can browse restaurants, place orders, make payments, and track deliveries."

The system processes the requirement and generates a structured design covering:

```text
User Requirement
       ↓
AI Analysis
       ↓
Requirements
       ↓
Architecture
       ↓
Database Design
       ↓
AI Design Critique
```

This provides the user with a starting point for understanding and developing the proposed system.

---

## ✨ Features

### 1. 📋 Requirements Analysis

The AI identifies:

* Functional requirements
* Non-functional requirements
* Actors
* System constraints
* Important domain-specific requirements

---

### 2. 🏗️ Architecture Design

The application generates a suitable software architecture based on the provided requirements.

It identifies:

* Major system components
* Responsibilities of components
* Communication between components
* Appropriate technologies or architectural patterns

The system avoids unnecessary over-engineering and generates architecture according to the actual requirements.

---

### 3. 🗄️ Database Design

The AI proposes a database structure based on the system requirements.

It can identify:

* Entities
* Attributes
* Primary keys
* Foreign keys
* Relationships
* Important database constraints

---

### 4. 🔍 AI Design Critique

The generated design is reviewed by an AI-based critic.

The critique checks for issues such as:

* Missing requirements
* Inconsistencies
* Unnecessary complexity
* Potential scalability problems
* Database design issues
* Architectural concerns
* Possible improvements

This provides an additional review layer instead of simply generating a design.

---

### 5. 🌐 Web-Based Interface

The application provides a simple web interface where users can:

1. Enter their software requirements.
2. Generate the system design.
3. View requirements.
4. View architecture.
5. View database design.
6. Review the AI critique.

---

## 🧠 AI Workflow

The application uses a structured AI pipeline:

```text
                 User Requirement
                        │
                        ▼
              ┌──────────────────┐
              │  AI Processing   │
              └────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    Requirements   Architecture   Database
          │            │            │
          └────────────┼────────────┘
                       ▼
                AI Design Critique
                       │
                       ▼
              Structured System Design
```

The AI response is normalized into structured sections so that each part of the generated design can be displayed separately.

---

## 🛠️ Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### AI

* Google Gemini API

### Deployment

* Render

### Version Control

* Git
* GitHub

---

## 📁 Project Structure

```text
AI-System-Design-Assistant/
│
├── app.py
├── requirements.txt
├── .env
├── README.md
│
├── services/
│   ├── gemini_client.py
│   └── system_design_service.py
│
├── templates/
│   ├── dashboard.html
│   ├── requirements.html
│   ├── architecture.html
│   ├── database.html
│   └── critique.html
│
└── static/
    ├── css/
    └── js/
```

> API keys and other sensitive configuration values are stored using environment variables and are not included in the repository.

---

## 🔄 Application Flow

### Step 1 — Enter Requirement

The user enters a natural-language description of the software system.

### Step 2 — AI Analysis

The requirement is sent to the AI service for structured analysis.

### Step 3 — Requirements Generation

The AI identifies functional requirements, non-functional requirements, actors, and constraints.

### Step 4 — Architecture Generation

The AI proposes an architecture suitable for the given requirements.

### Step 5 — Database Generation

The AI identifies the required entities, attributes, keys, and relationships.

### Step 6 — AI Critique

The generated design is reviewed to identify possible problems and improvements.

---

## 🧪 Example

### Input

```text
Design an online food delivery application where customers
can browse restaurants, order food, make payments and track
their deliveries.
```

### Generated Output

The system can produce:

```text
Requirements
├── Functional Requirements
├── Non-Functional Requirements
├── Actors
└── Constraints

Architecture
├── User Interface
├── Backend Services
├── Authentication
├── Restaurant Management
├── Order Management
├── Payment Service
└── Delivery Tracking

Database
├── Users
├── Restaurants
├── Menu Items
├── Orders
├── Order Items
├── Payments
└── Deliveries

AI Critique
├── Potential Issues
├── Missing Requirements
├── Design Concerns
└── Suggested Improvements
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Bojamma-06/AI-System-Design-Assistant.git
```

### 2. Navigate to the Project

```bash
cd AI-System-Design-Assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### 6. Run the Application

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

---

## ☁️ Deployment

The application can be deployed using **Render**.

The deployment uses the GitHub repository as the source.

When changes are pushed to the `main` branch, the Render service can automatically build and deploy the latest version.

Environment variables such as the Gemini API key should be configured directly in the Render dashboard rather than committed to GitHub.

---

## 🔐 Security

Sensitive credentials are not stored directly in the source code.

The application uses environment variables for API credentials.

```text
.env
   ↓
Environment Variable
   ↓
Gemini Client
   ↓
Gemini API
```

The `.env` file should never be committed to the public repository.

---

## 🎓 Project Purpose

This project was developed as an academic/portfolio project to explore the use of **Generative AI in software engineering and system design**.

It demonstrates how AI can assist with early-stage software development tasks such as:

* Requirement analysis
* Architecture planning
* Database modeling
* Design review

---

## 🔮 Future Enhancements

Possible future improvements include:

* 📊 Automatic architecture diagrams
* 🔄 Export system designs as PDF
* 📝 Export generated requirements
* 🗃️ SQL schema generation
* 🔐 User authentication
* 💾 Saving previous system designs
* 📐 UML diagram generation
* 🤖 Multi-agent design workflow
* ⚡ Streaming AI responses
* 📈 Improved scalability and caching

---

## 👩‍💻 Author

**Bojamma K M**

B.E. Computer Science & Engineering
Vidyavardhaka College of Engineering, Mysuru

GitHub:
https://github.com/Bojamma-06

---

## ⭐ Acknowledgement

This project uses Generative AI technology to assist with software system design and demonstrates the practical application of AI in software engineering.
