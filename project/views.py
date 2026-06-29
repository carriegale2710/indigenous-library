from flask import Blueprint, render_template, redirect, flash, abort, url_for, session, request
from project.model import CollectionItem, AccessRequest, CulturalMetadata, ReviewDecision, CommunityComment

# Views blueprints are for route for displaying information to the user
views_bp = Blueprint('views',__name__) 

# ---------------------------------------------------------
# Routes 
# ---------------------------------------------------------
# NOTE - All view routes from app.py have been converted into blueprints here

@views_bp.route("/")
def home():
    """Home page. Shows a few featured items pulled from the catalogue."""
    featured_items = CollectionItem.get_featured_items()
    return render_template("index.html", featured_items=featured_items)

@views_bp.route("/catalogue")
def catalogue():
    # read the three filter values from the query string
    search = request.args.get("search", "").strip()
    item_type = request.args.get("item_type", "").strip()
    status = request.args.get("status", "").strip()

    # the dropdown sends a status NAME, but the model filters on statusID
    status_ids = {"Open": 1, "Restricted": 2, "Culturally Sensitive": 3}
    status_id = status_ids.get(status)

    # search and status are filtered in SQL by the model
    items = CollectionItem.get_all(search=search, status_id=status_id)

    # itemType isn't a model filter, and the DB stores it lowercase
    if item_type and item_type != "All item types":
        items = [item for item in items if item["itemType"].lower() == item_type.lower()]

    return render_template("catalogue.html", items=items)

  
@views_bp.route("/item-details/<int:item_id>", methods=["GET", "POST"])
def item_details(item_id):
    """
    Display information to user about an item.

    The item details page must display:
    - [ ] Title
    - [ ] Image (if applicable)
    - [ ] Description, including cultural metadata and access notes
    - [ ] Current access status (Public / Restricted / Under Review)

    The page must:
    - [ ] allow Public Users to submit an access request for restricted items
    - [ ] validate all form inputs and provide clear feedback for invalid submissions
    - [ ] prevent unauthorised actions based on user role.

    - [ ] Users must not be able to access restricted data by manipulating URLs.
    
    """
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        abort(404)


    metadata = item
     

    related_items = [
    other for other in CollectionItem.get_all(collection_id=item["collectionID"])
    if other["itemID"] != item_id
    ][:3]

    existing_request = None
    user_id = session.get("userID")
    if user_id:
        for req in AccessRequest.get_by_user(user_id):
            if req["itemID"] == item_id:
                existing_request = req
                break

    return render_template(
        "item-details.html",
        item=item,
        metadata=metadata,
        related_items=related_items,
        existing_request=existing_request
    )

@views_bp.route("/item-assessment")
def item_assessment():
    """
    Displays full item metadata and features for item assessment, community comments, access requests and review decisions between authorised users. Restricted Access.

    This page must:

    - [ ] be accessible only to authorised roles (e.g. Admin, Community Reviewer/Elder)
    - [ ] display full item metadata, including cultural notes and access history
    - [ ] allow authorised reviewers to add:
    - [ ] discussion comments
    - [ ] update cultural metadata
    - [ ] approve or reject access.
    - [ ] dynamically update the item’s access status in the database
    - [ ] record review decisions, reviewer identity, and timestamp for audit purposes.

    The system must implement the following workflow:

    1. [ ] A Public User submits an access request.
    2. [ ] The item may transition to 'Under Review'.
    3. [ ] A Community Reviewer or Admin records a decision (Approved/Rejected).
    4. [ ] The item’s access status is updated accordingly.
    5. [ ] All decisions are stored in the database.

    - [ ] Items must not change access status without a recorded review decision.
    - [ ] Users without appropriate permissions must not be able to access this page, including via direct URL manipulation.

    """
    # TODO - implement logic

    return render_template("item-assessment.html")

@views_bp.route("/access-privacy")
def access_privacy():
    """
    Displays access privacy notice to users.
    """
    return render_template("access-privacy.html")

