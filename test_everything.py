from app import app, views, models, db, menu_views
from app.models import Total
from app.views import *
from app.menu_views import *
import pytest

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


def test_add_event():

    title_data = "Test Event somewhere in the fucking world hhgdkhfjhjfd"
    location_data = "UCD where dumb ass peeps go"
    description_data = "Test yes indeed, it's a test...  rjhgrhgrk"

    event = Event(
        title=title_data,
        location=location_data,
        description=description_data
    )
    title_data = "Test Event somewhere in the fucking world no nono"
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
    assert events[0].location == events[0].location

#def test_send_emails():
    #server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.ehlo()
    #server.starttls()
    #assert server.login("event.management.tcd@gmail.com", "tcdtcd12") == True
