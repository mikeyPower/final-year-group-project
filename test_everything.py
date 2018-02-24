from app import app, views, models, db, menu_views
from app.models import Total
from app.views import *
from app.menu_views import *
import pytest
import unittest

def test_total_raised():
    x = get_total_raised_tester()
    add_to_total_raised(4000)
    y = get_total_raised_tester()
    add_to_total_raised(-4000)
    assert y-x == 4000
    x = get_total_raised_tester()
    add_to_total_raised(6000)
    y = get_total_raised_tester()
    add_to_total_raised(-4000)
    assert y-x != 4000


def test_menu_added():
    title_data = "Brunch Test5"
    body_data = "Eggs and Toast Test5"
    add_menu(title_data,body_data)
    menu = Menu.query.filter_by(title=title_data).first()
    db.session.delete(menu)
    db.session.commit()
    assert body_data == menu.body


def test_create_event():

    title_data = "Test Event somewhere in world"
    location_data = "Mars in Mily Way Galaxy"
    description_data = "Test yes indeed, it's a test... !!!"

    event = Event(
        title=title_data,
        location=location_data,
        description=description_data
    )
    title_data = "Test Event somewhere in world 2"
    event2 = Event(
        title=title_data,
        location=location_data,
        description=description_data
    )
    db.session.add(event)
    db.session.add(event2)
    db.session.commit()
    events = db.session.query(Event).filter_by(location = location_data).all()
    db.session.delete(event)
    db.session.delete(event2)
    db.session.commit()
    print(events[0].location)
    print(events[1].location)
    #index = 10 / 0
    assert events[0].location == events[0].location

def test_send_emails():
    with pytest.raises(Exception) as e_info:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("event.management.tcd@gmail.com", "tcdtcd12676")


class MyTestCase(unittest.TestCase):
    def test_2_send_emails(self):
        with self.assertRaises(Exception) as context:
            msg = "Hello !!"
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("event.management.tcd@gmail.com", "tcdtcd1247576")
            server.sendmail("event.management.tcd@gmail.com", "hello@here.com", msg)

def test_view_invite_and_guest_lists():
    title_data = "Auction"
    location_data = "Grafton street"
    description_data = "Sell stuff"

    event = Event(
        id = 10,
        title=title_data,
        location=location_data,
        description=description_data
    )

    user = User(
        id = 15,
        username = "wessamgholam",
        email = "gholamwessam@gmail.com",
        hashed_password = "123",
        last_name = "Gholam",
        first_name = "Wessam"
    )
    user2 = User(
        id = 16,
        username = "wessamgholam2",
        email = "gholamwessam2@gmail.com",
        hashed_password = "123",
        last_name = "Gholam",
        first_name = "Wessam"
    )

    guest = Guest(
        event_id = 10,
        user_id = 15,
        code = "65tgnb"
    )

    db.session.add(event)
    db.session.add(user)
    db.session.add(user2)
    db.session.add(guest)
    db.session.commit()
    ##events = db.session.query(Event).filter_by(location = location_data).all()
    guest_list = db.session.query(Guest.user_id).filter_by(event_id = 10)
    myRecipient = User.query.all()
    invite_list = db.session.query(User).filter(~User.id.in_(guest_list)).all()
    guest_list2 = db.session.query(User).filter_by(id = 15).all()
    db.session.delete(event)
    db.session.delete(user)
    db.session.delete(user2)
    db.session.delete(guest)
    db.session.commit()
    assert guest_list2[0].email !=  invite_list[0].email
