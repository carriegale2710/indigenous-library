"""
Focused test for ONE method: CulturalMetadata.create
Insert a metadata row on a Pending item that has none, read it back, check the
values landed, then clean up so the database returns to its seeded state.

itemID is UNIQUE in CulturalMetadata (one row per item), so this test clears the
test item first and again at the end, which keeps it safe to run repeatedly.

Run from the repo root with the venv active:
    python test_metadata_create.py
"""
from project import create_app
from project.model import CulturalMetadata, _get_cursor

app = create_app()

# Item 20 is a Pending item that ships with NO metadata row in database.sql
TEST_ITEM = 20


def _clear(item_id):
    """Remove any metadata row for this item so the test can run again cleanly."""
    from project import mysql
    cur = _get_cursor()
    cur.execute("DELETE FROM CulturalMetadata WHERE itemID = %s", (item_id,))
    mysql.connection.commit()
    cur.close()


with app.app_context():
    # Start clean: no metadata row for the test item
    _clear(TEST_ITEM)
    assert CulturalMetadata.get_by_item(TEST_ITEM) is None, "test item should start with no metadata"

    # Insert a row through the method under test
    new_id = CulturalMetadata.create(
        TEST_ITEM,
        communityGroup="Test Community",
        language="Test Language",
        location="Test Location",
        subjectArea="Test Subject",
        culturalSensitivityNotes="Sensitivity note",
        culturalProtocolNotes="Protocol note",
        accessRecommendations="Open access",
    )
    print("create() returned metadataID:", new_id)
    assert new_id is not None, "create should return the new metadataID"

    # Read it back: the row should now exist with the values we inserted
    row = CulturalMetadata.get_by_item(TEST_ITEM)
    assert row is not None, "metadata row should exist after create"
    print("row read back:", row)
    assert row["itemID"] == TEST_ITEM, "itemID should match the item we inserted for"
    assert row["communityGroup"] == "Test Community"
    assert row["language"] == "Test Language"
    assert row["accessRecommendations"] == "Open access"
    assert row["metadataID"] == new_id, "get_by_item should return the row create just made"

    # Clean up so the seeded database is left as we found it
    _clear(TEST_ITEM)
    assert CulturalMetadata.get_by_item(TEST_ITEM) is None, "cleanup should have removed the test row"

    print("\nPASS: create inserted the row, values matched on read-back, cleanup restored the seed state.")
