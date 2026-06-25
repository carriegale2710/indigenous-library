# ============================================================
# IFQ582 Assignment 2 | Group 1D | Forms
# ============================================================

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, Length


# ------------------------------------------------------------
# Access Request Form — Rebecca
# ------------------------------------------------------------
class AccessRequestForm(FlaskForm):
    requestReason = TextAreaField('Reason for Request', validators=[DataRequired()])
    supportingDocuments = StringField('Supporting Documents', validators=[Optional()])
    submit = SubmitField('Submit Request')

# ------------------------------------------------------------
# Registration Form — Rebecca
# ------------------------------------------------------------
class RegistrationForm(FlaskForm):
    fullName = StringField('Enter your Full Name', validators=[DataRequired()])
    username = StringField('Enter your username', validators=[DataRequired()])
    email = StringField('Enter your email address', validators=[DataRequired(), Email()])
    password = PasswordField('', validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField('', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit Registration')

# ------------------------------------------------------------
# Collection Item Form — Rebecca
# ------------------------------------------------------------
# TODO

# ------------------------------------------------------------
# Cultural Metadata Form — Rebecca
# ------------------------------------------------------------
# TODO

# ------------------------------------------------------------
# Community Comment Form — pending team confirmation (Rebecca?)
# ------------------------------------------------------------
# TODO

# ------------------------------------------------------------
# Review Decision Form — Carrie
# ------------------------------------------------------------
# TODO

# ------------------------------------------------------------
# Login Form — Carrie
# ------------------------------------------------------------
# TODO