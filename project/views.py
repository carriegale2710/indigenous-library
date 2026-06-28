from flask import Blueprint, render_template, redirect, flash, abort, url_for, session, request
from app import get_item_by_id, get_sample_items # from project.model import CollectionItem, AccessRequest, CulturalMetadata, ReviewDecision, CommunityComment

# Views blueprints are for route for displaying information to the user
views_bp = Blueprint('views',__name__) 

# ---------------------------------------------------------
# Routes 
# ---------------------------------------------------------
# NOTE - All view routes from app.py have been converted into blueprints here

@views_bp.route("/")
def home():
    """
    Entry point for website.
    """
    return render_template("index.html")

@views_bp.route("/catalogue")
def catalogue():
    """
    Displays list of items in a catalogue page.

    The page must:
    - [ ] dynamically display collection items from the database
    - [ ] support search and filtering (e.g. by category, cultural group, access level, keyword)
    - [ ] handle empty result scenarios gracefully (e.g. 'No items found')
    - [ ] include a functional navigation bar and footer on all pages
    - [ ] be fully responsive across desktop, tablet, and mobile devices.
    """
    items = get_sample_items() # TODO - remove hardcoded data for mySQLdb

    # REVIEW - Test this search logic in browser, with mySQLdb - making sure keys match with columns
    search = request.args.get("search", "").strip().lower()
    item_type = request.args.get("item_type", "").strip().lower()
    status = request.args.get("status", "").strip().lower()

    if search:
        items = [
            item for item in items
            if search in item["title"].lower()
            or search in item["summary"].lower()
            or search in item["collectionName"].lower()
            or search in item["itemType"].lower()
            or search in item["statusName"].lower()
        ]

    if item_type and item_type != "all item types":
        items = [
            item for item in items
            if item["itemType"].lower() == item_type
        ]

    if status and status != "all statuses":
        items = [
            item for item in items
            if item["statusName"].lower() == status
        ]

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
    item = get_item_by_id(item_id)

    if item is None:
        abort(404)

    # TODO - remove hardcoded data below once synced to mySQL db

    metadata = {
        "communityGroup": "Torres Strait Islander community",
        "language": "Meriam Mir",
        "location": "Murray Island / Mer Island",
        "subjectArea": "Language, oral history and cultural memory",
        "culturalSensitivityNotes": "This item may contain culturally sensitive language knowledge.",
        "culturalProtocolNotes": "Because the recordings may include culturally sensitive language content and community knowledge, access is restricted until a review has been completed.",
        "accessRecommendations": "Research use only; no reproduction without further permission"
    }

    related_items = [
        related_item for related_item in get_sample_items()
        if related_item["itemID"] != item_id and related_item["collectionName"] == item["collectionName"]
    ][:3]

    existing_request = None

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

