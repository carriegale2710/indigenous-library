"""
# ============================================================
# IFQ582 Assignment 2 | Group 1D | Authorisation Layer
# ============================================================

"""
from flask import  Blueprint, abort, g, session, redirect, render_template, url_for,flash, request
from werkzeug.security import  generate_password_hash
from project.model import User
from project.forms import RegistrationForm, LoginForm
from MySQLdb import IntegrityError

# The authentication blueprint will have views to register new users and to log in and log out.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=('GET','POST'))
def register():
    """
    Allows user to fill and submit account RegistrationForm.

    1. When the user visits the `/auth/register` URL endpoint from nav link.
        -> Return register form template for user to fill out. 

    2. When user submits the form, this function will validate and save their details to DB:
        -> If invalid, will show the form again with an error message. 
        -> If Valid, will create the new user row in DB with hashed password -> Redirects to the login page.
    """
    
    form = RegistrationForm()


    if form.validate_on_submit():
        roleID = 4 # 'public user' role by default if role delegation can only be given by admin user
        fullName = form.fullName.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        passwordHash = generate_password_hash(password) # NOTE : For security, never store raw password! Always hash!


        # Save to mySQL database

        try:
            user = User.create(roleID,fullName,username, email, passwordHash)   

            if user is None:
                flash("Registration failed. Please try again.", "danger")
                abort(500)  # Internal Server Error
            
            flash(f"Registration for email {email} successful. UserID = {user}", "success")
            return redirect(url_for("auth.login"))
        
        except IntegrityError:
            # Duplicate username/email broke a UNIQUE constraint, so undo the failed INSERT.
            from project import mysql
            mysql.connection.rollback()
            form.email.errors.append("Registration failed due to a duplicate value.")
            
    return render_template('auth/register.html', form=form) 

@auth_bp.route('/login', methods=('GET','POST'))
def login():
    """
    Allows user to log into their account via LoginForm.

    User is Shown login form -> types in email and password -> submits form
        1. If Invalid input: show error message -> redirect to login page
        2. If Valid input: -> create new session with userID saved as cookie (to stay logged in)

    """

    form = LoginForm()

    if form.validate_on_submit():
        # username = form.username.data   # REVIEW - can the user log in with username too (instead of email)? 
        email = form.email.data
        password = form.password.data
        
        user = User.get_by_email(email)

        # Error handling
        error = None
        errorMessage = 'Incorrect email or password.' # NOTE: Security measure - Error message is generic on purpose so attackers don't know if email is in a database.

        if user is None:
            error = errorMessage
        elif not User.verify_password(user['passwordHash'], password):
            error = errorMessage
        elif user['accountStatus'] != 'active':
            error = 'This account is inactive. Please contact a library administrator.'
        
        # Store user details in new logged in session
        if error is None:
            session.clear()
            session['userID'] = user['userID']
            session['roleID'] = user['roleID']
            session['fullName'] = user['fullName']
            session['full_name'] = user['fullName']
            session['username'] = user['username']
            session["email"] = user['email']

            flash(f"Login for username '{session['username']}' with email '{session['email']}' successful.", "success")
            next_page = request.form.get('next') or request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('views.catalogue'))
        
        flash(error, "danger")

    return render_template('auth/login.html', form=form) 

# Add this route to project/auth.py, anywhere inside the auth_bp blueprint
# (e.g. directly below the existing login() route).
#
# It logs the visitor in as the seeded demo admin account ('smitchell',
# userID 1, roleID 1) with no password required. This account's data is
# restored on a short cycle by the scheduled reset (see
# .github/workflows/reset-demo.yml), so nothing a visitor does here sticks
# around for long.

@auth_bp.route('/demo-login')
def demo_login():
    """
    One-click login as the shared demo admin account, for portfolio visitors.

    Deliberately requires no password: it's meant to be a visible, obvious
    "try the full admin experience" button, not a real account. Session
    behaves identically to a normal login (same keys, same g.user wiring
    via load_logged_in_user), so every @role_required(1) route just works.
    """
    user = User.get_by_username('smitchell')

    if user is None or user['accountStatus'] != 'active':
        flash("Demo login is temporarily unavailable.", "danger")
        return redirect(url_for('auth.login'))

    session.clear()
    session['userID'] = user['userID']
    session['roleID'] = user['roleID']
    session['fullName'] = user['fullName']
    session['full_name'] = user['fullName']
    session['username'] = user['username']
    session['email'] = user['email']
    session['is_demo'] = True  # lets templates show a "you're in demo mode" banner

    flash(
        "You're browsing as the demo admin account. Changes reset automatically "
        "every few minutes, so feel free to explore freely.",
        "info"
    )
    return redirect(url_for('views.catalogue'))

@auth_bp.before_app_request 
def load_logged_in_user():
    """
    Checks if user is logged in or not.

    At start of each request, this function checks if a user id in stored in the current session. 
        1. If a user is logged: User info is loaded in session and made available to other views for length or request.
        2. If user not logged in: g.user will be None, no data stored in current session.
    """
    userID = session.get('userID')

    if userID is None:
        g.user = None
    else:
        g.user = User.get_by_id(userID)


@auth_bp.route('/logout')
def logout():
    """
    Logs out the user. 
    
    This will clear all data from current session, including userID. Redirects to index page.
    """
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))