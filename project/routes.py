from flask import Blueprint, render_template
from project.model import CollectionItem
from project.forms import AccessRequestForm
#from project.auth import login_required

items_bp = Blueprint('items_bp', __name__)

#@login_required -- confirm decorator name with Carrie
@items_bp.route('/items/<int:item_id>/request', methods=['GET'])

def request_access(item_id):
    item = CollectionItem.get_by_id(item_id)
    form = AccessRequestForm()
    if item is None:
        return render_template("error.html", error_code=404)
    return render_template("request_form.html", item=item, form=form)
