# MySQL Database

## Database Schema Design

> See `database.sql` and [EER diagram](EER_diagram.pdf)
> To run model tests, see [tests folder](../tests/README.md)

| Table                | Primary Key  | Foreign Keys                                       | Purpose                                                                                         |
| -------------------- | ------------ | -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Role**             | roleID       | —                                                  | Stores user roles (Admin, Community Reviewer, Library Staff, Public User)                       |
| **User**             | userID       | roleID → Role                                      | Stores user accounts with credentials, roles, and account status                                |
| **Collection**       | collectionID | —                                                  | Organizes collection items into themed groups (Languages, Oral History, Art, etc.)              |
| **CollectionItem**   | itemID       | collectionID → Collection, statusID → AccessStatus | Stores the main collection items with metadata like title, author, year, item type              |
| **AccessStatus**     | statusID     | —                                                  | Defines access levels (Open, Restricted, Culturally Sensitive)                                  |
| **CulturalMetadata** | metadataID   | itemID → CollectionItem (1:1)                      | Stores cultural information for items (community group, language, sensitivity notes, protocols) |
| **AccessRequest**    | requestID    | userID → User, itemID → CollectionItem             | Records user requests for restricted item access with reason and supporting documents           |
| **ReviewDecision**   | decisionID   | requestID → AccessRequest, reviewerID → User       | Records reviewer decisions (Approved/Rejected) with reasoning and access conditions             |
| **CommunityComment** | commentID    | requestID → AccessRequest, reviewerID → User       | Stores discussion comments from reviewers during the assessment workflow                        |

## How to login with different role permissions

The registration feature defaults to making a public user account only. Note that you can login with Admin test account in the live demo on the [login page](https://indigenous-library-ov0s.onrender.com/auth/login) — no password required. However, to access features with different role permissions in localhost, there are two methods:

1. **Create new account:** Go to [auth.py](project/auth.py) and edit `register()` roleID attribute from '4' (Public User) to 1-Admin/2-Staff/3-Community Member. This changes the default roleID given to users upon registration.
2. **Login to existing account from db:** Use the [unhash.sql](db/unhash.sql) file under the 'db' folder to unhash passwords from user accounts in your local `database.sql` in MySQL Workbench. This lets you login with any account in the db. (Demo purposes only)
