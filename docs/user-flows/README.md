# User Flows

## Registration

![diagram of request access Registration flow](flow_1_register.svg)

## Item into Collection

![diagram of request access Item into Collection flow](flow_2_item_into_collection.svg)

## Request Access Workflow

_Purpose:_ The library also plans to engage with community elders in order to assess the collections and receive community input on how the data is to be managed. The web application must, therefore, limit access to collections until appropriate parties have determined that a particular item in the collection can be publicly released or kept private. This is the most critical feature to meet client requirements.

1. **Public User submits request** → Views restricted item and clicks "Request Access"
2. **Item transitions** → Access status changes to "Under Review"
3. **Reviewer assesses** → Community Reviewer/Admin reviews item and comments on cultural appropriateness
4. **Decision recorded** → Reviewer approves or rejects with documented reasoning
5. **Status updated** → Item access level changes to Public (approved) or remains Restricted (rejected)
6. **Audit trail maintained** → All decisions stored in database with timestamp and reviewer details

![diagram of request access user flow](flow_3_request_access.svg)
