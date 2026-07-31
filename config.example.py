"""
Template for local secrets. Each team member does this once:

    1. Copy this file to config.py   (config.py is gitignored, never pushed)
    2. Put YOUR MySQL Workbench root password below

The app reads MYSQL_PASSWORD from config.py at startup. If config.py is
missing, it falls back to a MYSQL_PASSWORD environment variable, then blank.

"""
# Local host mySQL credentials

MYSQL_HOST="localhost" 
MYSQL_USER="root" 
MYSQL_PASSWORD="your-password" 
MYSQL_DB="indigenous_library_db" # → whatever database you ran your schema against (defaultdb or your renamed one)
MYSQL_PORT=3306

RESET_SECRET="test123"