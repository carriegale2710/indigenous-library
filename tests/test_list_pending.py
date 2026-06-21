"""
Focused test for ONE method: AccessRequest.list_pending
Confirms it returns only Pending requests, and that the two seeded
Pending requests (requestID 2 and 4) are in the result.

Run from the repo root with the venv active:
    python test_list_pending.py
"""
from project import create_app
from project.model import AccessRequest

app = create_app()
with app.app_context():
    rows = AccessRequest.list_pending()
    print("list_pending() returned", len(rows), "rows")

    assert isinstance(rows, (list, tuple)), "expected a list of rows"
    assert len(rows) >= 2, "seed data has at least 2 Pending requests (IDs 2 and 4)"

    # every row must actually be Pending
    for r in rows:
        assert r["requestStatus"] == "Pending", \
            "got a non-Pending row: " + str(r["requestStatus"])

    # the two seeded Pending requests must be present
    ids = [r["requestID"] for r in rows]
    assert 2 in ids, "seeded Pending request 2 missing"
    assert 4 in ids, "seeded Pending request 4 missing"

    print("returned requestIDs:", ids)
    print("\nPASS: list_pending returns only Pending requests, IDs 2 and 4 present.")
