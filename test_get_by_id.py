"""
Focused test for ONE method: CollectionItem.get_by_id
Normal item returns metadata; Pending item returns the row with NULL metadata; bad id returns None.

Run from the repo root with the venv active:
    python test_get_by_id.py
"""
from project import create_app
from project.model import CollectionItem

app = create_app()
with app.app_context():
    # A normal, reviewed item (item 1) has a metadata row
    normal = CollectionItem.get_by_id(1)
    print("item 1 title:", normal["title"])
    print("item 1 communityGroup:", normal["communityGroup"])
    assert normal["communityGroup"] is not None, "item 1 should have metadata"

    # A Pending item (item 21) has NO metadata row yet
    pending = CollectionItem.get_by_id(21)
    assert pending is not None, "LEFT JOIN wrongly dropped the Pending item"
    print("item 21 title:", pending["title"])
    print("item 21 communityGroup:", pending["communityGroup"], "(should be None)")
    assert pending["communityGroup"] is None, "expected NULL metadata for a Pending item"

    # An id that doesn't exist returns None
    missing = CollectionItem.get_by_id(9999)
    assert missing is None, "non-existent id should return None"

    print("\nPASS: metadata for normal items, NULL metadata for Pending, None for missing.")