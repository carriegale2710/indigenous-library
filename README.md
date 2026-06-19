# Team01D — IFQ582 Assignment 2

Indigenous Cultural Collection: a Flask web app backed by a MySQL database
(database `ifq582_a2`).

## Project layout

```
run.py                 App entry point (flask run / python run.py)
requirements.txt       Python packages the app needs
config.example.py      Template for your local MySQL password
config.py              Your real password (gitignored, never pushed)
database.sql           MySQL build script (run this in Workbench)
project/
  __init__.py          create_app() + the shared mysql object
  model.py             Data model: classes + data-access methods
test_create_only.py    Quick test for User.create
```

## First-time setup (each team member, once)

1. **Load the database.** Open `database.sql` in MySQL Workbench and run it.
   This creates the `ifq582_a2` database and all the tables.

2. **Set your password.** Copy `config.example.py` to `config.py` and put your
   own MySQL root password in it. `config.py` is gitignored, so your password
   never gets pushed.

3. **Make a virtual environment and install the packages.** From the repo root:

   ```
   python3 -m venv .venv
   source .venv/bin/activate        # macOS / Linux
   pip install -r requirements.txt
   ```

   (The `.venv` folder is gitignored. Everyone keeps their own.)

## Running the app

```
source .venv/bin/activate
python run.py
```

## Running the User.create test

```
source .venv/bin/activate
python test_create_only.py
```
