from app import db
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default = False)
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
    
    def __repr__(self):
        return '<User %r>' % (self.username)



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


#Many-To-Many
guests = db.Table('guests',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('guest_id', db.Integer, db.ForeignKey('guest.id'), primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    location = db.Column(db.String(120), index=True)
    description = db.Column(db.String(1000))
    guests = db.relationship('Guest', secondary=guests, lazy='subquery',
                           backref=db.backref('events', lazy=True))

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    body = db.Column(db.String(64), index=True, unique=True)




class Guest(db.Model):
    __tablename__ = 'guest'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(20), index=True)
    first_name = db.Column(db.String(20), index=True)
