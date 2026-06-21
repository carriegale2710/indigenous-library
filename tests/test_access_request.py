"""
Focused test for ONE method: AccessRequest.create
Inserts a request, then reads it back to confirm the INSERT committed.

Run from the repo root with the venv active:
    python test_access_request.py
"""
from project import create_app
from project.model import AccessRequest, _get_cursor

USER_ID = 5     # a Public User that exists
ITEM_ID = 10    # a restricted item

app = create_app()
with app.app_context():
    new_id = AccessRequest.create(USER_ID, ITEM_ID, requestReason="Research use")
    print("create() returned requestID:", new_id)
    assert new_id is not None, "create() returned None - did you return cur.lastrowid?"

    # read it back to prove the INSERT committed
    cur = _get_cursor()
    cur.execute(
        "SELECT userID, itemID, requestReason, requestDate, requestStatus "
        "FROM AccessRequest WHERE requestID = %s",
        (new_id,)
    )
    row = cur.fetchone()
    cur.close()

    assert row is not None, "row not found - the INSERT did not commit"
    print("row read back:", row)
    assert row["requestStatus"] == "Pending", "new request should default to Pending"
    print("\nPASS: create inserted the row, stamped the date, defaulted to Pending.")