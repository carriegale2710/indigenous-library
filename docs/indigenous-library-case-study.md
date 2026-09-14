# CASE STUDY: Indigenous Library

## Quick Facts

- **Role:** Full‑stack developer (primary implementation of backend, database, and core web features)  
- **Project type:** Web application for managing a library of Indigenous resources  
- **Stack:** Python (Flask‑style), SQL database, HTML/CSS/JS front end, deployed via Heroku‑style `Procfile`  
- **Timeline:** Academic/capstone project (single semester; ~10–12 weeks of active development)  
- **Team:** Small student team (you as the main full‑stack contributor)  
- **Impact:** Delivered a working, documented system for cataloguing and discovering Indigenous resources, with authentication, forms, and assessment workflows.

---

## Overview

Indigenous Library is a web application designed to help library staff and users manage and discover a curated collection of Indigenous resources. The system provides authenticated access, structured metadata, and workflows to add, search, and assess resources in a way that reflects the project's cultural and organisational requirements.

As the main full‑stack developer, I implemented the core application: database models, authentication, form handling, views/routes, and deployment configuration, supported by documentation such as a PRD, deployment guide, and design artifacts (mockups, user flows, EER diagram).

---

## Problem

Libraries and similar institutions often struggle to:

- Maintain a **structured, searchable catalogue** of Indigenous resources
- Enforce **access control** so only appropriate users can add or edit content
- Capture **consistent metadata** through well‑designed forms
- Provide **clear workflows** for staff to manage and assess resources

The Indigenous Library project addresses this by building a dedicated system that centralises resource management, enforces roles and permissions, and supports assessment workflows tailored to the domain. The PRD and related docs define these requirements and scope the features needed to meet them.

---

## Process

### Research & Requirements

- Reviewed the **Product Requirements Document** (`docs/prd.md`) to understand user types, core features, and acceptance criteria.
- Examined **user flows** and **mockups** in `docs/` to align implementation with intended UX.
- Studied the **EER diagram** to design a normalized SQL schema supporting resources, users, roles, and assessments.

### Technical Approach

- Chose a **Python/Flask‑style architecture** for rapid iteration and clear separation of concerns (`auth.py`, `forms.py`, `model.py`, `views.py`).
- Designed the database layer in `project/model.py` and supporting DB scripts under `project/db`, following the EER design.
- Implemented **authentication and authorization** using session‑based login and custom decorators to protect routes.
- Built **WTForms‑style forms** in `forms.py` to standardise input for creating/editing resources and assessments.
- Defined **view functions** in `views.py` to handle routes for browsing, searching, and managing resources.
- Added **assessment logic** in `assessment.py` to support domain‑specific evaluation workflows.
- Configured deployment via a `Procfile` and `config.example.py`, with environment‑based settings for database and secrets.

### Key Decisions

- **Monolithic Flask‑style app** over a heavier framework to keep the project simple, understandable, and deployable within a semester timeline.
- **Server‑rendered templates** with a `templates/` and `static/` folder for straightforward HTML/CSS/JS without the overhead of a separate SPA build pipeline.
- **Explicit role checks** via decorators to ensure only authorised users can access admin or assessment features.
- **Comprehensive documentation** (PRD, deploy guide, design artifacts) to demonstrate professional engineering practices and make onboarding/hand‑off easier.

---

## Solution

### System Architecture

The application follows a classic layered structure:

- **Entry point:** `run.py` launches the web server.
- **Application package:** `project/` contains the main codebase.
  - `auth.py` — login, logout, session management.
  - `forms.py` — form classes for resources, users, assessments.
  - `model.py` — SQLAlchemy‑style ORM models reflecting the EER diagram.
  - `views.py` — route handlers for pages and API‑like endpoints.
  - `assessment.py` — business logic for evaluating resources.
  - `decorators.py` — custom decorators for access control.
- **Database:** SQL database with schema defined according to `docs/EER_diagram.pdf`.
- **Front end:** Jinja‑style templates in `project/templates/` with static assets in `project/static/`.
- **Deployment:** Heroku‑style `Procfile` and configuration via `config.example.py` and environment variables.

### Core Features

- **User authentication:** Secure login/logout, session persistence, and role‑based access.
- **Resource management:** Create, read, update, and delete library resources with structured metadata via forms.
- **Search & browse:** Views to list and filter resources by key fields.
- **Assessment workflow:** Logic to assess resources according to domain criteria, stored and linked via the database.
- **Admin capabilities:** Protected routes for managing users and system configuration.

### Visual & Design Artifacts

The repo includes:

- **Mockups** under `docs/mockups/` showing key screens (catalogue, resource detail, forms).
- **User flows** under `docs/user-flows/` describing navigation and task sequences.
- **EER diagram** (`docs/EER_diagram.pdf`) visualising entities and relationships.

These artifacts demonstrate a deliberate design process and provide strong visuals for a portfolio page.

---

## Results

The project delivers concrete, demonstrable outcomes:

- A **working, deployable web application** with authentication, CRUD operations, and assessment workflows.
- A **well‑structured codebase** with clear separation of concerns, making it easy to discuss architecture in interviews.
- **Professional documentation** (PRD, deployment guide, design artifacts) that mirrors real product development practices.
- Evidence of **testing** via a `tests/` directory, indicating attention to reliability and correctness.

For a portfolio aimed at junior/mid full‑stack roles, this project shows I can:

- Design and implement a **relational data model** and wire it into a web app
- Build **auth‑protected features** and role‑based permissions
- Translate **requirements and UX artifacts** into working software
- Configure **deployment** and environment‑based settings

---

## Learnings

Key learnings and reflections from this project include:

- **Early alignment on requirements:** Investing time up front in requirements and data modelling paid off in clearer implementation. In future, I would involve stakeholders even earlier to validate assumptions about workflows and metadata.
- **Balancing scope and simplicity:** A monolithic Flask‑style app was a good fit for a time‑boxed project. Next time, I would modularise earlier (blueprints, separate config modules) to make the codebase easier to scale if the feature set grows.
- **Testing discipline:** With a `tests/` folder already present, a natural next step is to expand coverage (integration tests for auth and assessment flows) and possibly add CI to run tests on each push.
- **Cultural considerations:** For a system centred on Indigenous resources, future iterations could deepen consultation with relevant communities to ensure metadata, access rules, and UX reflect cultural protocols and community expectations.

---

## Visual Asset List

To turn this into a strong portfolio page, include:

1. **Screenshot: Login / Home** — showing authentication and main navigation.  
2. **Screenshot: Resource catalogue** — list view with search/filter.  
3. **Screenshot: Resource detail** — key metadata fields.  
4. **Screenshot: Create/Edit resource form** — demonstrating structured input.  
5. **Screenshot: Assessment view** — if available, showing the assessment workflow.  
6. **Diagram: EER snapshot** — cropped from `docs/EER_diagram.pdf` to illustrate data modelling.  
7. **Mockup vs implementation comparison** — one key screen from `docs/mockups/` alongside the live UI.  
8. **Architecture diagram** — simple block diagram (web server, app layer, DB, auth) for the "Solution" section.

---

## How to Use This Case Study

- Paste this Markdown into your portfolio site (e.g. Next.js, Astro, or a simple static site).
- Replace the "Visual Asset List" items with actual screenshots and diagrams.
- Optionally add a "Tech Stack" badge row and links to the live demo and GitHub repo.
