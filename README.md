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

# Team01D

For a team

## What is Github for?

https://www.w3schools.com/whatis/whatis_github.asp

## Github Basics

https://docs.github.com/en/get-started/start-your-journey/hello-world
https://docs.github.com/en/get-started/learning-to-code/getting-started-with-git

## Set up git on your local computer

https://docs.github.com/en/get-started/git-basics/set-up-git
https://training.github.com/downloads/github-git-cheat-sheet/

## How to clone this repo to your local computer

Please use these guides to get setup

Visual Studio IDE (easier): https://code.visualstudio.com/docs/sourcecontrol/repos-remotes
In your terminal: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

## Package Requirements

```
blinker==1.9.0
Bootstrap-Flask==2.4.1
click==8.1.8
colorama==0.4.6
dnspython==2.7.0
dominate==2.9.1
email_validator==2.2.0
Flask==3.1.0
Flask-MySQLdb==2.0.0
Flask-WTF==1.2.2
greenlet==3.1.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.5
MarkupSafe==3.0.2
mysqlclient==2.2.7
numpy==2.2.2
typing_extensions==4.12.2
visitor==0.1.3
Werkzeug==3.1.3
WTForms==3.2.1
```
