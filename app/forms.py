from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, FileField, BooleanField, TextAreaField, IntegerField, DateTimeField, DecimalField
from wtforms import StringField, PasswordField, FileField, BooleanField, TextAreaField, IntegerField, DateTimeField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField


class LoginForm(Form):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
    email = StringField('Email Address:', validators=[DataRequired()])
    last_name = StringField('Last name:', validators=[DataRequired()])
    first_name = StringField('First name:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired()])

class ChangePassForm(Form):
    oldPassword = PasswordField('Old Password:', validators=[DataRequired()])
    newPassword = PasswordField('New Password:', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password:', validators=[DataRequired()])

class MenuForm(Form):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body')


class EventForm(Form):
    title = StringField('Title:', validators=[DataRequired()])
    location = TextAreaField('Location',validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    start_time = StringField('Start time', validators=[DataRequired()])
    description = TextAreaField('Desription')

class GroupEmailForm(Form):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body',validators=[DataRequired()])

class SearchAdminForm(Form):
    username = StringField('Name', validators=[DataRequired()])

class EmailAddresses(Form):
    addresses = StringField('Email Addresses:', validators=[DataRequired()])

<<<<<<< HEAD
class PastebinEntry(Form):
    language = SelectMultipleField(
        'Programming Language',
        choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    )

=======
class MoneyRaisedForm(Form):
    source = StringField('Source:', validators=[DataRequired()])
    money_raised = DecimalField('Money Raised:', validators=[DataRequired()])
>>>>>>> 9132924af32a0503e614ab3785d25479b1aa1cfb
