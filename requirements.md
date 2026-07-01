# Part A - Web application code requirements

This document sets out the required pages and features, together with the detailed functional, technical, and submission requirements for Part A: Web application code.

> Note to team: Use this as a source of truth on what requirements have been met by the code so far. Each time before you commit any code, go here and check off what you did. This makes it a living document and keeps us on track with assignment criteria.

> 't' means test

Your team must complete the following:

## 1. Core Functional Pages

You must include a home page, items details page, and item assessment page (restricted access). See the following details of what to include in each.

### Home Page

Your home page must:

- [X] dynamically display collection items from the database
- [X] support search and filtering (e.g. by category, cultural group, access level, keyword)
- [ ] handle empty result scenarios gracefully (e.g. 'No items found')
- [X] include a functional navigation bar and footer on all pages
- [X] be fully responsive across desktop, tablet, and mobile devices.

- [X] Collection items may include (but are not limited to):
  - Historical photographs
  - Audio recordings of oral histories
  - Archival manuscripts or documents
  - Artwork created by Indigenous artists
  - Cultural artefact records
  - Language preservation materials

- [x] Each item must include appropriate cultural metadata such as:
  - cultural group
  - sensitivity notes
  - review status
  - access level.

### Item Details Page

The item details page must display:

- [X] Title
- [X] Image (if applicable)
- [X] Description, including cultural metadata and access notes
- [X] Current access status (Public / Restricted / Under Review)

The page must:

- [x] allow Public Users to submit an access request for restricted items
- [t] validate all form inputs and provide clear feedback for invalid submissions
- [t] prevent unauthorised actions based on user role.

- [t] Users must not be able to access restricted data by manipulating URLs.

### Item Assessment Page (Restricted aCcess)

- [X] Items must not change access status without a recorded review decision.
- [X] Users without appropriate permissions must not be able to access this page, including via direct URL manipulation.

This page must:

- [t] be accessible only to authorised roles (e.g. Admin, Community Reviewer/Elder)
- [X] display full item metadata, including cultural notes and access history
- allow authorised reviewers to add:
  - [X] discussion comments
  - [X] update cultural metadata
  - [X] approve or reject access.
  - [X] dynamically update the item’s access status in the database
- [X] record review decisions, reviewer identity, and timestamp for audit purposes.

The system must implement the following workflow:

1. [X] A Public User submits an access request.
2. [X] The item may transition to 'Under Review'.
3. [X] A Community Reviewer or Admin records a decision (Approved/Rejected).
4. [X] The item’s access status is updated accordingly.
5. [X] All decisions are stored in the database.

## 2. Authentication and Access Controls

Your application must implement a complete user authentication system, including:

- [X] Registration
- [X] Login/Logout
- [X] Hashed passwords
- [X] Session-based authentication

Role Permissions

- [X] Users must not be able to access, modify, or manipulate data outside their assigned role permissions.
- [X] Access control must be enforced at the route level using custom decorators (e.g., @admin_required) or Flask-Login session-based role checks.
- [X] Unauthorised access attempts must be handled gracefully (e.g., redirect to login or show an appropriate error page).

> Do not use Flask-Admin.

You must include the following roles and enforced permissions:

1. Admin

- [X] Full system access.
- [t] Create, edit, and delete collection items.
- [ ] Assign roles to users.
- [X] View and manage all access requests.
- [X] Participate in review decisions.
- [X] Modify metadata and access status.

2. Community Reviewer/Elder

- [X] View items under review.
- [X] Add comments.
- [X] Approve or reject access.
- [X] Update cultural metadata.
- [ ] Cannot delete items or manage users.

3. Library Staff

- [X] Create and edit collection items.
- [X] Upload images and metadata.
- [X] View access requests.
- [t] Cannot finalise review decisions unless assigned reviewer role.

4. Public User

- [X] Browse publicly available items
- [X] View item details.
- [X] Submit access requests.
- [X] Cannot edit items or access assessment pages.

## 3. CRUD Functionality

The system must support:

- [t] Create, Read, Update, Delete operations for collection items
- [X] Metadata updates
- [X] Submission of access requests
- [X] Recording of review decisions
- [X] Status transitions (Under Review → Public/Restricted)

- [ ] All CRUD operations must interact dynamically with the database and respect role permissions.

## 4. Database Integration

The application must be built on your Assignment 1 data model (with refinements if necessary). The database schema must logically reflect the entities and relationships identified in Assignment 1.

Minimum dataset requirements:

- [X] At least 15 collection items across multiple categories.
- [X] At least 6 users distributed across roles (minimum 1 per role).
- [X] At least 3 completed review decisions.
- [X] At least 3 access requests recorded. All database tables must remain in Third Normal Form (3NF).

The submitted database.sql file must be pre-populated and runnable.

## 5. Error Handling

- [X] Use an error.html template.
- [X] Flask @app.errorhandler should manage redirection and display.
- [t] Default Flask error pages must not be shown.
- [t] Handle and display custom error pages for at least:
  - [X] 404 Not Found page.
  - [ ] 500 Internal Server Error page.

## 6. Professional User Interface

Your application must:

- [X] include consistent navigation and footer on all pages
- [X] maintain clear spacing and alignment
- [X] avoid broken layouts or overlapping elements
- [X] have a consistent colour scheme, fonts, and layout
- [t] be responsive across screen sizes
- [t] use custom CSS refinements beyond default Bootstrap
- [t] ensure all forms include validation and clear feedback messages.

## 7. Technical Structure and Permitted Tools

Your project must follow the structure below.

Submit one ZIP file containing: 

```
[groupID]_582_A2.zip
├── run.py
├── README.txt
└── project/
    ├── static/
    │   ├── css/
    │   └── img/
    ├── templates/
    ├── forms.py
    ├── models.py
    ├── views.py
    ├── __init__.py
    └── database.sql
```

### Additional Requirements

Additional requirements are:

- [X] The database must be pre-populated.
- [X] The project must run locally. 
- [ ] app.debug must be set to False .
- [X] You must include a README.txt with instructions for running the project locally.
- [ ] Exclude any virtual environments and external dependencies from submission.
- There is no word limit.
- There is no minimum or maximum line-of-code requirement; however, the application must fully meet all functional requirements. 

### Tools and Requirements

The following tools and resources are permitted:

#### Frameworks

> IMPORTANT: Use of high-level frameworks, automation tools, or alternative libraries, including **Flask-Admin, Django**, or similar, is **strictly prohibited**.

- [X] You must use only the frameworks and libraries taught and discussed in collab sessions, or explicitly permitted, such as:
  - Flask
  - Flask-Login
  - Jinja2
  - Flask-WTF
  - WTForms
  - Flask-MySQLdb
  - MySQLClient
  - bootstrap-flask
  - Python standard libraries (e.g., datetime, os, etc).

The complete list of permitted packages is provided in **‘requirements-1.txt’**.

#### Front-End

- [X] Use only HTML and CSS, including Bootstrap 5.3.
