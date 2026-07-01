"""
ITEM ASSESSSMENT PAGE

Displays full item metadata and features for item assessment, community comments, access requests and review decisions between authorised users. Restricted Access.

This page must:

- [t] be accessible only to authorised roles (e.g. Admin, Community Reviewer/Elder)
- [t] display full item metadata, including cultural notes and access history
- [ ] allow authorised reviewers to add:
    - [ ] discussion comments
    - [t] update cultural metadata
    - [ ] approve or reject access.
    - [ ] dynamically update the item’s access status in the database
    - [ ] record review decisions, reviewer identity, and timestamp for audit purposes.

The system must implement the following workflow:

1. [t] A Public User submits an access request.
2. [ ] The item may transition to 'Under Review'.
3. [ ] A Community Reviewer or Admin records a decision (Approved/Rejected).
4. [ ] The item’s access status is updated accordingly.
5. [ ] All decisions are stored in the database.

Check:
- [ ] Items must not change access status without a recorded review decision.
- [ ] Users without appropriate permissions must not be able to access this page, including via direct URL manipulation.

"""
from flask import Blueprint, render_template, redirect, flash, url_for, abort, session, g

from project.model import User, CollectionItem, CulturalMetadata, AccessStatus, AccessRequest, CommunityComment, ReviewDecision
from project.forms import CommunityCommentForm, ReviewDecisionForm
from project.decorators import login_required, role_required

assessment_bp = Blueprint('assessment',__name__) 

@assessment_bp.route("/items/<int:item_id>", methods=["GET", "POST"])
@login_required
@role_required(1,2) # Admin and Community Elder access only
def item_assessment(item_id): #REVIEW
    """
    View to display item details and metadata including: cultural notes, access requests, review decision history.
    Only accessible by Admin, Community Reviewer/Elder roles. Users without appropriate permissions must not be able to access this page, including via direct URL manipulation.
    Access status should be dynamically updated upon access request approvals.

    """
    
    item = CollectionItem.get_by_id(item_id) 
    if item is None:
        abort(404)
    metadata = CulturalMetadata.get_by_item(item_id) 

    access_request = AccessRequest.get_by_id(item_id) # ('request summary' in html)
    access_status = AccessStatus.get_by_id(item['statusID'])

    if access_request is None:
        access_request_submitter = []
        access_request_comments = []
        review_decision_history = []
    else:
        access_request_comments = CommunityComment.get_by_request(access_request['requestID']) # ('consultation comments'in html)
        review_decision_history = ReviewDecision.get_by_request(access_request['requestID']) # ('assessment history' in html)
        access_request_submitter = User.get_by_id(access_request['userID']) 

        for comment in access_request_comments:
            user = User.get_by_id(comment['reviewerID'])
            comment['fullName'] = user['fullName']
            comment['username'] = user['fullname']

    form = CommunityCommentForm() # for add_comment feature

    return render_template(
        "item-assessment.html",
        item=item,
        metadata=metadata,
        access_status=access_status,
        access_request=access_request,
        access_request_submitter=access_request_submitter,
        access_request_comments=access_request_comments,
        review_decision_history=review_decision_history,
        form=form
    )


@assessment_bp.route('/items/<int:request_id>/comment', methods=['GET', 'POST'])
@login_required
@role_required(1,2) # Admin and Community Elder access only
def add_comment(request_id): #REVIEW - comment form renders in item-assessment.html
    """
    A reviewer's note on a request. Several reviewers can comment on one. 
    Uses CommunityComment WTForm.
    """
    request_obj = AccessRequest.get_by_id(request_id)
    if request_obj is None:
        abort(404)

    itemid = request_obj['itemID']
    item = CollectionItem.get_by_id(itemid)
    if item is None:
        abort(404)

    form = CommunityCommentForm()

    if form.validate_on_submit():
        reviewerID = session["userID"]
        commentText = form.commentText.data
        CommunityComment.add_comment(request_id, reviewerID, commentText)
        flash("Your community comment has been submitted", "success")
        return redirect(url_for("assessment.itemassessment", itemid=itemid))

    flash("Your community comment could not be submitted. Please try again", "danger")
    return render_template(
        "item-assessment.html",
        item=item,
        request=request_obj,
        form=form,
    )


@assessment_bp.route('/items/<int:request_id>/decision', methods=['GET', 'POST'])
@login_required
@role_required(1,2) # Admin and Community Elder access only
def save_review_decision(request_id): #REVIEW
    """
    Uses ReviewDecision WTForm.
    A reviewer's ruling on a request. This is the AUDIT record: reviewerID and
    decisionDate are who decided and when.
    """
    request = AccessRequest.get_by_id(request_id)
    if request is None:
        abort(404)

    item_id=request['itemID']
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        abort(404)

    form = ReviewDecisionForm()

    if form.validate_on_submit():
        reviewerID = session['userID']
        decisionType = form.decisionType.data
        decisionNotes = form.decisionNotes.data
        accessConditions = form.accessConditions.data
        ReviewDecision.create(request_id, reviewerID, decisionType, decisionNotes, accessConditions)
        flash('Your review decision has been submitted', 'success')
        return redirect(url_for('item_assessment.html', item_id))

    flash('Your review decision could not be submitted. Please try again', 'danger')
    return render_template("review-decision-form.html", item=item, request=request, form=form) #REVIEW create review-decision-form.html
