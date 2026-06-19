"""
Focused test for ONE method: User.create

It calls create(), then reads the row back with get_by_username() (already
implemented), so the verify_password and list_all stubs don't get in the way.

Run from the repo root with the venv active:
    python test_create_only.py
"""
import time
from werkzeug.security import generate_password_hash
from project import create_app
from project.model import User

# unique each run so re-running doesn't trip the UNIQUE username/email rule
stamp = int(time.time())
username = f"createtest_{stamp}"
email = f"createtest_{stamp}@example.com"
ROLE_ID = 4   # must be a roleID that exists in your Role table

app = create_app()
with app.app_context():
    try:
        pw_hash = generate_password_hash("Password123")   # the view layer hashes; create just stores

        new_id = User.create(ROLE_ID, "Create Test", username, email, pw_hash)
        print(f"create() returned userID: {new_id}")
        assert new_id is not None, "create() returned None, did you return cur.lastrowid?"

        row = User.get_by_username(username)
        assert row is not None, "row not found, the INSERT did not commit"
        print("row read back from the database:")
        print(f"  userID        = {row['userID']}")
        print(f"  roleID        = {row['roleID']}        (want {ROLE_ID})")
        print(f"  username      = {row['username']}")
        print(f"  email         = {row['email']}")
        print(f"  accountStatus = {row['accountStatus']}   (want 'active' from the default)")
        print(f"  createdDate   = {row['createdDate']}     (want today)")
        print(f"  passwordHash  = {row['passwordHash'][:25]}...  (stored hashed, not plain)")

        assert row["roleID"] == ROLE_ID
        assert row["accountStatus"] == "active"
        print("\nPASS: User.create inserted the row, set the date, and returned the new id.")
    except Exception as e:
        print(f"\nFAIL: {type(e).__name__}: {e}")
