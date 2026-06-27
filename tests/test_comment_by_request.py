"""
Focused test for ONE method: CommunityComment.get_by_request
Reads seeded data only (no writes, no cleanup needed).

Request 1 has two comments in database.sql, oldest first:
  commentID 1 by userID 3 (Margaret Williams) on 2026-05-20
  commentID 2 by userID 4 (David Yunupingu) on 2026-05-21
Request 6 has no comments.

Run from the repo root with the venv active:
    python test_comment_by_request.py
"""
from project import create_app
from project.model import CommunityComment

app = create_app()

with app.app_context():
    rows = CommunityComment.get_by_request(1)
    print("comments for request 1:", len(rows))
    for r in rows:
        print("  ", r["commentID"], r["createdDate"], r["fullName"])

    assert len(rows) == 2, "request 1 should have two comments"

    # JOIN worked: the reviewer's name came across from the User table
    assert rows[0]["fullName"] == "Margaret Williams", "JOIN should bring the reviewer name"

    # ORDER BY createdDate: oldest first, so commentID 1 before commentID 2
    assert rows[0]["commentID"] == 1, "oldest comment should be first"
    assert rows[1]["commentID"] == 2, "newer comment should be second"
    assert rows[0]["createdDate"] <= rows[1]["createdDate"], "rows should be in date order"

    # A request with no comments returns an empty list, not None
    none_rows = CommunityComment.get_by_request(6)
    print("comments for request 6:", len(none_rows))
    assert none_rows == [], "a request with no comments should return an empty list"

    print("\nPASS: comments returned with reviewer names, ordered oldest first, empty list when none.")
