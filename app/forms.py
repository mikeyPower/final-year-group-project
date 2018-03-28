from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, FileField, BooleanField, TextAreaField, IntegerField, DateTimeField, DecimalField,SelectField,SelectMultipleField,DateField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
from app import models, db
from app.models import User


class LoginForm(Form):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
    email = StringField('Email Address:')
    last_name = StringField('Last name:', validators=[DataRequired()])
    first_name = StringField('First name:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired()])
    phone = StringField('Phone:')
    has_dietary_requirements = BooleanField('Special Dietary Requirements')
    dietary_requirements = TextAreaField('Describe your dietary requirements:')

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
    month = SelectField(
        'Month',
        choices=[('01', 'Jan'), ('02', 'Feb'), ('03', 'Mar'), ('04', 'Apr'), ('05', 'May'), ('06', 'Jun'),
                 ('07', 'Jul'), ('08', 'Jul'), ('09', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')],
        validators=[DataRequired()]
    )
    day = SelectField(
        'Day',
        choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'),
                 ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'),
                 ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')],
        validators=[DataRequired()]
    )
    year = SelectField(
        'Year',
        choices=[('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'),
                 ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'), ('2037', '2037'),
                 ('2038', '2038'), ('2039', '2039'), ('2040', '2040'), ('2041', '2041'), ('2042', '2042'), ('2043', '2043'), ('2044', '2044'), ('2045', '2045'), ('2046', '2046'), ('2047', '2047'),
                 ('2048', '2048'), ('2049', '2049'), ('2050', '2050'), ('2051', '2051'), ('2052', '2052'), ('2053', '2053'), ('2054', '2054'), ('2055', '2055'), ('2056', '2056'), ('2057', '2057'),
                 ('2058', '2058'), ('2059', '2059'), ('2060', '2060'), ('2061', '2061'), ('2062', '2062'), ('2063', '2063'), ('2064', '2064'), ('2065', '2065'), ('2066', '2066'), ('2067', '2067'),
                 ('2068', '2068'), ('2069', '2069'), ('2070', '2070'), ('2071', '2071'), ('2072', '2072'), ('2073', '2073'), ('2074', '2074'), ('2075', '2075'), ('2076', '2076'), ('2077', '2077'),
                 ('2078', '2078'), ('2079', '2079'), ('2080', '2080'), ('2081', '2081'), ('2082', '2082'), ('2083', '2083'), ('2084', '2084'), ('2085', '2085'), ('2086', '2086'), ('2087', '2087'),
                 ('2088', '2088'), ('2089', '2089'), ('2090', '2090'), ('2091', '2091'), ('2092', '2092'), ('2093', '2093'), ('2094', '2094'), ('2095', '2095'), ('2096', '2096'), ('2097', '2097'),
                 ('2098', '2098'), ('2099', '2099'), ('2100', '2100'), ('2101', '2101'), ('2102', '2102'), ('2103', '2103'), ('2104', '2104'), ('2105', '2105'), ('2106', '2106')],
        validators=[DataRequired()]
    )
    start_time = StringField('Start time', validators=[DataRequired()])
    description = TextAreaField('Desription')

class GroupEmailForm(Form):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body',validators=[DataRequired()])

class SearchAdminForm(Form):
    username = StringField('Name', validators=[DataRequired()])

class EmailAddresses(Form):
    addresses = StringField('Email Addresses:', validators=[DataRequired()])

class EmailAddresses2(Form):
    title = StringField('Title:', validators=[DataRequired()])
    addresses = StringField('Email Addresses:', validators=[DataRequired()])

class PastebinEntry(Form):
    language = SelectMultipleField(
        'Programming Language',
        choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    )
class EditAccountForm(Form):
    email = StringField('Email Address:')
    last_name = StringField('Last name:', validators=[DataRequired()])
    first_name = StringField('First name:', validators=[DataRequired()])
    phone = StringField('Phone:')
    has_dietary_requirements = BooleanField('Special Dietary Requirements')
    dietary_requirements = TextAreaField('Describe your dietary requirements:')
