from flask import Flask, render_template, abort

app = Flask(__name__)
app.secret_key = "temporary-dev-key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/catalogue")
def catalogue():
    items = [
        {
            "itemID": 1,
            "title": "Recordings of Meriam Mir Speakers",
            "summary": "Audio recordings connected to Meriam Mir language knowledge and Torres Strait Islander cultural memory.",
            "year": 2026,
            "thumbnailPath": "recordings-of-meriam-mir-speakers.svg",
            "itemType": "Recording",
            "statusName": "Restricted",
            "statusDescription": "Community review required",
            "collectionName": "Languages of the Torres Strait",
            "authorCreator": "Community speakers and library field researcher",
            "nextReviewDate": "2026-05-18"
        },
        {
            "itemID": 2,
            "title": "Kalaw Lagaw Ya Dictionary",
            "summary": "Language resource from the Torres Strait collection.",
            "year": 2024,
            "thumbnailPath": "kalaw-lagaw-ya-dictionary.svg",
            "itemType": "Resource",
            "statusName": "Open",
            "statusDescription": "Open access available",
            "collectionName": "Languages of the Torres Strait",
            "authorCreator": "Library language team",
            "nextReviewDate": None
        }
    ]

    return render_template("catalogue.html", items=items)


@app.route("/item-details/<int:item_id>", methods=["GET", "POST"])
def item_details(item_id):
    item = {
        "itemID": item_id,
        "title": "Recordings of Meriam Mir Speakers",
        "summary": "This catalogue record represents a set of audio recordings connected to Meriam Mir language knowledge, Torres Strait Islander cultural memory and community language revival.",
        "year": 2026,
        "thumbnailPath": "recordings-of-meriam-mir-speakers.svg",
        "itemType": "Recording",
        "statusName": "Restricted",
        "statusDescription": "Community review required",
        "collectionName": "Languages of the Torres Strait",
        "authorCreator": "Community speakers and library field researcher",
        "nextReviewDate": "2026-05-18"
    }

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

    related_items = []
    existing_request = None

    return render_template(
        "item-details.html",
        item=item,
        metadata=metadata,
        related_items=related_items,
        existing_request=existing_request
    )

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/my-access-requests")
def my_access_requests():
    return render_template("my-access-requests.html")


@app.route("/item-assessment")
def item_assessment():
    return render_template("item-assessment.html")


@app.route("/access-privacy")
def access_privacy():
    return render_template("access-privacy.html")


if __name__ == "__main__":
    app.run(debug=True)
