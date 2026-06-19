"""
Focused test for ONE method: CollectionItem.get_all
Reads the catalogue, then reads it again filtered, and checks the filter narrows it.

Run from the repo root with the venv active:
    python test_get_all.py
"""
from project import create_app
from project.model import CollectionItem

app = create_app()
with app.app_context():
    all_items = CollectionItem.get_all()
    print("total items:", len(all_items))
    songs = CollectionItem.get_all(search="Recordings")
    print("items matching 'Recordings':", len(songs))
    assert len(songs) < len(all_items), "filter did not narrow the results"