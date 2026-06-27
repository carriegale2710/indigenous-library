from flask import Blueprint, render_template, redirect, flash, abort, url_for, session, request
from app import get_item_by_id, get_sample_items

views_bp = Blueprint('views',__name__)

# ---------------------------------------------------------
# Routes # TODO - Convert all view routes from app.py into blueprints here
# ---------------------------------------------------------


@views_bp.route("/")
def home():
    return render_template("index.html")


@views_bp.route("/catalogue")
def catalogue():
    items = get_sample_items()

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
    item = get_item_by_id(item_id)

    if item is None:
        abort(404)

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
    return render_template("item-assessment.html")


@views_bp.route("/access-privacy")
def access_privacy():
    return render_template("access-privacy.html")

