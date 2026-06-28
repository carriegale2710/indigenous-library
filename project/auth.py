# ============================================================
# IFQ582 Assignment 2 | Group 1D | Authorisation - Register/Login/Logout
# ============================================================
from flask import  Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from project.forms import RegistrationForm, LoginForm
from project import mysql
import MySQLdb

# The authentication blueprint will have views to register new users and to log in and log out.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=('GET','POST'))
def register():
    """
    USER REGISTRATION VIEW

    Allows user to fill and submit account registration form.

        1. When the user visits the `/auth/register` URL endpoint from nav link.
            -> Return register form template for user to fill out. 

        2. When user submits the form, this function will validate and save their details to DB:
            -> If invalid, will show the form again with an error message. 
            -> If Valid, will create the new user row in DB with hashed password -> Redirects to the login page.
    """
    
    form = RegistrationForm()

    if form.validate_on_submit():
        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        cur = mysql.connection.cursor()
        error = None

        # Save to mySQL database
        try:
            cur.execute(
                "INSERT INTO user (fullname, username, email, passwordHash) VALUES (%s, %s, %s, %s)",
                (fullname, username, email, generate_password_hash(password)) # NOTE : For security, never store raw password! Always hash!
            )
            mysql.connection.commit()
        except MySQLdb.IntegrityError:
            error = f"User {username} or email {email} is already registered."
        finally:
            cur.close()

        if error is None:
            flash("Temporary registration submitted successfully.", "success")
            return redirect(url_for("auth.login"))
            
        flash(error, "error")
           
    return render_template('auth/register.html', form=form) 

@auth_bp.route('/login', methods=('GET','POST'))
def login():
    """
    USER LOGIN VIEW

    Allows user to log into their account.

    User is Shown login form -> types in email and password -> submits form
        1. If Invalid input: show error message -> redirect to login page
        2. If Valid input: -> create new session with user_id saved as cookie (to stay logged in)

    """

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cur = mysql.connection.cursor()

        # Search user database with inputted email
        cur.execute('SELECT * FROM user WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()

        error = None

        # Error handling
        if user is None or not check_password_hash(user['passwordHash'],password):
            error = 'Incorrect email or password.' # NOTE: Security measure - So attackers don't know if email is in a database.
        
        # Store user details in new login session
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['fullname'] = user['fullname']
            session["email"] = user['email']

            flash("Temporary login successful.", "success")
            return redirect(url_for('views.catalogue'))
        
        flash(error, "error")

    return render_template('auth/login.html', form=form) 

@auth_bp.before_app_request 
def load_logged_in_user():
    """
    USER LOGIN STATUS CHECK

    Checks if user is logged in or not.

    At start of each request, this function checks if a user id in stored in the current session. 
        1. If a user is logged: User info is loaded in session and made available to other views for length or request.
        2. If user not logged in: g.user will be None, no data stored in current session.
    """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM user WHERE id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()


@auth_bp.route('/logout')
def logout():
    """
    USER LOGOUT 

    Logs out the user. 
    
    This will clear all data from current session, including user_id. Redirects to index page.
    """
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))