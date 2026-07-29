-- Access Admin/Community Reviewer/Library Staff accounts

-- PURPOSE:

-- The registration feature defaults to making a public user account only.
-- To access features with different role permissions, you can unhash passwords from user accounts in your local `database.sql` in MySQL Workbench.

-- STEPS:

-- 1. Open MySQL Workbench and connect to your local instance (same one python run.py connects to).
-- 2. In the schema navigator on the left, make sure ifq582_a2 is set as the active schema, double-click it if it's not bolded/selected, that's what points a new query at the right database.
-- 3. Open a new SQL tab (the little page icon, or File > New Query Tab).
-- 4. Paste query below (or run `unhash.sql`).
-- 5. Run it, either the lightning bolt icon in the toolbar or Cmd+Return with your cursor on that line.Workbench will report something like "8 row(s) affected" in the output panel at the bottom, that's your confirmation all 8 seeded users got the new hash.
-- 6. You should now be able to login to all accounts with the password 'Pass1234'.
-- 7. To reverse these change, just re-run `database.sql` in MySql to reinitialise the database.

--- QUERY (copy this):

-- Use this query to unhash passwords in the database to access other accounts.
UPDATE User 
-- Change pw to Hash for 'Pass1234'
SET passwordHash = 'scrypt:32768:8:1$IHBREYqzuKD0jk4z$6d39174c27e44379d0991d57503aa991f0871fac6e7213feb9d913e723c9bdfd9bd81bbbcce46a583addc70d786d6230a00d08f7c6884ec7dd8f79e1b7e7e448' 
-- Updates pw for all accounts in db
WHERE userID > 0; -- change to `WHERE userID = <int>` for specific user
-- Login with Pass1234.