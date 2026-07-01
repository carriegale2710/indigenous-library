"""IFQ582 Decorators - Role-based Permissions for the Indigenous Collections System


- Users must not be able to access, modify, or manipulate data outside their assigned role permissions
- Access control must be enforced at the route level using custom decorators (e.g., @admin_required)
or Flask-Login session-based role checks
- Unauthorised access attempts must be handled gracefully (e.g., redirect to login or show an
appropriate error page)
- Do not use Flask-Admin. """


from functools import wraps
from flask import redirect, url_for, g, flash, request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('You must be logged in to perform this action.', 'info')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user is None:
                flash('You must be logged in to perform this action.', 'info')
                return redirect(url_for('auth.login', next=request.path))
            if g.user['roleID'] not in allowed_roles:
                flash('You do not have permission to access this page', 'danger')
                return redirect(url_for('views.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator




