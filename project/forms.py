# ============================================================
# IFQ582 Assignment 2 | Group 1D | Forms
# ============================================================

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

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
# TODO

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