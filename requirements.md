# Part A - Web application code requirements

This document sets out the required pages and features, together with the detailed functional, technical, and submission requirements for Part A: Web application code.

> Note to team: Use this as a source of truth on what requirements have been met by the code so far. Each time before you commit any code, go here and check off what you did. This makes it a living document and keeps us on track with assignment criteria.

Your team must complete the following:

## 1. Core Functional Pages

You must include a home page, items details page, and item assessment page (restricted access). See the following details of what to include in each.

### Home Page

Your home page must:

- [X] dynamically display collection items from the database
- [X] support search and filtering (e.g. by category, cultural group, access level, keyword)
- [X] handle empty result scenarios gracefully (e.g. 'No items found')
- [X] include a functional navigation bar and footer on all pages
- [ ] be fully responsive across desktop, tablet, and mobile devices.

Collection items may include (but are not limited to):

- [X] Historical photographs
- [X] Audio recordings of oral histories
- [X] Archival manuscripts or documents
- [X] Artwork created by Indigenous artists
- [X] Cultural artefact records
- [X] Language preservation materials

Each item must include appropriate cultural metadata such as cultural group, sensitivity notes, review status, and access level.

### Item Details Page

The item details page must display:

- [X] Title
- [X] Image (if applicable)
- [X] Description, including cultural metadata and access notes
- [X] Current access status (Public / Restricted / Culturally Sensitive)

The page must:

- [x] allow Public Users to submit an access request for restricted items
- [x] validate all form inputs and provide clear feedback for invalid submissions
- [x] prevent unauthorised actions based on user role.

Users must not be able to access restricted data by manipulating URLs.

### Item Assessment Page (Restricted aCcess)

- [x] Items must not change access status without a recorded review decision.
- [x] Users without appropriate permissions must not be able to access this page, including via direct URL manipulation.

This page must:

- [x] be accessible only to authorised roles (e.g. Admin, Community Reviewer/Elder)
- [x] display full item metadata, including cultural notes and access history
- [ ] allow authorised reviewers to add:
  - [x] discussion comments
  - [x] update cultural metadata
  - [ ] approve or reject access.
  - [ ] dynamically update the item’s access status in the database
  - [ ] record review decisions, reviewer identity, and timestamp for audit purposes.

The system must implement the following workflow:

1. [ ] A Public User submits an access request.
2. [ ] The item may transition to 'Under Review'.
3. [ ] A Community Reviewer or Admin records a decision (Approved/Rejected).
4. [ ] The item’s access status is updated accordingly.
5. [ ] All decisions are stored in the database.

## 2. Authentication and Access Controls

Your application must implement a complete user authentication system, including:

- [ ] Registration
- [ ] Login/Logout
- [ ] Hashed passwords
- [ ] Session-based authentication

Role Permissions

- [ ] Users must not be able to access, modify, or manipulate data outside their assigned role permissions.
- [ ] Access control must be enforced at the route level using custom decorators (e.g., @admin_required) or Flask-Login session-based role checks.
- [ ] Unauthorised access attempts must be handled gracefully (e.g., redirect to login or show an appropriate error page).

> Do not use Flask-Admin.

You must include the following roles and enforced permissions:

1. Admin

- [ ] Full system access.
- [ ] Create, edit, and delete collection items.
- [ ] Assign roles to users.
- [ ] View and manage all access requests.
- [ ] Participate in review decisions.
- [ ] Modify metadata and access status.

2. Community Reviewer/Elder

- [ ] View items under review.
- [ ] Add comments.
- [ ] Approve or reject access.
- [ ] Update cultural metadata.
- [ ] Cannot delete items or manage users.

3. Library Staff

- [ ] Create and edit collection items.
- [ ] Upload images and metadata.
- [ ] View access requests.
- [ ] Cannot finalise review decisions unless assigned reviewer role.

4. Public User

- [ ] Browse publicly available items
- [ ] View item details.
- [ ] Submit access requests.
- [ ] Cannot edit items or access assessment pages.

## 3. CRUD Functionality

The system must support:

- [ ] Create, Read, Update, Delete operations for collection items
- [ ] Metadata updates
- [ ] Submission of access requests
- [ ] Recording of review decisions
- [ ] Status transitions (Under Review → Public/Restricted)

All CRUD operations must interact dynamically with the database and respect role permissions.

## 4. Database Integration

The application must be built on your Assignment 1 data model (with refinements if necessary). The database schema must logically reflect the entities and relationships identified in Assignment 1.

Minimum dataset requirements:

- [ ] At least 15 collection items across multiple categories.
- [ ] At least 6 users distributed across roles (minimum 1 per role).
- [ ] At least 3 completed review decisions.
- [ ] At least 3 access requests recorded. All database tables must remain in Third Normal Form (3NF).

The submitted database.sql file must be pre-populated and runnable.

## 5. Error Handling

- [ ] Use an error.html template.
- [ ] Flask @app.errorhandler should manage redirection and display.
- [ ] Default Flask error pages must not be shown.
- [ ] Handle and display custom error pages for at least:
  - [ ] 404 Not Found page.
  - [ ] 500 Internal Server Error page.

## 6. Professional User Interface

Your application must:

- [ ] include consistent navigation and footer on all pages
- [ ] maintain clear spacing and alignment
- [ ] avoid broken layouts or overlapping elements
- [ ] have a consistent colour scheme, fonts, and layout
- [ ] be responsive across screen sizes
- [ ] use custom CSS refinements beyond default Bootstrap
- [ ] ensure all forms include validation and clear feedback messages.

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

- [ ] The database must be pre-populated.
- [ ] The project must run locally. 
- [ ] app.debug must be set to False .
- [ ] You must include a README.txt with instructions for running the project locally.
- [ ] Exclude any virtual environments and external dependencies from submission.
- [ ] There is no word limit.
- [ ] There is no minimum or maximum line-of-code requirement; however, the application must fully meet all functional requirements. 

### Tools and Requirements

The following tools and resources are permitted:

#### Frameworks

> IMPORTANT: Use of high-level frameworks, automation tools, or alternative libraries, including **Flask-Admin, Django**, or similar, is **strictly prohibited**.

- [ ] You must use only the frameworks and libraries taught and discussed in collab sessions, or explicitly permitted, such as:
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

- [ ] Use only HTML and CSS, including Bootstrap 5.3.
