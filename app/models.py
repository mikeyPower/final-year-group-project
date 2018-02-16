from app import db
#from passlib.apps import custom_app_context as pwd_context
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self):
        return not self.deleted

    @property
    def is_active(self):
        return not self.deleted

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
class Total(db.Model):
    __tablename__ = 'totalraised'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float,index=True)

    def __repr__(self):
        return '<Total %r>' % (self.total)

class Recipient(db.Model):
    __tablename__ = 'recipients'
    #id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    #email = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(20), index=True)
    first_name = db.Column(db.String(20), index=True)


    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3



class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    body = db.Column(db.String(64), index=True, unique=True)
