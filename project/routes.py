from flask import Blueprint, render_template, redirect, flash, url_for, session

from project.model import CollectionItem, AccessRequest, CulturalMetadata
from project.forms import AccessRequestForm, CollectionItemForm, CulturalMetadataForm
from project.decorators import login_required

items_bp = Blueprint('items_bp', __name__)


@items_bp.route('/items/<int:item_id>/request', methods=['GET', 'POST'])
@login_required

def request_access(item_id):
    """
    Displays AccessRequestForm to allow a Public User to submit an access request to a resticted item.

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
@login_required

def collection_item_update(item_id):
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        return render_template("error.html", error_code=404)

    form = CollectionItemForm(
        title = item['title'],
        authorCreator = item['authorCreator'],
        year=item['year'],
        summary=item['summary'],
        collection=item['collectionID'],
        itemType=item['itemType'],
        thumbnailPath=item['thumbnailPath'],
        nextReviewDate=item['nextReviewDate']
    )
    if form.validate_on_submit():
        CollectionItem.update(
           item_id,
           title = form.title.data,
           authorCreator = form.authorCreator.data,
           summary = form.summary.data,
           collectionID = form.collection.data,
           year = form.year.data,
           itemType = form.itemType.data,
           thumbnailPath = form.thumbnailPath.data,
           nextReviewDate = form.nextReviewDate.data
        )
        flash('Your collection item has been updated', 'success')
        return redirect(url_for('views.item_details', item_id=item_id))

    return render_template("collection-item-form.html", item=item, form=form)


@items_bp.route('/items/<int:item_id>/delete', methods=['POST'])
@login_required

def collection_item_delete(item_id):
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        return render_template("error.html", error_code=404)
    CollectionItem.delete(item_id)
    flash('Your collection item has been deleted', 'success')
    return redirect(url_for('views.home'))

@items_bp.route('/items/<int:item_id>/metadata', methods=['GET', 'POST'])
@login_required
#TODO: restrict to ADM and CE roles only (Carrie)

def cultural_metadata(item_id):
    metadata = CulturalMetadata.get_by_item(item_id)

    if metadata:
        form = CulturalMetadataForm(
            communityGroup = metadata['communityGroup'],
            language = metadata['language'],
            location = metadata['location'],
            subjectArea = metadata['subjectArea'],
            culturalSensitivityNotes = metadata['culturalSensitivityNotes'],
            culturalProtocolNotes = metadata['culturalProtocolNotes'],
            accessRecommendations = metadata['accessRecommendations'],
        )

    else:
        form = CulturalMetadataForm()

    if form.validate_on_submit():
        if metadata is None:
            CulturalMetadata.create(
                itemID = item_id,
                communityGroup = form.communityGroup.data,
                language = form.language.data,
                location = form.location.data,
                subjectArea = form.subjectArea.data,
                culturalSensitivityNotes = form.culturalSensitivityNotes.data,
                culturalProtocolNotes = form.culturalProtocolNotes.data,
                accessRecommendations = form.accessRecommendations.data,
            )
        else:
            CulturalMetadata.update(
                item_id,
                communityGroup = form.communityGroup.data,
                language = form.language.data,
                location = form.location.data,
                subjectArea = form.subjectArea.data,
                culturalSensitivityNotes = form.culturalSensitivityNotes.data,
                culturalProtocolNotes = form.culturalProtocolNotes.data,
                accessRecommendations = form.accessRecommendations.data,
            )

        flash('Cultural metadata saved successfully.', 'success')
        return redirect(url_for('views.item_details', item_id=item_id))

    return render_template("cultural-metadata-form.html", metadata=metadata, form=form)

