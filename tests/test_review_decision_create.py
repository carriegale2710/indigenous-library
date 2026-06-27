"""
Focused test for ONE method: ReviewDecision.create
Insert a decision against an existing request, confirm it landed with today's date,
then delete just that decision so the seeded database is left as we found it.

Run from the repo root with the venv active:
    python test_review_decision_create.py
"""
from datetime import date
from project import create_app
from project.model import ReviewDecision, _get_cursor

app = create_app()

# Seed data: requestID 2 exists; userID 3 (Margaret Williams) is a Reviewer/Elder
TEST_REQUEST = 2
TEST_REVIEWER = 3

with app.app_context():
    new_id = ReviewDecision.create(
        TEST_REQUEST,
        TEST_REVIEWER,
        "Approve",
        decisionNotes="Test decision, safe to delete.",
        accessConditions="Reading room only",
    )
    print("create returned decisionID:", new_id)
    assert new_id is not None, "create should return the new decisionID"

    # Read the row straight back to confirm what was stored
    cur = _get_cursor()
    cur.execute(
        "SELECT decisionID, requestID, reviewerID, decisionType, decisionNotes, "
        "accessConditions, decisionDate FROM ReviewDecision WHERE decisionID = %s",
        (new_id,),
    )
    row = cur.fetchone()
    cur.close()
    print("row read back:", row)
    assert row is not None, "the decision should exist after create"
    assert row["requestID"] == TEST_REQUEST
    assert row["reviewerID"] == TEST_REVIEWER
    assert row["decisionType"] == "Approve"
    assert row["decisionNotes"] == "Test decision, safe to delete."
    assert row["accessConditions"] == "Reading room only"
    assert row["decisionDate"] == date.today(), "decisionDate should be stamped to today"

    # Clean up: remove only the decision this test created
    from project import mysql
    cur = _get_cursor()
    cur.execute("DELETE FROM ReviewDecision WHERE decisionID = %s", (new_id,))
    mysql.connection.commit()
    cur.close()

    print("\nPASS: decision inserted, today's date stamped, values matched, cleanup done.")
