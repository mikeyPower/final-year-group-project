from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, FileField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(Form):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
    email = StringField('Email Address:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired()])

class ChangePassForm(Form):
    oldPassword = PasswordField('Old Password:', validators=[DataRequired()])
    newPassword = PasswordField('New Password:', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password:', validators=[DataRequired()])

class MailingForm(Form):
    email = StringField('Email Address:', validators=[DataRequired()])
    last_name = StringField('Last name:', validators=[DataRequired()])
    first_name = StringField('First name:', validators=[DataRequired()])

class MenuForm(Form):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body',validators=[DataRequired()])
