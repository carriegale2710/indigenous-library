"""
IFQ582 Assignment 2  |  Group 1D  |  Indigenous Cultural Collection
Data model: classes + data-access methods for the Flask app.

Source of truth for tables and columns: IFQ582_A2_database.sql  (database: ifq582_a2)

================================================================================
HOW TO USE THIS FILE
================================================================================
This is a DRAFT skeleton. Every data-access method is stubbed with:
  * a docstring that states exactly which table, columns and WHERE clause it needs
  * a "# TODO" line where YOU write the SQL
  * raise NotImplementedError(...) so an unfinished method fails loudly

Suggested build order (do not write all 30+ methods at once):
  1. _get_cursor()                         connect first, prove it works
  2. CollectionItem.get_all                home page reads from this
  3. CollectionItem.get_by_id              item details page
  4. User.get_by_username + verify_password + create   login and register
  5. AccessRequest.create                  public submits a request
  6. ReviewDecision.create + CollectionItem.update_status   the review workflow
Then fill in the rest as the View team needs them.

================================================================================
WIRING THE DATABASE (Flask-MySQLdb)
================================================================================
In project/__init__.py you create the MySQL object and configure the connection:

    from flask_mysqldb import MySQL
    mysql = MySQL()

    def create_app():
        app = Flask(__name__)
        app.config["MYSQL_HOST"] = "localhost"
        app.config["MYSQL_USER"] = "root"
        app.config["MYSQL_PASSWORD"] = "your_password"
        app.config["MYSQL_DB"] = "ifq582_a2"
        app.config["MYSQL_CURSORCLASS"] = "DictCursor"   # rows come back as dicts
        mysql.init_app(app)
        ...

Then this file imports that same object. Update the import below to match your
package name (e.g. "from project import mysql" or "from .extensions import mysql").
"""
from datetime import date
from werkzeug.security import check_password_hash
# ----------------------------------------------------------------------------
# Shared database helper
# ----------------------------------------------------------------------------
def _get_cursor():
    """
    Return a cursor on the live Flask-MySQLdb connection.

    With MYSQL_CURSORCLASS = "DictCursor" each fetched row is a dict keyed by
    column name, e.g. row["title"].

    The import sits inside the function on purpose: it avoids a circular import
    (project/__init__.py imports your views, which import this file). Change
    "project" to whatever your package folder is actually called.

    Typical use inside a method:
        cur = _get_cursor()
        cur.execute("SELECT ...", (param,))
        rows = cur.fetchall()
        cur.close()
        return rows

    For INSERT / UPDATE / DELETE you must also commit:
        from project import mysql
        mysql.connection.commit()
    """
    from project import mysql      # adjust "project" to your package folder name
    return mysql.connection.cursor()


# ============================================================================
# Lookup tables
# ============================================================================
class Role:
    """Role lookup: Admin, Community Reviewer/Elder, Library Staff, Public User."""

    def __init__(self, roleID=None, roleName=None, roleDescription=None):
        self.roleID = roleID
        self.roleName = roleName
        self.roleDescription = roleDescription

    @staticmethod
    def get_all():
        """SELECT every row from Role. Returns a list of role rows."""
        cur = _get_cursor()
        cur.execute("SELECT roleID, roleName, roleDescription FROM Role")
        rows = cur.fetchall()
        cur.close()
        return rows
       
    @staticmethod
    def get_by_id(role_id):
        """SELECT one Role by roleID. Returns a single row or None."""
        cur = _get_cursor()
        cur.execute("SELECT roleID, roleName, roleDescription FROM Role WHERE roleID = %s", (role_id,))
        rows = cur.fetchone()
        cur.close()
        return rows
       

class Collection:
    """Collection groups items by theme (Languages, Songlines, etc.)."""

    def __init__(self, collectionID=None, collectionName=None,
                 collectionDescription=None, collectionTheme=None):
        self.collectionID = collectionID
        self.collectionName = collectionName
        self.collectionDescription = collectionDescription
        self.collectionTheme = collectionTheme

    @staticmethod
    def get_all():
        """SELECT every Collection. Used to populate filter dropdowns."""
        cur = _get_cursor()
        cur.execute("SELECT collectionID, collectionName, collectionDescription, collectionTheme FROM Collection")
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def get_by_id(collection_id):
        """SELECT one Collection by collectionID. Returns a row or None."""
        cur = _get_cursor()
        cur.execute("SELECT collectionID, collectionName, collectionDescription, collectionTheme FROM Collection WHERE collectionID = %s", (collection_id,))
        rows = cur.fetchone()
        cur.close()
        return rows


