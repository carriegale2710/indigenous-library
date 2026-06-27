"""
Combined final test for the 9 methods completed in this session.
Read-only checks run first. State-changing checks capture and restore,
and the create/update/delete trio works on a throwaway item so the
seeded catalogue is left exactly as it was.

Run from the repo root with the venv active:
    python test_model_final.py
"""
from project import create_app
from project.model import AccessRequest, CollectionItem, ReviewDecision, _get_cursor


def read_one(sql, params):
    cur = _get_cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    cur.close()
    return row


app = create_app()
with app.app_context():

    # 1. AccessRequest.list_pending -------------------------------------------
    pending = AccessRequest.list_pending()
    assert all(r["requestStatus"] == "Pending" for r in pending), "non-Pending row returned"
    ids = [r["requestID"] for r in pending]
    assert 2 in ids and 4 in ids, "seeded Pending requests 2 and 4 missing"
    print("1. list_pending OK -", len(pending), "pending requests")

    # 2. AccessRequest.update_status (capture / flip / restore) ----------------
    original = read_one("SELECT requestStatus FROM AccessRequest WHERE requestID = %s", (2,))["requestStatus"]
    assert AccessRequest.update_status(2, "Approved") == 1, "expected 1 row updated"
    assert read_one("SELECT requestStatus FROM AccessRequest WHERE requestID = %s", (2,))["requestStatus"] == "Approved"
    AccessRequest.update_status(2, original)
    assert read_one("SELECT requestStatus FROM AccessRequest WHERE requestID = %s", (2,))["requestStatus"] == original
    print("2. AccessRequest.update_status OK - changed, committed, restored")

    # 3. CollectionItem.update_status (capture / flip / restore) ---------------
    orig_status = read_one("SELECT statusID FROM CollectionItem WHERE itemID = %s", (1,))["statusID"]
    flip = 3 if orig_status == 2 else 2
    assert CollectionItem.update_status(1, flip) == 1, "expected 1 row updated"
    assert read_one("SELECT statusID FROM CollectionItem WHERE itemID = %s", (1,))["statusID"] == flip
    CollectionItem.update_status(1, orig_status)
    assert read_one("SELECT statusID FROM CollectionItem WHERE itemID = %s", (1,))["statusID"] == orig_status
    print("3. CollectionItem.update_status OK - changed, committed, restored")

    # 4. ReviewDecision.get_by_request (JOIN to User) --------------------------
    decisions = ReviewDecision.get_by_request(1)   # request 1 has decision 1 by reviewer 3
    assert len(decisions) >= 1, "request 1 should have at least one decision"
    d = decisions[0]
    assert d["decisionType"] == "Approve", "decision 1 is an Approve"
    assert d["fullName"] == "Margaret Williams", "reviewer name should join through"
    print("4. ReviewDecision.get_by_request OK - reviewer:", d["fullName"])

    # 5. AccessRequest.get_by_id (JOIN to User and CollectionItem) -------------
    req = AccessRequest.get_by_id(1)
    assert req is not None, "request 1 should exist"
    assert req["username"] == "echen", "user should join through"
    assert req["title"] == "Recordings of Meriam Mir Speakers", "item title should join through"
    assert AccessRequest.get_by_id(99999) is None, "missing id should return None"
    print("5. AccessRequest.get_by_id OK - asker echen, item:", req["title"])

    # 6. AccessRequest.get_by_user (JOIN to CollectionItem, DESC order) --------
    mine = AccessRequest.get_by_user(5)   # Emily Chen: requests 1, 3, 5
    assert all(r["userID"] == 5 for r in mine), "all rows should belong to user 5"
    assert all("title" in r for r in mine), "each row should carry the item title"
    dates = [r["requestDate"] for r in mine]
    assert dates == sorted(dates, reverse=True), "should be newest first (DESC)"
    print("6. AccessRequest.get_by_user OK -", len(mine), "requests, newest first")

    # 7-9. create -> update -> delete on a throwaway item ----------------------
    new_id = CollectionItem.create(collectionID=1, title="ZZ Test Item (delete me)")
    assert new_id is not None, "create should return the new itemID"
    made = read_one("SELECT statusID, thumbnailPath FROM CollectionItem WHERE itemID = %s", (new_id,))
    assert made["statusID"] == 4, "new item should default to Pending (4)"
    assert made["thumbnailPath"] == "/img/items/IC_Logo.jpg", "thumbnail default should apply"
    print("7. CollectionItem.create OK - new itemID", new_id, "status Pending, default thumbnail")

    # update: real field changes, bogus field ignored by the whitelist
    changed = CollectionItem.update(new_id, title="ZZ Updated Title", evil_column="hack")
    assert changed == 1, "expected 1 row updated"
    after = read_one("SELECT title FROM CollectionItem WHERE itemID = %s", (new_id,))
    assert after["title"] == "ZZ Updated Title", "title should change"
    assert CollectionItem.update(new_id, evil_column="hack") == 0, "no editable field -> 0, no query"
    print("8. CollectionItem.update OK - title changed, non-editable field ignored")

    # delete: removes the throwaway item
    assert CollectionItem.delete(new_id) == 1, "expected 1 row deleted"
    assert read_one("SELECT itemID FROM CollectionItem WHERE itemID = %s", (new_id,)) is None, "item should be gone"
    print("9. CollectionItem.delete OK - throwaway item removed, catalogue clean")

    print("\nPASS: all 9 methods behave correctly and seed data is left unchanged.")
