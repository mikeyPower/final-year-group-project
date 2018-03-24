from app import db
from wtforms import Form, StringField, TextAreaField, PasswordField, DateField, validators
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship, backref


#Many-To-Many
#users_in_mailing_list = db.Table('emails_in_mailing_list',
#    db.Column('user', db.Integer, db.ForeignKey('user.id')),
#    db.Column('mailing_list', db.Integer, db.ForeignKey('mailing_list.id'))
#)

#association_table = db.Table('items_users',
#    db.Column('user', db.Integer, db.ForeignKey('user.id')),
#    db.Column('mailing_list', db.Integer, db.ForeignKey('mailing_list.id'))
#)

#keep save
#class Recipient(db.Model):
#    __tablename__ = 'recipient'
#    user_id = db.Column( db.Integer, db.ForeignKey('user.id'), primary_key=True)
#    mailing_list_id = db.Column( db.Integer, db.ForeignKey('mailing_list.id'), primary_key=True)
#    user = db.relationship("User")

class Recipient(db.Model):
    __tablename__ = 'recipient'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column( db.Integer, unique=True)
    mailing_list_idd = db.Column( db.Integer, unique=True)

class Non_user_recipient(db.Model):
    __tablename__ = 'non_user_recipient'
    id = db.Column(db.Integer, primary_key=True)
    mailing_list_idd = db.Column( db.Integer, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)




class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default = False)
    deleted = db.Column(db.Boolean, default=False)
    last_name = db.Column(db.String(20), index=True)
    first_name = db.Column(db.String(20), index=True)
    #mailing_list = relationship('Mailing_list', secondary=association_table, lazy='dynamic', backref=backref('user', lazy='dynamic'))
    #mailing_list = relationship("Mailing_list", secondary="users_mailing_list")
    #users_in_mailing_list = db.relationship('Mailing_list', secondary=users_in_mailing_list,
        #backref=db.backref('user'))

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


#Many-To-Many
#   guests = db.Table('guests',
#    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#    db.Column('code', db.String(64))
#)
class Guest(db.Model):
    __tablename__ = 'guest'
    event_id = db.Column( db.Integer, db.ForeignKey('event.id'), primary_key=True)
    user_id = db.Column( db.Integer, db.ForeignKey('user.id'), primary_key=True)
    code = db.Column( db.String(64))
    user = db.relationship("User")

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    location = db.Column(db.String(120), index=True)
    date = db.Column(db.String(30))
    start_time = db.Column(db.String(30))
    description = db.Column(db.String(1000))
    guests = db.relationship("Guest", backref = "event", cascade="all, delete-orphan")
    moneyraised = db.relationship('MoneyRaised', backref='event', lazy=True)
    #guests = db.relationship('User', secondary=guests, lazy='subquery', backref=db.backref('events', lazy=True))

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #unique=True
    body = db.Column(db.String(1000))
    created_time = db.Column(db.String(100))

#money raised at an event and where it came from
class MoneyRaised(db.Model):
    __tablename__ = 'moneyraised'
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float)
    source = db.Column(db.String(512))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.String(50))

class Mailing_list(db.Model):
    __tablename__ = 'mailing_list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True) #unique=True
    #recipients = db.relationship("Recipient", backref = "recipient", cascade="all, delete-orphan")
    #user = relationship("User",secondary="users_mailing_list")

#Many-To-Many
#class Users_in_mailing_list(db.Model):
#    __table__ = 'users_mailing_list'
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id')),
#    mailing_list_id = db.Column(db.Integer, db.ForeignKey('mailing_list.id'))
#    user = relationship(User,backref=backref("users_mailing_list",cascade="all, delete-orphan"))
#    mailing_list = relationship(Mailing_list,backref=backref("users_mailing_list",cascade="all, delete-orphan"))

#Many-To-Many
#guests = db.Table('guests',
#    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#    db.Column('code', db.String(64))
#)


#class Ticket(db.Model):
#    __tablename__= 'ticket'
#    id = db.Column(db.Integer, primary_key=True)
#    code = db.Column(db.String(64), index=True, unique=True)
#    event_id = db.Column(db.Integer, db.ForeignKey('event.id'),nullable=False)

#class Buyer(db.model):
    #__tablename__ = 'buyer'
    #id = db.Column(db.Integer, primary_key=True)
    #code = db.Column(db.String(64), index=True, unique=True)
    #event_id = db.Column(db.Integer, db.ForeignKey('event.id'),
        #nullable=False)
