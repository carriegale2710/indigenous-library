# Database Schema Design

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
