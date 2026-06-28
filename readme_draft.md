# Team01D — IFQ582 Assignment 2
### Indigenous Cultural Collection

A Flask web application for an Indigenous Academic Library. Users can browse a catalogue of collection items, view cultural metadata, submit access requests for restricted items, and review those requests through a cultural assessment workflow. Built with Flask (MVC structure), MySQL, session-based authentication, WTForms and Bootstrap 5.

---

## Prerequisites

Install these once before you set anything up:

- **Python 3.12** (the team standard). Newer versions such as 3.14 can work, but may not have prebuilt packages on Windows yet, so 3.12 keeps installs simple for everyone.
- **MySQL Server** and **MySQL Workbench** (to create and load the database).
- **Git**, or **GitHub Desktop** if you prefer a visual tool.

---

## 1. Get the code

Clone the repository (GitHub Desktop: File, then Clone Repository, then choose Team01D), and check out the **controller** branch. That branch holds the integrated, runnable app.

## 2. Create the database

Open `database.sql` in MySQL Workbench and run it (Execute All). This creates the `ifq582_a2` database and all its tables.

## 3. Set your database password

Copy `config.example.py` to `config.py` and put your own MySQL root password in it. `config.py` is gitignored, so your password never gets pushed.

- Windows: `copy config.example.py config.py`
- Mac or Linux: `cp config.example.py config.py`

## 4. Create a virtual environment and install the packages

From the repository root.

**Windows (PowerShell):**

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Mac or Linux:**

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**A note on `mysqlclient`:**

- On **Windows** (Python 3.12), pip installs a prebuilt package. Nothing extra is needed.
- On **Mac**, it compiles from source, so run `brew install mysql pkg-config` first, then the `pip install` above.

## 5. Run the app

```
python run.py
```

Open the address it prints, usually `http://127.0.0.1:5000`.

To stop the server, press `Ctrl + C` in the terminal.

---

## Running the model test

A quick check that the database connection and `User.create` work:

```
python test_create_only.py
```

---

## Project structure

```
run.py              App entry point
requirements.txt    Python packages the app needs
config.example.py   Template for your local MySQL password
config.py           Your real password (gitignored, never pushed)
database.sql        MySQL build script (run this in Workbench)
project/
  __init__.py       create_app() and the shared mysql object
  model.py          Data model: classes and data-access methods
  routes.py         Item and access-request routes
  views.py          Page routes (home, catalogue, item details, and so on)
  auth.py           Register, login, logout
  forms.py          WTForms form classes
  templates/        Jinja templates
  static/           CSS and images
```

---

## Working on the project

`controller` is the integration branch where everyone's work is brought together, so it holds the current runnable app. Do your work on your own branch, then it gets merged into `controller`. Pull the latest before you start so you're not working on stale code.
