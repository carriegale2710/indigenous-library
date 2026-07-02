from flask import Blueprint, render_template, redirect, flash, abort, url_for, session, request
from MySQLdb import IntegrityError
from project.model import CollectionItem, Collection, AccessRequest
from project.decorators import login_required, role_required
from project.forms import AccessRequestForm, CollectionItemForm

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
    if items is None:
        abort(500)
    if not items:
        flash("No items found matching your search criteria.", "info")

    # itemType isn't a model filter, and the DB stores it lowercase
    if item_type and item_type != "All item types":
        items = [item for item in items if item["itemType"].lower() == item_type.lower()]

    return render_template("catalogue.html", items=items)


@views_bp.route("/item-details/<int:item_id>", methods=["GET", "POST"])
def item_details(item_id):
    """
    Display information to user about an item.

    The item details page displays: Title, Image (if applicable), Description (including cultural metadata and access notes) and Current access status (Public / Restricted / Under Review).

    The page :
    - [x] allows Public Users to submit an access request for restricted items
    - [x] validates all form inputs and provide clear feedback for invalid submissions
    - [x] prevents unauthorised actions based on user role, including access restricted data by manipulating URLs.
    
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

@views_bp.route("/access-privacy")
def access_privacy():
    """
    Displays access privacy notice to users.
    """
    return render_template("access-privacy.html")

@views_bp.route('/items/<int:item_id>/request', methods=['GET', 'POST'])
@login_required                 #Any Logged in user can submit
def request_access(item_id):
    """
    Displays AccessRequestForm to allow a Public User to submit an access request to a restricted item.
    """
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        abort(500)

    # Check they haven't already made a request for this item
    user_id = session.get("userID") 
    if user_id:
        for req in AccessRequest.get_by_user(user_id):
            if req["itemID"] == item_id:
                flash("You have already made a request for this item.")
                return redirect(url_for('views.item_details', item_id=item_id))
    
    form = AccessRequestForm()

    if form.validate_on_submit():
        userID = session['userID']
        requestReason = form.requestReason.data
        # MVP NOTE: supportingDocuments is a FileField so the form correctly
        # prompts the user to upload a file. However, this MVP does not implement
        # file storage (saving to disk/cloud, generating a unique filename,
        # storing the file path in the database). Currently we only capture the
        # filename for record-keeping, not the file content itself.
        # If operational: the uploaded file would be saved to a dedicated
        # uploads folder, the file path stored in AccessRequest.supportingDocuments,
        # and a download link surfaced on the assessment page for reviewers.
        supportingDocuments = form.supportingDocuments.data

        try:
            AccessRequest.create(userID, item_id, requestReason, supportingDocuments)
            CollectionItem.update_status(item_id, 4)  # Update item status to 'Pending' when a new access request is submitted
            flash('Your access request has been submitted', 'success')
        
        except IntegrityError:
            from project import mysql
            mysql.connection.rollback()
            flash("Database Integrity error.")
        
        finally:
            return redirect(url_for('views.item_details', item_id=item_id))

    return render_template("request-form.html", item=item, form=form)

@views_bp.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
@role_required(1,3)        #Admin and Library Staff Only
def collection_item_update(item_id):
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        abort(404)

    collections = Collection.get_all()
    collection_choices = [(str(c['collectionID']), c['collectionName']) for c in collections]

    form = CollectionItemForm(
        title=item['title'],
        authorCreator=item['authorCreator'],
        year=item['year'],
        summary=item['summary'],
        collection=item['collectionID'],
        itemType=item['itemType'],
        thumbnailPath=item['thumbnailPath'],
        nextReviewDate=item['nextReviewDate']
    )
    form.collection.choices = collection_choices

    if form.validate_on_submit():
        CollectionItem.update(
            item_id,
            title=form.title.data,
            authorCreator=form.authorCreator.data,
            summary=form.summary.data,
            collectionID=form.collection.data,
            year=form.year.data,
            itemType=form.itemType.data,
            thumbnailPath=form.thumbnailPath.data,
            nextReviewDate=form.nextReviewDate.data
        )
        flash('Item updated successfully', 'success')
        return redirect(url_for('views.item_details', item_id=item_id))

    return render_template("collection-item-form.html", item=item, form=form)

@views_bp.route('/items/<int:item_id>/delete', methods=['POST'])
@role_required(1)         # Admin only 
def collection_item_delete(item_id):

    
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        abort(500)

    CollectionItem.delete(item_id)
    flash('Your collection item has been deleted', 'success')

    return redirect(url_for('views.home'))

# CollectionItem.create — OUT OF SCOPE for MVP.
# Assumption: all catalogue items pre-exist in the database for MVP demo purposes
# Phase 2: Admin and Library Staff would use CollectionItemForm to add new items directly
# from the routes layer. The model method (CollectionItem.create) already exists
# and defaults new items to statusID 4 (Pending) — this aligns with CARE's
# Authority to Control, ensuring no item is publicly visible/classified until
# a Community Elder has reviewed and set its access status.


# ---------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------

@views_bp.app_errorhandler(403)
def forbidden(error):
    return render_template(
        "error.html",
        error_code=403,
        error_title="Access Forbidden",
        error_message="You do not have permission to access this page.",
        error_description="This area may be restricted to authorised library staff, administrators, or community reviewers."
    ), 403


@views_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        error_code=404,
        error_title="Page Not Found",
        error_message="The page you are looking for could not be found.",
        error_description="The link may be incorrect, the page may have moved, or the item may no longer be available."
    ), 404


@views_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template(
        "error.html",
        error_code=500,
        error_title="Internal Server Error",
        error_message="Something went wrong while processing your request.",
        error_description="Please try again later or contact library staff if the problem continues."
    ), 500


@views_bp.app_errorhandler(IntegrityError)
def handle_integrity_error(error):
    try:
        # If you have a shared connection/session, rollback it here.
        from project import mysql
        mysql.connection.rollback()
        pass
    except Exception:
        pass

    flash("That action could not be completed because it would create invalid or duplicate data.", "error")
    return redirect(request.referrer or url_for("views.home"))