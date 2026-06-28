# ============================================================
# IFQ582 Assignment 2 | Group 1D | Authorisation - Register/Login/Logout
# ============================================================
from flask import  Blueprint, g, session, redirect, render_template, url_for,flash
from werkzeug.security import  generate_password_hash
from project.model import User
from project.forms import RegistrationForm, LoginForm
from sqlalchemy.exc import IntegrityError

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
        # TODO - Add error handling for MySQLdb.IntegrityError for duplicate usernames/emails

        try:
            user = User.create(roleID,fullName,username, email, passwordHash)   

            if user is None:
                flash("Registration failed. Please try again.", "danger")
                return render_template("error.html", error_code = 500)
            
            flash(f"Registration for email {email} successful. UserID = {user}", "success")
            return redirect(url_for("auth.login"))
        
        except IntegrityError:
            # Required after failed insert/commit when using ORM/session patterns
            session.rollback()
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
        
        # Store user details in new logged in session
        if error is None:
            session.clear()
            session['userID'] = user['userID']
            session['fullName'] = user['fullName']
            session['username'] = user['username']
            session["email"] = user['email']

            flash(f"Login for username '{session['username']}' with email '{session['email']}' successful.", "success")
            return redirect(url_for('views.catalogue'))
        
        flash(error, "danger")

    return render_template('auth/login.html', form=form) 

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
