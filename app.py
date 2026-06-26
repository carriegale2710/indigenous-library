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

    return render_template("catalogue.html", items=items)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
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
