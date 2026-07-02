# Running the model tests

These are small, focused checks. Each one exercises a single data access method in `project/model.py`, runs it against a local MySQL copy of the database, and prints `PASS` if the method behaves the way we expect. I wrote them so we can prove each method works before wiring it into a page, and so anyone on the team can re-run them after a change.

## Before you run anything

You need three things in place:

1. **The virtual environment is active.** From the repo root run `source .venv/bin/activate` (Mac/Linux) or `.venv\Scripts\activate` (Windows). Your prompt shows `(.venv)` when it's on.
2. **MySQL is running and the database is loaded.** Run `database.sql` once in MySQL Workbench to build and seed the `ifq582_a2` database.
3. **Your `config.py` exists.** Copy `config.example.py` to `config.py` and put your own MySQL password in it. This file is gitignored, so it never gets pushed.

## How to run them

Run the tests **from the repo root**, and call them as modules with dots, not as a file path. This is the part that trips people up.

**Correct:**

```bash
python -m tests.test_list_pending
```

**Wrong** (fails with `ModuleNotFoundError: No module named 'project'`):

```bash
python tests/test_list_pending.py
```

### Why the dot version is the one that works

Every test starts with `from project import create_app`. That import only resolves when the repo root sits on Python's search path. Running with `python -m tests.test_name` from the root keeps the root on the path, so `project` is found. Running the file directly (`python tests/...py`) puts the **tests** folder on the path instead, and Python can no longer see the `project` package. So you don't move the file back to the root; you just call it the module way.

Note there's no `.py` on the end and you use dots, not slashes: `tests.test_list_pending`, not `tests/test_list_pending.py`.

### Running every test in one go

```bash
for t in tests/test_*.py; do
  name="tests.$(basename "$t" .py)"
  echo "=== $name ==="
  python -m "$name"
done
```

For a single broad check, `python -m tests.test_model_final` runs the nine methods from the final build batch in one pass.

## What each test covers

| Test file | Method(s) it checks | Touches data? |
|-----------|--------------------|----------------|
| `test_get_all.py` | `CollectionItem.get_all` | Reads only |
| `test_get_by_id.py` | `CollectionItem.get_by_id` | Reads only |
| `test_get_by_item.py` | `CulturalMetadata.get_by_item` | Reads only |
| `test_comment_by_request.py` | `CommunityComment.get_by_request` | Reads only |
| `test_list_pending.py` | `AccessRequest.list_pending` | Reads only |
| `test_update_status.py` | `AccessRequest.update_status` | Writes, then restores |
| `test_item_update_status.py` | `CollectionItem.update_status` | Writes, then restores |
| `test_metadata_create.py` | `CulturalMetadata.create`, `get_by_item` | Writes, then cleans up |
| `test_metadata_update.py` | `CulturalMetadata.create`, `update`, `get_by_item` | Writes, then cleans up |
| `test_add_comment.py` | `CommunityComment.add_comment` | Writes, then deletes the row |
| `test_review_decision_create.py` | `ReviewDecision.create` | Writes, then deletes the row |
| `test_access_request.py` | `AccessRequest.create` | Writes and **leaves the row** |
| `test_create_only.py` | `User.create`, `User.get_by_username` | Writes and **leaves the row** |
| `test_model_final.py` | The nine final methods: `AccessRequest` (`list_pending`, `update_status`, `get_by_id`, `get_by_user`), `CollectionItem` (`update_status`, `create`, `update`, `delete`), `ReviewDecision.get_by_request` | Writes, then restores and deletes its own throwaway item |

## A note on the seed data

Most tests put the database back the way they found it, either by restoring the original value or deleting the row they added. Two of the early ones, `test_access_request.py` and `test_create_only.py`, leave their inserted row behind on purpose. That's harmless, but it's why you might see an extra pending request or an extra user after running them. If you ever want a clean slate, re-run `database.sql` to rebuild and reseed the database.
