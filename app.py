from flask import Flask, render_template, abort, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.secret_key = "temporary-dev-key"


# ---------------------------------------------------------
# Temporary WTForms class for request-form.html
# Later, this can be moved into a separate forms.py file.
# ---------------------------------------------------------
class AccessRequestForm(FlaskForm):
    requestReason = TextAreaField("Reason for Request", validators=[DataRequired()])
    supportingDocuments = FileField("Supporting Documents")
    submit = SubmitField("Submit Request")


# ---------------------------------------------------------
# Temporary catalogue data
# Later, this will be replaced with MySQL queries.
# ---------------------------------------------------------
def get_sample_items():
    return [
        {
            "itemID": 1,
            "title": "Kalaw Lagaw Ya Dictionary",
            "summary": "A community dictionary of the Kalaw Lagaw Ya language.",
            "year": 2018,
            "thumbnailPath": "kalaw-lagaw-ya-dictionary.svg",
            "itemType": "Book",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Torres Strait Language Collection",
            "authorCreator": "Community language contributors",
            "nextReviewDate": None
        },
        {
            "itemID": 2,
            "title": "Recordings of Meriam Mir Speakers",
            "summary": "Audio recordings of fluent Meriam Mir speakers.",
            "year": 2005,
            "thumbnailPath": "recordings-of-meriam-mir-speakers.svg",
            "itemType": "Recording",
            "statusName": "Restricted",
            "statusDescription": "Community review required",
            "collectionName": "Torres Strait Language Collection",
            "authorCreator": "Community speakers and library field researcher",
            "nextReviewDate": "2026-05-18"
        },
        {
            "itemID": 3,
            "title": "Creation Songline of the Seven Sisters",
            "summary": "A recorded songline shared under cultural protocol.",
            "year": 1998,
            "thumbnailPath": "creation-songline-of-the-seven-sisters.svg",
            "itemType": "Recording",
            "statusName": "Restricted",
            "statusDescription": "Staff and community review required",
            "collectionName": "Cultural Knowledge Collection",
            "authorCreator": "Community knowledge holders",
            "nextReviewDate": None
        },
        {
            "itemID": 4,
            "title": "Oral History: Mission Days",
            "summary": "Interviews recalling life on the missions.",
            "year": 2010,
            "thumbnailPath": "oral-history-mission-days.svg",
            "itemType": "Recording",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Cultural Knowledge Collection",
            "authorCreator": "Oral history contributors",
            "nextReviewDate": None
        },
        {
            "itemID": 5,
            "title": "Weaving Patterns of the Yolngu",
            "summary": "Photographs documenting traditional weaving patterns.",
            "year": 2015,
            "thumbnailPath": "weaving-patterns-of-the-yolngu.svg",
            "itemType": "Image",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Visual Culture Collection",
            "authorCreator": "Library visual culture team",
            "nextReviewDate": None
        },
        {
            "itemID": 6,
            "title": "Ceremony Photographs Collection",
            "summary": "A restricted set of ceremony photographs.",
            "year": 1972,
            "thumbnailPath": "ceremony-photographs-collection.svg",
            "itemType": "Image",
            "statusName": "Restricted",
            "statusDescription": "Community permission required",
            "collectionName": "Visual Culture Collection",
            "authorCreator": "Unknown photographer",
            "nextReviewDate": None
        },
        {
            "itemID": 7,
            "title": "Children's Picture Book in Yumplatok",
            "summary": "An illustrated children's book in Yumplatok, also known as Torres Strait Creole.",
            "year": 2020,
            "thumbnailPath": "childrens-picture-book-in-yumplatok.svg",
            "itemType": "Book",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Torres Strait Language Collection",
            "authorCreator": "Community education team",
            "nextReviewDate": None
        },
        {
            "itemID": 8,
            "title": "Men's Business Recordings",
            "summary": "Restricted recordings held under cultural protocol.",
            "year": 1985,
            "thumbnailPath": "mens-business-recordings.svg",
            "itemType": "Recording",
            "statusName": "Restricted",
            "statusDescription": "Restricted cultural protocol applies",
            "collectionName": "Cultural Knowledge Collection",
            "authorCreator": "Community contributors",
            "nextReviewDate": None
        },
        {
            "itemID": 9,
            "title": "Bark Painting Records",
            "summary": "Catalogue of bark paintings with artist notes.",
            "year": 2012,
            "thumbnailPath": "bark-painting-records.svg",
            "itemType": "Image",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Visual Culture Collection",
            "authorCreator": "Library collection team",
            "nextReviewDate": None
        },
        {
            "itemID": 10,
            "title": "Restricted Ceremony Audio",
            "summary": "Ceremony audio with an access request under assessment.",
            "year": 1990,
            "thumbnailPath": "restricted-ceremony-audio.svg",
            "itemType": "Recording",
            "statusName": "Culturally Sensitive",
            "statusDescription": "Culturally sensitive item under review",
            "collectionName": "Cultural Knowledge Collection",
            "authorCreator": "Community knowledge holders",
            "nextReviewDate": None
        },
        {
            "itemID": 11,
            "title": "Yolngu Matha Language Primer",
            "summary": "An introductory primer for Yolngu Matha.",
            "year": 2017,
            "thumbnailPath": "yolngu-matha-language-primer.svg",
            "itemType": "Book",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Torres Strait Language Collection",
            "authorCreator": "Language education team",
            "nextReviewDate": None
        },
        {
            "itemID": 12,
            "title": "Sacred Site Survey Notes",
            "summary": "Field notes referencing restricted sacred sites.",
            "year": 2003,
            "thumbnailPath": "sacred-site-survey-notes.svg",
            "itemType": "Manuscript",
            "statusName": "Restricted",
            "statusDescription": "Restricted access due to sacred site information",
            "collectionName": "Cultural Knowledge Collection",
            "authorCreator": "Field researcher",
            "nextReviewDate": None
        },
        {
            "itemID": 13,
            "title": "Community Festival Photographs",
            "summary": "Photographs from annual community festivals.",
            "year": 2019,
            "thumbnailPath": "community-festival-photographs.svg",
            "itemType": "Image",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Visual Culture Collection",
            "authorCreator": "Community photographer",
            "nextReviewDate": None
        },
        {
            "itemID": 14,
            "title": "Initiation Recordings",
            "summary": "Initiation recordings with an access request under assessment.",
            "year": 1988,
            "thumbnailPath": "initiation-recordings.svg",
            "itemType": "Recording",
            "statusName": "Culturally Sensitive",
            "statusDescription": "Culturally sensitive item under review",
            "collectionName": "Cultural Knowledge Collection",
            "authorCreator": "Community knowledge holders",
            "nextReviewDate": None
        },
        {
            "itemID": 15,
            "title": "Dreaming Stories Anthology",
            "summary": "A published anthology of Dreaming stories cleared for public access.",
            "year": 2014,
            "thumbnailPath": "dreaming-stories-anthology.svg",
            "itemType": "Book",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Cultural Knowledge Collection",
            "authorCreator": "Published anthology contributors",
            "nextReviewDate": None
        },
        {
            "itemID": 16,
            "title": "Seasonal Plant Knowledge Cards",
            "summary": "Illustrated cards describing traditional plant uses and seasonal gathering calendars.",
            "year": 2021,
            "thumbnailPath": "seasonal-plant-knowledge-cards.svg",
            "itemType": "Resource",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Land and Sea Country Collection",
            "authorCreator": "Community education team",
            "nextReviewDate": None
        },
        {
            "itemID": 17,
            "title": "Healing Practices Recordings",
            "summary": "Recordings of healing practices and plant preparation methods shared under cultural conditions.",
            "year": 1996,
            "thumbnailPath": "healing-practices-recordings.svg",
            "itemType": "Recording",
            "statusName": "Culturally Sensitive",
            "statusDescription": "Culturally sensitive item under review",
            "collectionName": "Land and Sea Country Collection",
            "authorCreator": "Community knowledge holders",
            "nextReviewDate": None
        },
        {
            "itemID": 18,
            "title": "Caring for Sea Country Photo Series",
            "summary": "Photographs documenting sea country management and community-led conservation work.",
            "year": 2022,
            "thumbnailPath": "caring-for-sea-country-photo-series.svg",
            "itemType": "Image",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Land and Sea Country Collection",
            "authorCreator": "Community conservation team",
            "nextReviewDate": None
        },
        {
            "itemID": 19,
            "title": "Land Management Oral Histories",
            "summary": "Interviews with Elders describing traditional land management and fire practices.",
            "year": 2009,
            "thumbnailPath": "land-management-oral-histories.svg",
            "itemType": "Recording",
            "statusName": "Restricted",
            "statusDescription": "Restricted access due to cultural protocol",
            "collectionName": "Land and Sea Country Collection",
            "authorCreator": "Oral history contributors",
            "nextReviewDate": None
        },
        {
            "itemID": 20,
            "title": "Recently Donated Community Recordings",
            "summary": "Newly catalogued recordings awaiting cultural review before an access status is set.",
            "year": 2023,
            "thumbnailPath": "recently-donated-community-recordings.svg",
            "itemType": "Recording",
            "statusName": "Pending",
            "statusDescription": "Awaiting cultural review",
            "collectionName": "Cultural Knowledge Collection",
            "authorCreator": "Community donor",
            "nextReviewDate": None
        },
        {
            "itemID": 21,
            "title": "Uncatalogued Photograph Series",
            "summary": "A set of photographs recently added to the catalogue and awaiting Elder review.",
            "year": None,
            "thumbnailPath": "uncatalogued-item.svg",
            "itemType": "Image",
            "statusName": "Pending",
            "statusDescription": "Awaiting Elder review",
            "collectionName": "Visual Culture Collection",
            "authorCreator": "Unknown",
            "nextReviewDate": None
        }
    ]


