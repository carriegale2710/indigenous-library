from functools import wraps
from flask import redirect, url_for, g, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('You must be logged in to perform this action.', 'info')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user is None:
                flash('You must be logged in to perform this action.', 'info')
                return redirect(url_for('auth.login'))
            if g.user['roleID'] not in allowed_roles:
                flash('You do not have permission to access this page', 'danger')
                return redirect(url_for('views.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator




