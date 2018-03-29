from app import app, views, models, db, menu_views
from app.models import Total
from app.views import *
from app.menu_views import *
import pytest
import unittest

#Testing email syntax functionality
def test_email_syntax():
    x = 'testemail@gmail.com'
    y = 'wrongEmail@gmail.com'
    z =  'incorrect@gmail'
    assert verifyEmailSynatax(x) == True
    assert verifyEmailSynatax(y) ==  False
    assert verifyEmailSynatax(z) ==  False


#Testing register functionality
def test_try_register():
    email ='testemail1@gmail.com'
    name ='testemail1@gmail.com'
    password ='testPassword'
    confirm_pass = 'testPassword'
    f_name ='michael'
    l_name ='power'
    has_reqs=False
    reqs=None
    phone='086666666'
    assert try_register(email,name,password,confirm_pass,f_name,l_name,has_reqs,reqs,phone) == False
    reg = User.query.filter_by(email=email).first()
    db.session.delete(reg)
    db.session.commit()




def test_menu_added():
    title_data = "Brunch Test5"
    body_data = "Eggs and Toast Test5"
    upload =False
    add_menu(title_data,body_data,upload)
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

def test_event_update():
    title_data = "Test Event somewhere in world"
    location_data = "Mars in Mily Way Galaxy"
    description_data = "Test yes indeed, it's a test... !!!"

    event = Event(
        title=title_data,
        location=location_data,
        description=description_data
    )
    old_title = event.title
    db.session.add(event)
    db.session.commit()
    ev2 = db.session.query(Event).filter_by(title = old_title).first_or_404()
    ev2.title = "this is a new title"
    db.session.add(ev2)
    db.session.commit()
    ev3 = db.session.query(Event).filter_by(title = "this is a new title").first_or_404()
    assert ev3.title != old_title
    db.session.delete(ev3)
    db.session.commit()

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

def test_eticketing():
    email ='testemail3@gmail.com'
    name ='testemail3@gmail.com'
    password ='testPassword'
    confirm_pass = 'testPassword'
    f_name ='John'
    l_name ='M'
    has_reqs=False
    reqs=None
    phone='086666666'
    assert try_register(email,name,password,confirm_pass,f_name,l_name,has_reqs,reqs,phone) == False
    u = User.query.filter_by(email=email).first()

    title_data = "Cool Event"
    location_data = "Drawda"
    description_data = "Test yes indeed, it's a test... !!!"
    event = Event(
        title=title_data,
        location=location_data,
        description=description_data
    )
    db.session.add(event)
    db.session.commit()
    e = Event.query.all()[-1]
    assert e.title == title_data
    assert assign_ticket(e.id,u.id) != None
    assert assign_ticket(e.id,u.id) == None
    rem_guest_tester(e.id,u.id)
    db.session.delete(e)
    db.session.delete(u)
    db.session.commit()


##test admin##
def test_creating_admin():
    usr=User(username="billjoe123",email="mytesteremail@test.com",hashed_password="123",last_name="joe",first_name="billy")
    db.session.add(usr)
    db.session.commit()
    assert usr.admin==False
    admin_test_function(usr.username)
    assert usr.admin==True
    db.session.delete(usr)
    db.session.commit()

########END########

def test_mailing_list():
    ml = Mailing_list(title = 'test_mailing_list')
    db.session.add(ml)
    db.session.commit()
    assert ml.title=='test_mailing_list'
    db.session.delete(ml)
    db.session.commit()

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

def keep_track_all_users():
    user = User(
        id = 15,
        username = "wessamgholam",
        email = "gholamwessam@gmail.com",
        hashed_password = "123",
        last_name = "Gholam",
        first_name = "Wessam"
    )
    db.session.add(user)
    db.session.commit()
    assert user in User.query.all()
    db.session.delete(user)
    db.session.commit()


def test_guests_add_and_remove():
    title_data = "Auction"
    location_data = "Grafton street"
    description_data = "Sell stuff"

    event = Event(
        id=10,
        title=title_data,
        location=location_data,
        description=description_data
    )

    user = User(
        id=15,
        username="bizzzzboi",
        email="tstus@gmail.com",
        hashed_password="123",
        last_name="dude",
        first_name="my"
    )
    user2 = User(
        id=16,
        username="lzzzzzzilboi",
        email="sectstusr@gmail.com",
        hashed_password="123",
        last_name="boujee",
        first_name="bad"
    )

    g = Guest(
        event_id=10,
        user_id=15,
        user = user,
        code="65nb"
    )

    g2 = Guest(
        event_id=10,
        user_id=16,
        user=user2,
        code="65nb"
    )

    db.session.add(event)
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()
    auc = db.session.query(Event).filter_by(id = 10).first_or_404()
    auc.guests.append(g)
    auc.guests.append(g2)
    db.session.commit()
    print(auc.guests)
    assert g in auc.guests
    auc.guests.remove(g)
    db.session.commit()
    assert g not in auc.guests
    auc.guests.remove(g2)
    db.session.delete(event)
    db.session.delete(user)
    db.session.delete(user2)
    db.session.commit()


def test_admin():
    reg = User.query.filter_by(username='Admin').first_or_404()
    assert reg is not None
