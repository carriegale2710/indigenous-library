# ============================================================
# IFQ582 Assignment 2 | Group 1D | Forms
# ============================================================
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, PasswordField, FileField, BooleanField, DateField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileAllowed
from project.model import User


# ------------------------------------------------------------
# Access Request Form — Rebecca
# ------------------------------------------------------------
class AccessRequestForm(FlaskForm):
    requestReason = TextAreaField('Reason for Request', validators=[DataRequired()])
    supportingDocuments = FileField('Supporting Documents', validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]) #changed to FileField for supporting documents
    submit = SubmitField('Submit Request')

# ------------------------------------------------------------
# Registration Form — Rebecca
# ------------------------------------------------------------
class RegistrationForm(FlaskForm):
    fullName = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters.')])
    confirmPassword = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    agreeTerms = BooleanField('I agree to follow the access conditions, privacy expectations and responsible use requirements of the Indigenous Academic Library.', validators=[DataRequired(message='You must check this box.')])
    submit = SubmitField('Create Account')

    # Handle mySQLdb Integrity errors from duplicate entries
    def validate_username(self, field):
        if User.get_by_username(field.data.strip()):
            raise ValidationError("That username is already taken.")

    def validate_email(self, field):
        if User.get_by_email(field.data.strip().lower()):
            raise ValidationError("That email is already registered.")
        
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
    nextReviewDate = DateField('Next Review Date', validators=[Optional()])
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
# Community Comment Form — pending team confirmation (Carrie)
# ------------------------------------------------------------
class CommunityCommentForm(FlaskForm):
    commentText = TextAreaField('Add Comment', validators=[DataRequired()])
    submit =  SubmitField('Submit Comment')

# ------------------------------------------------------------
# Review Decision Form — Carrie
# ------------------------------------------------------------
class RequiredIfDecision: # for accessConditions validation logic
    def __call__(self, form, field):
        if form.decisionType.data == "approve" and not field.data:
            raise ValidationError("Access Conditions are required when approving.")

class ReviewDecisionForm(FlaskForm):
    decisionType = SelectField('Decision Type', choices=[('Approve', 'Approve'), ('Reject', 'Reject')], validators=[DataRequired()])
    decisionNotes = TextAreaField('Decision Notes', validators=[Optional()])
    accessConditions = TextAreaField('Access Conditions', validators=[RequiredIfDecision()]) 
    submit = SubmitField('Submit Review Decision')

# ------------------------------------------------------------
# Login Form — Carrie
# ------------------------------------------------------------
class LoginForm(FlaskForm):
    email = StringField('Enter your email address', validators=[DataRequired(), Email()])  
    password = PasswordField('Enter your password', validators=[DataRequired()])
    submit = SubmitField('Log In')