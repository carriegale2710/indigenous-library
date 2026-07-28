# Flask application routes & permissions

## Role Permissions

| Role                   | Permissions                                                                                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Admin**              | Full system access • Create/edit/delete items • Assign user roles • View & manage all requests • Approve/reject access • Modify metadata            |
| **Community Reviewer** | View items under review • Add discussion comments • Approve/reject access requests • Update cultural metadata • Cannot delete items or manage users |
| **Library Staff**      | Create & edit collection items • Upload images and metadata • View access requests • Cannot finalize decisions unless assigned reviewer role        |
| **Public User**        | Browse public items • View item details • Submit access requests for restricted items • Cannot edit items or access assessment pages                |

---

## CRUD Endpoints / Flask Routes

### **Home & Browsing**

| Endpoint          | Description                                                              | Access Level |
| ----------------- | ------------------------------------------------------------------------ | ------------ |
| `/`               | Home page with featured items                                            | Public       |
| `/catalogue`      | Browse all items with search and filtering by category, type, and status | Public       |
| `/access-privacy` | Access and privacy notice                                                | Public       |
| `/auth/register`  | User registration                                                        | Public       |
| `/auth/login`     | User login                                                               | Public       |
| `/auth/logout`    | User logout                                                              | Logged-in    |

### **Item Management**

| Endpoint               | Description                    | Access Level         |
| ---------------------- | ------------------------------ | -------------------- |
| `/item-details/<id>`   | View item details and metadata | Public               |
| `/items/<id>/edit`     | Edit item details              | Admin, Library Staff |
| `/items/<id>/delete`   | Delete item                    | Admin                |
| `/items/<id>/metadata` | Update cultural metadata       | Reviewers, Admin     |

### **Access Requests & Assessment**

| Endpoint                                  | Description                                | Access Level                    |
| ----------------------------------------- | ------------------------------------------ | ------------------------------- |
| `/items/<id>/request`                     | Submit access request for restricted items | Logged-in                       |
| `/items/assessment/<id>`                  | View and assess item with pending requests | Reviewers, Admin, Library Staff |
| `/items/assessment/<request_id>/comment`  | Add discussion comment to request          | Reviewers, Admin                |
| `/items/assessment/<request_id>/decision` | Record approval/rejection decision         | Reviewers, Admin                |

### **Demo-Only Endpoints**

| Endpoint            | Description                                                            | Access Level                      |
| ------------------- | ---------------------------------------------------------------------- | --------------------------------- |
| `/auth/demo-login`  | One-click login as the shared demo admin account, no password required | Public                            |
| `/admin/reset-demo` | Truncates and reseeds demo-writable tables back to the original state  | Secret key (`X-Reset-Key` header) |
