#!flask/bin/python
from app import app, db, models
from app.models import User, Menu, Total, Event, Guest

def clean_all():
    clean_menu()
    clean_user()
    clean_event()
    clean_total()

def clean_menu():
    db.session.query(Menu).delete()
    db.session.commit()

def clean_user():
    db.session.query(User).delete()
    db.session.commit()


def clean_event():
    db.session.query(Event).delete()
    db.session.commit()

def clean_total():
    db.session.query(Total).delete()
    db.session.commit()
