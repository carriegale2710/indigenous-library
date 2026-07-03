-- Use this query to unhash passwords in the database to access other accounts.
UPDATE User 
-- Change pw to Hash for 'Pass1234'
SET passwordHash = 'scrypt:32768:8:1$IHBREYqzuKD0jk4z$6d39174c27e44379d0991d57503aa991f0871fac6e7213feb9d913e723c9bdfd9bd81bbbcce46a583addc70d786d6230a00d08f7c6884ec7dd8f79e1b7e7e448' 
-- Updates pw for all accounts in db
WHERE userID > 0; -- change to `WHERE userID = <int>` for specific user
-- Login with Pass1234.