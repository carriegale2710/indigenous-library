"""
Focused test for ONE method: CommunityComment.add_comment
Insert a comment against an existing request, confirm it landed with today's date,
then delete just that comment so the seeded database is left as we found it.

Run from the repo root with the venv active:
    python test_add_comment.py
"""
from datetime import date
from project import create_app
from project.model import CommunityComment, _get_cursor

app = create_app()

# Seed data: requestID 2 exists; userID 3 (Margaret Williams) is a Reviewer/Elder
TEST_REQUEST = 2
TEST_REVIEWER = 3

with app.app_context():
    new_id = CommunityComment.add_comment(
        TEST_REQUEST, TEST_REVIEWER, "Test comment, safe to delete."
    )
    print("add_comment returned commentID:", new_id)
    assert new_id is not None, "add_comment should return the new commentID"

    # Read the row straight back to confirm what was stored
    cur = _get_cursor()
    cur.execute(
        "SELECT commentID, requestID, reviewerID, commentText, createdDate "
        "FROM CommunityComment WHERE commentID = %s",
        (new_id,),
    )
    row = cur.fetchone()
    cur.close()
    print("row read back:", row)
    assert row is not None, "the comment should exist after add_comment"
    assert row["requestID"] == TEST_REQUEST
    assert row["reviewerID"] == TEST_REVIEWER
    assert row["commentText"] == "Test comment, safe to delete."
    assert row["createdDate"] == date.today(), "createdDate should be stamped to today"

    # Clean up: remove only the comment this test created
    from project import mysql
    cur = _get_cursor()
    cur.execute("DELETE FROM CommunityComment WHERE commentID = %s", (new_id,))
    mysql.connection.commit()
    cur.close()

    print("\nPASS: comment inserted, today's date stamped, values matched, cleanup done.")