class AccessStatus:
    """Access status lookup: Open, Restricted, Culturally Sensitive, Pending."""

    def __init__(self, statusID=None, statusName=None, statusDescription=None):
        self.statusID = statusID
        self.statusName = statusName
        self.statusDescription = statusDescription

    @staticmethod
    def get_all():
        """SELECT every AccessStatus. Used for filters and the review screen."""
        cur = _get_cursor()
        cur.execute("SELECT statusID, statusName, statusDescription FROM AccessStatus")
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def get_by_id(status_id):
        """SELECT one AccessStatus by statusID. Returns a row or None."""
        cur = _get_cursor()
        cur.execute("SELECT statusID, statusName, statusDescription FROM AccessStatus WHERE statusID = %s", (status_id,))
        rows = cur.fetchone()
        cur.close()
        return rows

# ============================================================================
# Users and authentication
# ============================================================================
class User:
    """An account. roleID controls what the user may do across the app."""

    def __init__(self, userID=None, roleID=None, fullName=None, username=None,
                 email=None, passwordHash=None, accountStatus=None, createdDate=None):
        self.userID = userID
        self.roleID = roleID
        self.fullName = fullName
        self.username = username
        self.email = email
        self.passwordHash = passwordHash
        self.accountStatus = accountStatus
        self.createdDate = createdDate

    @staticmethod
    def get_by_username(username):
        """
        SELECT one User by username. The login route calls this, then checks
        the password with verify_password(). Returns a row or None.
        """
        cur = _get_cursor()
        cur.execute("SELECT userID, roleID, fullName, username, email, passwordHash, accountStatus, createdDate FROM `User` WHERE username = %s", (username,))
        rows = cur.fetchone()
        cur.close()
        return rows
    
    @staticmethod
    def get_by_email(email):
        """
        SELECT one User by email. The login route calls this, then checks
        the password with verify_password(). Returns a row or None.
        """
        cur = _get_cursor()
        cur.execute("SELECT userID, roleID, fullName, username, email, passwordHash, accountStatus, createdDate FROM `User` WHERE email = %s", (email,))
        rows = cur.fetchone()
        cur.close()
        return rows


    @staticmethod
    def get_by_id(userID):
        """SELECT one User by userID. Flask-Login's user loader uses this."""
        cur = _get_cursor()
        cur.execute("SELECT userID, roleID, fullName, username, email, passwordHash, accountStatus, createdDate FROM `User` WHERE userID = %s", (userID,))
        rows = cur.fetchone()
        cur.close()
        return rows

    @staticmethod
    def create(roleID, fullName, username, email, passwordHash, accountStatus="active"):
        """
        INSERT a new User (registration).
        IMPORTANT: passwordHash must already be hashed before it reaches here.
        Hash it in the view/form layer (e.g. werkzeug generate_password_hash),
        never store a plain password. Remember mysql.connection.commit().
        Returns the new userID (cur.lastrowid).
        """
        cur = _get_cursor()
        cur.execute("INSERT INTO `User` "
        "(roleID, fullName, username, email, passwordHash, accountStatus, createdDate) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (roleID, fullName, username, email, passwordHash, accountStatus, date.today()))
        from project import mysql
        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id

    @staticmethod
    def verify_password(stored_hash, candidate_password):
        """
        Return True if candidate_password matches stored_hash.
        Use the checker that matches your hashing function
        (e.g. werkzeug check_password_hash). No SQL here.
        """
        return check_password_hash(stored_hash, candidate_password)
      

    @staticmethod
    def list_all():
        """SELECT all users (Admin user-management screen). Returns a list."""
        cur = _get_cursor()
        cur.execute("SELECT userID, roleID, fullName, username, email, passwordHash, accountStatus, createdDate FROM `User`")
        rows = cur.fetchall()
        cur.close()
        return rows
        


# ============================================================================
# Collection items (the catalogue) and their cultural metadata
# ============================================================================
class CollectionItem:
    """A catalogue item. statusID 4 (Pending) is the default for new items."""

    def __init__(self, itemID=None, collectionID=None, statusID=None, title=None,
                 authorCreator=None, year=None, itemType=None, summary=None,
                 thumbnailPath=None, nextReviewDate=None):
        self.itemID = itemID
        self.collectionID = collectionID
        self.statusID = statusID
        self.title = title
        self.authorCreator = authorCreator
        self.year = year
        self.itemType = itemType
        self.summary = summary
        self.thumbnailPath = thumbnailPath
        self.nextReviewDate = nextReviewDate

    @staticmethod
    def get_all(search=None, collection_id=None, status_id=None):
        """
         Build the WHERE clause from whichever filters are provided:
          * search       LIKE on title (and maybe summary)
          * collection_id exact match on collectionID
          * status_id     exact match on statusID
        If no filter is passed, return everything. Returns a list of rows.

        Tip: build the SQL with a growing list of conditions and a params list,
        then join the conditions with " AND ". Always use %s placeholders, never
        string formatting, so you are safe from SQL injection. 
        """
        sql = """
            SELECT 
                ci.itemID,
                ci.title,
                ci.authorCreator,
                ci.`year`,
                ci.itemType,
                ci.summary,
                ci.thumbnailPath,
                ci.statusID,
                ci.collectionID,
                c.collectionName,
                ast.statusName
            FROM CollectionItem ci
                JOIN Collection c  
                    ON ci.collectionID = c.collectionID
                JOIN AccessStatus ast 
                    ON ci.statusID = ast.statusID
                LEFT JOIN CulturalMetadata cm
                    ON ci.itemID = cm.itemID
            """

        # Collect a condition + value for each filter that was actually passed
        conditions = []
        params = []

        if search:
            like = f"%{search}%"
            conditions.append(
                "(ci.title LIKE %s OR ci.summary LIKE %s OR ci.authorCreator LIKE %s "
                "OR cm.communityGroup LIKE %s OR cm.`language` LIKE %s "
                "OR cm.location LIKE %s OR cm.subjectArea LIKE %s)"
            )
            params.extend([like] * 7)
        if collection_id:
            conditions.append("ci.collectionID = %s")
            params.append(collection_id)
        if status_id:
            conditions.append("ci.statusID = %s")
            params.append(status_id)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY ci.title"     # ensures search returns consistent ordering for same search terms

        cur = _get_cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        return rows 
    
    @staticmethod
    def get_featured_items():
        """
        Pages used:
            - index.html
        Purpose:
            - populates the 'Featured Items' cards with a random set of 3 items
        """
        cur = _get_cursor()
        cur.execute("""
            SELECT
                ci.itemID,
                ci.title,
                ci.summary,
                ci.thumbnailPath,
                ci.statusID,
                ast.statusName
            FROM CollectionItem ci
            JOIN AccessStatus ast
                ON ci.statusID = ast.statusID
            ORDER BY RAND()
            LIMIT 3
        """)
        rows = cur.fetchall()
        cur.close()
        return rows
    
    
    @staticmethod
    def get_by_id(item_id):
        """
        Item details page. SELECT one item JOINed to Collection, AccessStatus
        and (LEFT JOIN) CulturalMetadata, since Pending items have no metadata
        row yet. Returns a single row or None (None drives the 404 / empty state).
        """
        cur = _get_cursor()
        cur.execute(
            """
            SELECT 
                ci.itemID,
                ci.title,
                ci.authorCreator,
                ci.`year`,
                ci.itemType,
                ci.summary,
                ci.thumbnailPath,
                ci.statusID,
                ci.collectionID,
                ci.nextReviewDate,
                c.collectionName,
                ast.statusName,
                ast.statusDescription,
                cm.communityGroup,
                cm.language,
                cm.location,
                cm.subjectArea,
                cm.culturalSensitivityNotes,
                cm.culturalProtocolNotes,
                cm.accessRecommendations
            FROM CollectionItem ci
                JOIN Collection c 
                    ON ci.collectionID = c.collectionID
                JOIN AccessStatus ast 
                    ON ci.statusID = ast.statusID
                LEFT JOIN CulturalMetadata cm 
                    ON ci.itemID = cm.itemID
            WHERE ci.itemID = %s
            """,
            (item_id,)
        )
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def create(collectionID, title, authorCreator=None, year=None, itemType=None,
               summary=None, thumbnailPath=None, statusID=4, nextReviewDate=None):
        """
        INSERT a new item (Library Staff). New items default to statusID 4 = Pending.
        Commit, then return the new itemID.
        """
        if thumbnailPath is None:
            thumbnailPath = "/img/items/IC_Logo.jpg"
        cur = _get_cursor()
        cur.execute(
            "INSERT INTO CollectionItem "
            "(collectionID, statusID, title, authorCreator, `year`, itemType, summary, thumbnailPath, nextReviewDate) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (collectionID, statusID, title, authorCreator, year, itemType, summary, thumbnailPath, nextReviewDate)
        )
        from project import mysql
        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id

    @staticmethod
    def update(item_id, **fields):
        """
        UPDATE an item's editable fields (title, summary, collection, etc.).
        Decide which columns staff may edit, build a SET clause from the passed
        fields, commit. Returns nothing (or the affected row count).
        """
        editable = {"collectionID", "title", "authorCreator",
                    "year", "itemType", "summary", "thumbnailPath", "nextReviewDate"}

        set_parts = []
        params = []
        for column, value in fields.items():
            if column in editable:
                set_parts.append("`" + column + "` = %s")
                params.append(value)

        if not set_parts:
            return 0

        params.append(item_id)
        sql = "UPDATE CollectionItem SET " + ", ".join(set_parts) + " WHERE itemID = %s"

        cur = _get_cursor()
        cur.execute(sql, params)
        from project import mysql
        mysql.connection.commit()
        count = cur.rowcount
        cur.close()
        return count
        

    @staticmethod
    def update_status(item_id, new_status_id):
        """
        The status transition. After a review decision, move an item between
        Pending / Open / Restricted / Culturally Sensitive. Commit.
        This is the write half of the review workflow, pair it with
        ReviewDecision.create.
        """
        cur = _get_cursor()
        cur.execute(
            "UPDATE CollectionItem SET statusID = %s WHERE itemID = %s",
            (new_status_id, item_id)
        )
        from project import mysql
        mysql.connection.commit()
        count = cur.rowcount
        cur.close()
        return count

    @staticmethod
    def delete(item_id):
        """
        DELETE an item. CulturalMetadata cascades; AccessRequest does not, so
        decide how to handle items that already have requests. Commit.
        """
        cur = _get_cursor()
        cur.execute(
            "DELETE FROM CollectionItem WHERE itemID = %s",
            (item_id,)
        )
        from project import mysql
        mysql.connection.commit()
        count = cur.rowcount
        cur.close()
        return count


class CulturalMetadata:
    """One row per item (1:1). Pending items have no metadata row yet."""

    def __init__(self, metadataID=None, itemID=None, communityGroup=None,
                 language=None, location=None, subjectArea=None,
                 culturalSensitivityNotes=None, culturalProtocolNotes=None,
                 accessRecommendations=None):
        self.metadataID = metadataID
        self.itemID = itemID
        self.communityGroup = communityGroup
        self.language = language
        self.location = location
        self.subjectArea = subjectArea
        self.culturalSensitivityNotes = culturalSensitivityNotes
        self.culturalProtocolNotes = culturalProtocolNotes
        self.accessRecommendations = accessRecommendations

    @staticmethod
    def get_by_item(item_id):
        """SELECT the metadata row for one item. Returns a row or None."""
        cur = _get_cursor()
        cur.execute("SELECT metadataID, itemID, communityGroup, `language`, location, subjectArea, culturalSensitivityNotes, culturalProtocolNotes, accessRecommendations FROM CulturalMetadata WHERE itemID = %s", (item_id,))
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def create(itemID, communityGroup=None, language=None, location=None,
               subjectArea=None, culturalSensitivityNotes=None,
               culturalProtocolNotes=None, accessRecommendations=None):
        """
        INSERT a metadata row. A Reviewer/Elder adds this when first reviewing a
        Pending item. itemID is UNIQUE, so one row per item. Commit.
        """
        cur = _get_cursor()
        cur.execute(
            "INSERT INTO CulturalMetadata " 
            "(itemID, communityGroup, language, location, subjectArea, culturalSensitivityNotes, culturalProtocolNotes, accessRecommendations) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
            (itemID, communityGroup, language, location, subjectArea, culturalSensitivityNotes, culturalProtocolNotes, accessRecommendations)
        )
        from project import mysql
        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id

    @staticmethod
    def update(item_id, communityGroup=None, language=None, location=None, subjectArea=None, culturalSensitivityNotes=None, culturalProtocolNotes=None, accessRecommendations=None):
        """UPDATE the metadata for an item (Reviewer edits). Commit."""
        cur = _get_cursor()
        cur.execute(
            "UPDATE CulturalMetadata SET communityGroup = %s, language = %s, location = %s, subjectArea = %s, culturalSensitivityNotes = %s, culturalProtocolNotes= %s, accessRecommendations = %s "  
            "WHERE itemID = %s", (communityGroup, language, location, subjectArea, culturalSensitivityNotes, culturalProtocolNotes, accessRecommendations, item_id))
        from project import mysql
        mysql.connection.commit()
        count = cur.rowcount
        cur.close()
        return count


# ============================================================================
# Access requests, review decisions, community comments (the workflow)
# ============================================================================
class AccessRequest:
    """A public user's request to view a Restricted or Sensitive item."""

    def __init__(self, requestID=None, userID=None, itemID=None,
                 requestReason=None, supportingDocuments=None,
                 requestDate=None, requestStatus=None):
        self.requestID = requestID
        self.userID = userID
        self.itemID = itemID
        self.requestReason = requestReason
        self.supportingDocuments = supportingDocuments
        self.requestDate = requestDate
        self.requestStatus = requestStatus

    @staticmethod
    def create(userID, itemID, requestReason=None, supportingDocuments=None,
               requestStatus="Pending"):
        """
        INSERT a new access request (public user submits the form on the details
        page). Set requestDate to today. Commit, return the new requestID.
        """
        cur = _get_cursor()
        cur.execute(
            "INSERT INTO AccessRequest "
            "(userID, itemID, requestReason, supportingDocuments, requestDate, requestStatus) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (userID, itemID, requestReason, supportingDocuments, date.today(), requestStatus)
        )
        from project import mysql
        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id


    @staticmethod
    def get_by_id(request_id):
        """
        SELECT one request, ideally JOINed to User and CollectionItem so the
        assessment page can show who asked and for which item. Row or None.
        """
        cur = _get_cursor()
        cur.execute(
            """
            SELECT 
                ar.requestID,
                ar.userID,
                ar.itemID,
                ar.requestReason,
                ar.supportingDocuments,
                ar.requestDate,
                ar.requestStatus,
                u.fullName,
                u.username,
                CollectionItem.title
            FROM AccessRequest ar
                JOIN `User` u
                    ON ar.userID = u.userID
                JOIN CollectionItem 
                    ON ar.itemID = CollectionItem.itemID
            WHERE ar.requestID = %s
            """,
            (request_id,)
        )
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def get_by_user(userID):
        """SELECT all requests a user has made (their 'my requests' view)."""
        cur = _get_cursor()
        cur.execute(
            """
            SELECT
                ar.requestID,
                ar.userID,
                ar.itemID,
                ar.requestReason,
                ar.supportingDocuments,
                ar.requestDate,
                ar.requestStatus,
                ci.title
            FROM AccessRequest ar
                JOIN CollectionItem ci
                    ON ar.itemID = ci.itemID
            WHERE ar.userID = %s
            ORDER BY ar.requestDate DESC
            """,
            (userID,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def list_pending():
        """
        SELECT requests still awaiting a decision (requestStatus = 'Pending').
        This is the Reviewer's work queue. Returns a list.
        """
        cur = _get_cursor()
        cur.execute(
            "SELECT requestID, userID, itemID, requestReason, supportingDocuments, requestDate, requestStatus "
            "FROM AccessRequest WHERE requestStatus = %s",
            ("Pending",)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
    
    @staticmethod
    def get_all_by_item(item_id):
        """
        SELECT all access requests for one item, joined to User and CollectionItem.
        Returns a list of rows.
        """
        cur = _get_cursor()
        cur.execute(
            """
            SELECT 
                ar.requestID,
                ar.userID,
                ar.itemID,
                ar.requestReason,
                ar.supportingDocuments,
                ar.requestDate,
                ar.requestStatus,
                u.fullName,
                u.username,
                u.email,
                CollectionItem.title
            FROM AccessRequest ar
                JOIN `User` u
                    ON ar.userID = u.userID
                JOIN CollectionItem
                    ON ar.itemID = CollectionItem.itemID
            WHERE ar.itemID = %s
            ORDER BY ar.requestDate DESC
            """,
            (item_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
    
    @staticmethod
    def update_status(request_id, new_status):
        """
        UPDATE requestStatus to 'Approved' or 'Rejected' once a decision is
        recorded. Commit. Call this alongside ReviewDecision.create.
        """
        cur = _get_cursor()
        cur.execute(
            "UPDATE AccessRequest SET requestStatus = %s WHERE requestID = %s",
            (new_status, request_id)
        )
        from project import mysql
        mysql.connection.commit()
        count = cur.rowcount
        cur.close()
        return count


class ReviewDecision:
    """
    A reviewer's ruling on a request. This is the AUDIT record: reviewerID and
    decisionDate are who decided and when.
    """

    def __init__(self, decisionID=None, requestID=None, reviewerID=None,
                 decisionType=None, decisionNotes=None, accessConditions=None,
                 decisionDate=None):
        self.decisionID = decisionID
        self.requestID = requestID
        self.reviewerID = reviewerID
        self.decisionType = decisionType
        self.decisionNotes = decisionNotes
        self.accessConditions = accessConditions
        self.decisionDate = decisionDate

    @staticmethod
    def create(requestID, reviewerID, decisionType, decisionNotes=None,
               accessConditions=None):
        """
        INSERT the decision. decisionType is 'Approve' or 'Reject'. Stamp
        reviewerID (the logged-in reviewer) and decisionDate (today): together
        they are the audit trail the brief asks for. Commit, return decisionID.

        This is the centre of the workflow. A complete "approve" usually does
        three writes together:
          1. ReviewDecision.create(...)          record the ruling + audit
          2. AccessRequest.update_status(...)    mark the request Approved
          3. CollectionItem.update_status(...)   set the item's access status
        Do all three so the data stays consistent.
        """
        cur = _get_cursor()
        cur.execute(
            "INSERT INTO ReviewDecision "
            "(requestID, reviewerID, decisionType,decisionNotes, accessConditions, decisionDate) " 
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (requestID, reviewerID, decisionType,decisionNotes, accessConditions, date.today())
        )
        from project import mysql
        mysql.connection.commit()
        new_decision = cur.lastrowid
        cur.close()
        return new_decision
  

    @staticmethod
    def get_by_request(request_id):
        """SELECT the decision(s) for a request. Shown in the request history."""
        cur = _get_cursor()
        cur.execute(
            """
            SELECT
                rd.decisionID,
                rd.requestID,
                rd.reviewerID,
                rd.decisionType,
                rd.decisionNotes,
                rd.accessConditions,
                rd.decisionDate,
                u.fullName,
                u.roleID,
                u.username,
                u.email
            FROM ReviewDecision rd
                JOIN `User` u
                    ON rd.reviewerID = u.userID
            WHERE rd.requestID = %s
            ORDER BY rd.decisionDate
            """,
            (request_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
    
    @staticmethod
    def get_all_by_item(item_id):
        """
        SELECT all review decisions by item_id. Returns a list. Sorted by newest first.
        """
        cur = _get_cursor()
        cur.execute(
            """
            SELECT
                rd.decisionID,
                rd.requestID,
                rd.reviewerID,
                rd.decisionType,
                rd.decisionNotes,
                rd.accessConditions,
                rd.decisionDate,
                u.fullName,
                u.roleID,
                r.roleName
            FROM ReviewDecision rd
                JOIN `User` u
                    ON rd.reviewerID = u.userID
                JOIN `Role` r   
                    ON u.roleID = r.roleID
            WHERE rd.requestID = %s
            ORDER BY rd.decisionDate DESC
            """,
            (item_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows


class CommunityComment:
    """A reviewer's note on a request. Several reviewers can comment on one."""

    def __init__(self, commentID=None, requestID=None, reviewerID=None,
                 commentText=None, createdDate=None):
        self.commentID = commentID
        self.requestID = requestID
        self.reviewerID = reviewerID
        self.commentText = commentText
        self.createdDate = createdDate

    @staticmethod
    def add_comment(requestID, reviewerID, commentText):
        """
        INSERT a comment against a request. Stamp createdDate (today). Commit,
        return the new commentID.
        """
        cur = _get_cursor()
        cur.execute(
            "INSERT INTO CommunityComment "
            "(requestID, reviewerID, commentText, createdDate) " 
            "VALUES (%s, %s, %s, %s)",
            (requestID, reviewerID, commentText, date.today())
        )
        from project import mysql
        mysql.connection.commit()
        new_comment = cur.lastrowid
        cur.close()
        return new_comment

    @staticmethod
    def get_by_request(request_id):
        """
        SELECT all comments for a request, oldest first, ideally JOINed to User
        so the page can show each reviewer's name. Returns a list.
        """
        cur = _get_cursor()
        cur.execute(
            """
            SELECT
                cc.commentID,
                cc.requestID,
                cc.reviewerID,
                cc.commentText,
                cc.createdDate,
                u.roleID,
                u.fullName
            FROM CommunityComment cc
                JOIN `User` u
                    ON cc.reviewerID = u.userID
            WHERE cc.requestID = %s
            ORDER BY cc.createdDate
            """,
            (request_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
      
