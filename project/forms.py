# ============================================================
# IFQ582 Assignment 2 | Group 1D | Forms
# ============================================================

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, PasswordField, FileField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, Length
from flask_wtf.file import FileAllowed


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
class CollectionItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authorCreator = StringField('Author or Creator', validators=[DataRequired()])
    year = StringField('Year', validators=[Optional()])
    summary = TextAreaField('Summary', validators=[Optional()])
    collection = SelectField('Collection', choices=[], validators=[DataRequired()])
    itemType = SelectField('Item Type', choices=[('book','Book'), ('recording','Recording'),('image','Image'),('manuscript','Manuscript'),('resource','Resource')], validators=[DataRequired()])
    thumbnailPath = FileField('Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'svg'])])
    submit = SubmitField('Submit Item to Collection')


# ------------------------------------------------------------
# Cultural Metadata Form — Rebecca
# ------------------------------------------------------------
class CulturalMetadataForm(FlaskForm):
    communityGroup = StringField('Community Group', validators=[Optional()])
    language = StringField('Language', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    subjectArea = SelectField('Subject Area', choices=[('bush_medicine', 'Bush Medicine'),('ceremony','Ceremony'), ('childrens_literature',"Children's Literature"), ('community_life', 'Community Life'), ('healing_practices', 'Healing Practices'), ('initiation','Initiation'), ('land_management', 'Land Management'), ('land_and_sea_management', 'Land and Sea Management'), ('language','Language'), ('oral_history', 'Oral History'), ('painting','Painting'), ('sacred_site', 'Sacred Site'), ('songline', 'Songline'), ('weaving','Weaving')], validators=[Optional()])
    culturalSensitivityNotes = TextAreaField('Cultural Sensitivity Notes', validators=[Optional()])
    culturalProtocolNotes = TextAreaField('Cultural Protocol Notes', validators=[Optional()])
    accessRecommendations = TextAreaField('Access Recommendations', validators=[Optional()])
    submit = SubmitField('Submit Cultural Metadata')
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