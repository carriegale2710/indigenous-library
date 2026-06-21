"""
Focused test for ONE method: CulturalMetadata.get_by_item
A reviewed item returns its metadata row; a Pending item returns None; a bad id returns None.

Run from the repo root with the venv active:
    python test_get_by_item.py
"""
from project import create_app
from project.model import CulturalMetadata

app = create_app()
with app.app_context():
    # Item 1 is reviewed and has a metadata row
    meta = CulturalMetadata.get_by_item(1)
    assert meta is not None, "item 1 should have a metadata row"
    print("item 1 communityGroup:", meta["communityGroup"])
    print("item 1 language:", meta["language"])
    print("item 1 location:", meta["location"])
    assert meta["itemID"] == 1, "returned row should belong to item 1"
    # Every column the method SELECTs should be addressable by name
    for col in ("metadataID", "itemID", "communityGroup", "language", "location",
                "subjectArea", "culturalSensitivityNotes", "culturalProtocolNotes",
                "accessRecommendations"):
        assert col in meta, "missing column in result: " + col

    # Item 21 is Pending and has NO metadata row yet
    none_yet = CulturalMetadata.get_by_item(21)
    print("item 21 metadata:", none_yet, "(should be None)")
    assert none_yet is None, "a Pending item with no metadata row should return None"

    # An id that doesn't exist returns None
    missing = CulturalMetadata.get_by_item(9999)
    assert missing is None, "non-existent id should return None"

    print("\nPASS: metadata row for a reviewed item, None for Pending, None for missing.")
