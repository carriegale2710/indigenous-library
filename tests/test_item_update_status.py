"""
Focused test for ONE method: CollectionItem.update_status
Changes an item's statusID, reads it back to prove the commit,
then restores the original value so the catalogue is left unchanged.

Run from the repo root with the venv active:
    python test_item_update_status.py
"""
from project import create_app
from project.model import CollectionItem, _get_cursor

ITEM_ID = 1   # seeded with statusID 1 (Open)


def read_status_id(item_id):
    cur = _get_cursor()
    cur.execute(
        "SELECT statusID FROM CollectionItem WHERE itemID = %s",
        (item_id,)
    )
    row = cur.fetchone()
    cur.close()
    return row["statusID"]


app = create_app()
with app.app_context():
    original = read_status_id(ITEM_ID)
    print("original statusID:", original)

    # pick a different valid status (2 = Restricted, unless it already is)
    new_status = 3 if original == 2 else 2

    count = CollectionItem.update_status(ITEM_ID, new_status)
    print("update_status() returned rowcount:", count)
    assert count == 1, "expected exactly 1 row updated"

    after = read_status_id(ITEM_ID)
    print("statusID after update:", after)
    assert after == new_status, "the commit did not land"

    # restore the seed value
    CollectionItem.update_status(ITEM_ID, original)
    restored = read_status_id(ITEM_ID)
    assert restored == original, "failed to restore original statusID"
    print("restored statusID:", restored)

    print("\nPASS: CollectionItem.update_status changed the row, committed, reverted.")
