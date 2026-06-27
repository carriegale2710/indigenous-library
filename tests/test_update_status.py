"""
Focused test for ONE method: AccessRequest.update_status
Flips a request's status, reads it back to prove the commit landed,
then restores the original value so seed data is left unchanged.

Run from the repo root with the venv active:
    python test_update_status.py
"""
from project import create_app
from project.model import AccessRequest, _get_cursor

REQUEST_ID = 2   # seeded as 'Pending'


def read_status(request_id):
    cur = _get_cursor()
    cur.execute(
        "SELECT requestStatus FROM AccessRequest WHERE requestID = %s",
        (request_id,)
    )
    row = cur.fetchone()
    cur.close()
    return row["requestStatus"]


app = create_app()
with app.app_context():
    original = read_status(REQUEST_ID)
    print("original status:", original)

    count = AccessRequest.update_status(REQUEST_ID, "Approved")
    print("update_status() returned rowcount:", count)
    assert count == 1, "expected exactly 1 row updated"

    after = read_status(REQUEST_ID)
    print("status after update:", after)
    assert after == "Approved", "the commit did not land"

    # restore the seed value so the DB is left as we found it
    AccessRequest.update_status(REQUEST_ID, original)
    restored = read_status(REQUEST_ID)
    assert restored == original, "failed to restore original status"
    print("restored status:", restored)

    print("\nPASS: update_status changed the row, committed, and was reverted.")
