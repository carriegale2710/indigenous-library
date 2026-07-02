"""
Template for local secrets. Each team member does this once:

    1. Copy this file to config.py   (config.py is gitignored, never pushed)
    2. Put YOUR MySQL Workbench root password below

The app reads MYSQL_PASSWORD from config.py at startup. If config.py is
missing, it falls back to a MYSQL_PASSWORD environment variable, then blank.
"""
MYSQL_PASSWORD = "your_mysql_password_here"
