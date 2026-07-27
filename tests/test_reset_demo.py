"""
Focused test for the demo reset feature: reset_demo_data() in project/reset.py,
and the protected route in project/maintenance.py.

Deliberately messes up the demo data (changes a title, adds a junk user),
runs the reset, and checks everything is back to exactly the seed state.
Also checks the /admin/reset-demo route rejects requests without the
correct secret key, so a stray or guessed request can't wipe the demo
account by accident.

Run from the repo root with the venv active:
    python -m tests.test_reset_demo
"""
import os
from project import create_app, mysql
from project.model import _get_cursor
from project.reset import reset_demo_data, _RESET_TABLES

app = create_app()

with app.app_context():

    # 1. Mess up the demo data on purpose -------------------------------------
    cur = _get_cursor()
    cur.execute("UPDATE CollectionItem SET title = %s WHERE itemID = %s", ("HACKED TITLE", 1))
    cur.execute(
        "INSERT INTO `User` (roleID, fullName, username, email, passwordHash, "
        "accountStatus, createdDate) VALUES "
        "(4, 'Junk Visitor', 'junkuser', 'junk@example.com', 'not-a-real-hash', 'active', '2026-01-01')"
    )
    mysql.connection.commit()
    cur.close()

    check = _get_cursor()
    check.execute("SELECT title FROM CollectionItem WHERE itemID = %s", (1,))
    assert check.fetchone()["title"] == "HACKED TITLE", "setup for the test didn't take"
    check.close()
    print("1. Demo data deliberately messed up (title changed, junk user added)")

    # 2. reset_demo_data() should put everything back -------------------------
    result = reset_demo_data()
    assert result == {"status": "ok", "tables_reset": len(_RESET_TABLES)}, "unexpected result shape"
    print("2. reset_demo_data() OK -", result)

    # 3. The edited title should be back to its seed value ---------------------
    check = _get_cursor()
    check.execute("SELECT title FROM CollectionItem WHERE itemID = %s", (1,))
    restored_title = check.fetchone()["title"]
    check.close()
    assert restored_title == "Kalaw Lagaw Ya Dictionary", "title should be back to seed value"
    print("3. CollectionItem 1 title restored -", restored_title)

    # 4. The junk user should be gone ------------------------------------------
    check = _get_cursor()
    check.execute("SELECT * FROM `User` WHERE username = %s", ("junkuser",))
    assert check.fetchone() is None, "junk user should be gone after reset"
    check.close()
    print("4. Junk user removed by reset")

    # 5. The seeded demo admin account should still be there and correct -------
    check = _get_cursor()
    check.execute("SELECT roleID, accountStatus FROM `User` WHERE username = %s", ("smitchell",))
    demo_admin = check.fetchone()
    check.close()
    assert demo_admin is not None, "demo admin account should exist after reset"
    assert demo_admin["roleID"] == 1, "demo admin should be Admin role"
    assert demo_admin["accountStatus"] == "active", "demo admin should be active"
    print("5. Demo admin account (smitchell) present, Admin role, active")

# 6. /admin/reset-demo should reject missing/wrong secrets, accept the right one
os.environ["RESET_SECRET"] = "test-secret-for-this-run"
with app.test_client() as client:
    no_header = client.post("/admin/reset-demo")
    assert no_header.status_code == 403, "missing header should be forbidden"

    wrong_header = client.post("/admin/reset-demo", headers={"X-Reset-Key": "wrong-value"})
    assert wrong_header.status_code == 403, "wrong secret should be forbidden"

    right_header = client.post(
        "/admin/reset-demo", headers={"X-Reset-Key": "test-secret-for-this-run"}
    )
    assert right_header.status_code == 200, "correct secret should succeed"
    assert right_header.get_json()["status"] == "ok"

print("6. /admin/reset-demo rejects missing/wrong secret, accepts the correct one")

print(
    "\nPASS: reset restores seed data, removes junk rows, demo admin survives, "
    "and the route is properly secret-protected."
)