"""
ITEM ASSESSSMENT PAGE

Displays full item metadata and features for item assessment, community comments, access requests and review decisions between authorised users. Restricted Access.

This page must:

- [X] be accessible only to authorised roles (e.g. Admin, Community Reviewer/Elder)
- [X] display full item metadata, including cultural notes and access history
- [ ] allow authorised reviewers to add:
    - [X] discussion comments
    - [X] update cultural metadata
    - [ ] approve or reject access.
    - [ ] dynamically update the item’s access status in the database
- [X] record review decisions, reviewer identity, and timestamp for audit purposes.

The system must implement the following workflow:

1. [X] A Public User submits an access request.
2. [ ] The item may transition to 'Under Review'.
3. [ ] A Community Reviewer or Admin records a decision (Approved/Rejected).
4. [ ] The item’s access status is updated accordingly.
5. [ ] All decisions are stored in the database.

Check:
- [ ] Items must not change access status without a recorded review decision.
- [X] Users without appropriate permissions must not be able to access this page, including via direct URL manipulation.

"""
from flask import Blueprint, render_template, redirect, flash, url_for, abort, session, g

from project.model import User, CollectionItem, CulturalMetadata, AccessStatus, AccessRequest, CommunityComment, ReviewDecision
from project.forms import CommunityCommentForm, ReviewDecisionForm, CulturalMetadataForm
from project.decorators import login_required, role_required

assessment_bp = Blueprint('assessment',__name__) 

@assessment_bp.route("/items/assessment/<int:item_id>", methods=["GET", "POST"])
@login_required
@role_required(1,2,3) # only accessible by Admin, Community Reviewer/Elder, and Library Staff
def item_assessment(item_id): #REVIEW
    """
    View to display item details and metadata including: cultural notes, access requests, review decision history.
    Only accessible by Admin, Community Reviewer/Elder roles. Users without appropriate permissions must not be able to access this page, including via direct URL manipulation.
    Access status should be dynamically updated upon access request approvals.

    """
    form = CommunityCommentForm() # for add_comment feature
    
    item = CollectionItem.get_by_id(item_id) 
    if item is None:
        abort(500)
    metadata = CulturalMetadata.get_by_item(item_id) 
    access_status = AccessStatus.get_by_id(item['statusID'])
    request_history = AccessRequest.get_all_by_item(item_id) 

    # store comments and decisions for each request
    for req in request_history:
        req['comments'] = CommunityComment.get_by_request(req['requestID'])  
        if req['requestStatus'] != 'Pending':  
            req['decision'] = ReviewDecision.get_by_request(req['requestID'])  # stores userName of reviewer too #FIXME - not fetching anything

    pending_requests = [req for req in request_history if req['requestStatus'] == 'Pending']  # filter for pending requests
    closed_requests = [req for req in request_history if req['requestStatus'] != 'Pending']  # filter for closed requests

    return render_template(
        "item-assessment.html",
        item=item,
        metadata=metadata,
        access_status=access_status ,                                   
        request_history=request_history,
        pending_requests=pending_requests,
        closed_requests=closed_requests,
        form=form
    )


@assessment_bp.route('/items/assessment/<int:request_id>/comment', methods=['GET', 'POST'])
@login_required
@role_required(1,2,3) # Admin, Community Reviewer/Elder, and Library Staff access only
def add_comment(request_id): # Comment form renders in item-assessment.html - no separate template needed
    """
    A reviewer's note on a request. Several reviewers can comment on one. 
    Uses CommunityComment WTForm.
    """
    request_obj = AccessRequest.get_by_id(request_id)
    if request_obj is None:
        abort(500)

    itemid = request_obj['itemID']
    item = CollectionItem.get_by_id(itemid)
    if item is None:
        abort(500)

    form = CommunityCommentForm()

    if form.validate_on_submit():
        reviewerID = session["userID"]
        commentText = form.commentText.data
        CommunityComment.add_comment(request_id, reviewerID, commentText)
        flash("Your community comment has been submitted", "success")
        return redirect(url_for("assessment.item_assessment", item_id=itemid))

    flash("Your community comment could not be submitted. Please try again", "danger")
    return redirect(url_for("assessment.item_assessment", item_id=itemid))


@assessment_bp.route('/items/assessment/<int:request_id>/decision', methods=['GET', 'POST'])
@login_required
@role_required(1,2) # Admin and Community Elder access only
def save_review_decision(request_id): 
    """
    Uses ReviewDecision WTForm.
    A reviewer's ruling on a request. This is the AUDIT record: reviewerID and
    decisionDate are who decided and when.
    """
    request = AccessRequest.get_by_id(request_id)
    if request is None:
        abort(500)

    item_id=request['itemID']
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        abort(500)

    form = ReviewDecisionForm()

    if form.validate_on_submit():
        reviewerID = session['userID']
        decisionType = form.decisionType.data
        decisionNotes = form.decisionNotes.data
        accessConditions = form.accessConditions.data
        ReviewDecision.create(request_id, reviewerID, decisionType, decisionNotes, accessConditions)

        if decisionType == 'Approve':
            AccessRequest.update_status(request_id, 'Approved')  
            CollectionItem.update_status(item_id, 1)  # Update item status to 'Open' only if approved
        else:
            AccessRequest.update_status(request_id, 'Rejected')

        flash('Your review decision has been submitted', 'success')
        return redirect(url_for('assessment.item_assessment', item_id=item_id))

    flash('Your review decision could not be submitted. Please try again', 'danger')
    return render_template("review-decision-form.html", item=item, request=request, form=form) 


@assessment_bp.route('/items/<int:item_id>/metadata', methods=['GET', 'POST'])
@role_required(1,2,3) # Admin, Community Reviewer/Elder, and Library Staff access only
def cultural_metadata(item_id):
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        abort(500)

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