def get_item_by_id(item_id):
    for item in get_sample_items():
        if item["itemID"] == item_id:
            return item
    return None


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/catalogue")
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


@app.route("/item-details/<int:item_id>", methods=["GET", "POST"])
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


@app.route("/request-access/<int:item_id>", methods=["GET", "POST"])
def request_access(item_id):
    item = get_item_by_id(item_id)

    if item is None:
        abort(404)

    form = AccessRequestForm()

    if form.validate_on_submit():
        flash("Your access request has been submitted for review.", "success")
        return redirect(url_for("my_access_requests"))

    return render_template("request-form.html", item=item, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")

        session["user_id"] = 1
        session["full_name"] = "Test User"
        session["email"] = email

        flash("Temporary login successful.", "success")
        return redirect(url_for("catalogue"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        flash("Temporary registration submitted successfully.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/my-access-requests")
def my_access_requests():
    access_requests = [
        {
            "itemID": 2,
            "title": "Recordings of Meriam Mir Speakers",
            "itemType": "Restricted audio",
            "requestDate": "12 May 2026",
            "purpose": "PhD research on language revival",
            "requestStatus": "Approved",
            "decisionConditions": "Research use only. No reproduction without further permission. Approved viewing is arranged at the library."
        },
        {
            "itemID": 3,
            "title": "Creation Songline of the Seven Sisters",
            "itemType": "Culturally sensitive",
            "requestDate": "14 May 2026",
            "purpose": "Teaching preparation",
            "requestStatus": "Pending Review",
            "decisionConditions": "Awaiting community consultation."
        },
        {
            "itemID": 6,
            "title": "Ceremony Photographs Collection",
            "itemType": "Restricted image",
            "requestDate": "18 May 2026",
            "purpose": "Community access request",
            "requestStatus": "Rejected",
            "decisionConditions": "Not publicly accessible. Further community permission required."
        }
    ]

    total_requests = len(access_requests)
    pending_requests = sum(
        1 for request_item in access_requests
        if request_item["requestStatus"] == "Pending Review"
    )
    decided_requests = sum(
        1 for request_item in access_requests
        if request_item["requestStatus"] in ["Approved", "Rejected"]
    )

    return render_template(
        "my-access-requests.html",
        access_requests=access_requests,
        total_requests=total_requests,
        pending_requests=pending_requests,
        decided_requests=decided_requests
    )


@app.route("/item-assessment")
def item_assessment():
    return render_template("item-assessment.html")


@app.route("/access-privacy")
def access_privacy():
    return render_template("access-privacy.html")


# ---------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------
@app.errorhandler(403)
def forbidden(error):
    return render_template(
        "error.html",
        error_code=403,
        error_title="Access Forbidden",
        error_message="You do not have permission to access this page.",
        error_description="This area may be restricted to authorised library staff, administrators, or community reviewers."
    ), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        error_code=404,
        error_title="Page Not Found",
        error_message="The page you are looking for could not be found.",
        error_description="The link may be incorrect, the page may have moved, or the item may no longer be available."
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        "error.html",
        error_code=500,
        error_title="Internal Server Error",
        error_message="Something went wrong while processing your request.",
        error_description="Please try again later or contact library staff if the problem continues."
    ), 500


if __name__ == "__main__":
    app.run(debug=True)