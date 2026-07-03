"""
Entry point for the Flask app.

Run it from the repo root with the venv active:
    flask --app run run --debug
or simply:
    python run.py
"""
from project import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
