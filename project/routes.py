"""CRUD Functionality
- The System must support:
> Create, Read, Update, Delete Operations for collection items
> Submission of access requests
> Recording of review decisions
> Status transitions (Under Review -> Public/Restricted)

All CRUD operations must interact dynamically with the database and respect role permissions. """

from flask import Blueprint, render_template, redirect, flash, url_for, session

from project.model import CollectionItem, AccessRequest, CulturalMetadata, Collection
from project.forms import AccessRequestForm, CollectionItemForm, CulturalMetadataForm
from project.decorators import login_required, role_required

items_bp = Blueprint('items_bp', __name__)


@items_bp.route('/items/<int:item_id>/request', methods=['GET', 'POST'])
@login_required                 #Any Logged in user can submit
def request_access(item_id):
    """
    Displays AccessRequestForm to allow a Public User to submit an access request to a restricted item.
    """
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        return render_template("error.html", error_code=404)

    form = AccessRequestForm()

    if form.validate_on_submit():
        userID = session['userID']
        requestReason = form.requestReason.data
        supportingDocuments = form.supportingDocuments.data
        AccessRequest.create(userID, item_id, requestReason, supportingDocuments)
        flash('Your access request has been submitted', 'success')
        return redirect(url_for('items_bp.request_access', item_id=item_id))

    return render_template("request-form.html", item=item, form=form)


@items_bp.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
@role_required(1,3)        #Admin and Library Staff Only
def collection_item_update(item_id):
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        return render_template("error.html", error_code=404)

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


@items_bp.route('/items/<int:item_id>/delete', methods=['POST'])
@role_required(1,3)         # Admin and Library Staff only
def collection_item_delete(item_id):
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        return render_template("error.html", error_code=404)
    CollectionItem.delete(item_id)
    flash('Your collection item has been deleted', 'success')
    return redirect(url_for('views.home'))


@items_bp.route('/items/<int:item_id>/metadata', methods=['GET', 'POST'])
@role_required(1,2)             # Admin and Community Reviewer/Elder only

def cultural_metadata(item_id):
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        return render_template("error.html", error_code=404)

    metadata = CulturalMetadata.get_by_item(item_id)

    if metadata:
        form = CulturalMetadataForm(
            communityGroup=metadata['communityGroup'],
            language=metadata['language'],
            location=metadata['location'],
            subjectArea=metadata['subjectArea'],
            culturalSensitivityNotes=metadata['culturalSensitivityNotes'],
            culturalProtocolNotes=metadata['culturalProtocolNotes'],
            accessRecommendations=metadata['accessRecommendations']
        )
    else:
        form = CulturalMetadataForm()

    if form.validate_on_submit():
        if metadata is None:
            CulturalMetadata.create(
                itemID=item_id,
                communityGroup=form.communityGroup.data,
                language=form.language.data,
                location=form.location.data,
                subjectArea=form.subjectArea.data,
                culturalSensitivityNotes=form.culturalSensitivityNotes.data,
                culturalProtocolNotes=form.culturalProtocolNotes.data,
                accessRecommendations=form.accessRecommendations.data
            )
        else:
            CulturalMetadata.update(
                item_id,
                communityGroup=form.communityGroup.data,
                language=form.language.data,
                location=form.location.data,
                subjectArea=form.subjectArea.data,
                culturalSensitivityNotes=form.culturalSensitivityNotes.data,
                culturalProtocolNotes=form.culturalProtocolNotes.data,
                accessRecommendations=form.accessRecommendations.data
            )
        flash('Cultural metadata saved successfully.', 'success')
        return redirect(url_for('views.item_details', item_id=item_id))

    return render_template("cultural-metadata-form.html", item=item, metadata=metadata, form=form)