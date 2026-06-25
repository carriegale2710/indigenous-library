from flask import Blueprint, render_template, redirect, flash, url_for, session
from project.model import CollectionItem, AccessRequest
from project.forms import AccessRequestForm
#from project.auth import login_required

items_bp = Blueprint('items_bp', __name__)

#@login_required -- confirm decorator name with Carrie
@items_bp.route('/items/<int:item_id>/request', methods=['GET', 'POST'])

def request_access(item_id):
    item = CollectionItem.get_by_id(item_id)
    if item is None:
        return render_template("error.html", error_code=404)

    form = AccessRequestForm()

    if form.validate_on_submit():
        user_id = session['user_id']
        requestReason = form.requestReason.data
        supportingDocuments = form.supportingDocuments.data
        AccessRequest.create(user_id, item_id, requestReason, supportingDocuments)
        flash('Your access request has been submitted', 'success')
        return redirect(url_for('items_bp.request_access', item_id=item_id))

    return render_template("request_form.html", item=item, form=form)
