"""
Focused test for ONE method: CulturalMetadata.update
Seed a metadata row, change its values through update(), read it back to confirm
the new values landed, check the returned row count, and confirm that updating a
missing item changes nothing. Cleans up so the database returns to its seed state.

Run from the repo root with the venv active:
    python test_metadata_update.py
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
    # Start clean, then seed a baseline row to edit
    _clear(TEST_ITEM)
    CulturalMetadata.create(
        TEST_ITEM,
        communityGroup="Before",
        language="Before",
        location="Before",
        subjectArea="Before",
        culturalSensitivityNotes="Before",
        culturalProtocolNotes="Before",
        accessRecommendations="Before",
    )

    # Change every field through the method under test
    changed = CulturalMetadata.update(
        TEST_ITEM,
        communityGroup="After Community",
        language="After Language",
        location="After Location",
        subjectArea="After Subject",
        culturalSensitivityNotes="After Sensitivity",
        culturalProtocolNotes="After Protocol",
        accessRecommendations="After Access",
    )
    print("update() reported rows changed:", changed)
    assert changed == 1, "updating one existing item should change exactly one row"

    # Read it back: the new values should be in place
    row = CulturalMetadata.get_by_item(TEST_ITEM)
    print("row read back:", row)
    assert row["communityGroup"] == "After Community"
    assert row["language"] == "After Language"
    assert row["accessRecommendations"] == "After Access"
    assert row["itemID"] == TEST_ITEM, "WHERE clause should have targeted the right item"

    # Updating an item that doesn't exist should change zero rows
    none_changed = CulturalMetadata.update(9999, communityGroup="Nobody")
    print("update on missing item reported rows changed:", none_changed)
    assert none_changed == 0, "no row should match a non-existent itemID"

    # Clean up so the seeded database is left as we found it
    _clear(TEST_ITEM)

    print("\nPASS: update changed the row, new values read back, missing item changed nothing, cleanup done.")
