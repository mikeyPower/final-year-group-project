from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm, menu_views
from app.menu_views import *
from flask import g,render_template, flash, redirect, session, Flask, url_for, request
from .forms import LoginForm, RegisterForm, MenuForm,ChangePassForm, GroupEmailForm, EventForm
from .models import User, Menu, Total, Event, Guest
from flask_table import Table, Col, LinkCol
from flask_wtf import Form as BaseForm
from functools import wraps
from passlib.hash import sha256_crypt
import smtplib
import os
import email.encoders
import email.mime.text
import email.mime.base
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import jsonify
import re
import random
import string


def verifyEmailSynatax(addressToVerify):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

    if match == None:
	    return False
    else:
        return True

def add_menu(title,body):
    title = form.title.data
    body = form.body.data

    menu = Menu(
      title = title,
      body = body
    )
    db.session.add(menu)
    db.session.commit()
    return



#######admin stuff########

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not g.user.admin :
                #flash("you are not an admin")
                return render_template('access_denied.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@app.route("/create_admin", methods=['POST', 'GET'])
@login_required
def create_admin():
    users = User.query.filter_by(admin=False).all()
    return render_template('create_admin.html', users = users)

#######end admin##########




@app.route('/index')
@login_required
def index():
    return render_template('index.html')

# Manage mailing list
@app.route('/email', methods=['GET', 'POST'])
@login_required
def email():
    #db.session.query(Recipient).delete()
    #db.session.commit()
    form = MailingForm()
    #myRecipient = recipient.query.all()
    recipient = Recipient(
        email = form.email.data,
        last_name = form.last_name.data,
        first_name = form.first_name.data
    )
    if request.method == 'POST':
        form = MailingForm()
        flash('Added')
        print("Added!!")
        db.session.add(recipient)
        db.session.commit()
        myRecipient = recipient.query.all()
        return render_template('email.html', form = form, myRecipient = myRecipient)
    else:
        myRecipient = recipient.query.all()
        return render_template('email.html', form = form, myRecipient = myRecipient)



#<string:id>

#logic of how to register



# Send emails
@app.route('/send_emails/<int:ev_id>', methods=['GET', 'POST'])
@login_required
def send_email(ev_id):
    index = 0
    idd = id
    myRecipient = User.query.all()
    me = "Event Company"
    you = "Wessam Gholam"
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
    APP_STATIC = os.path.join(APP_ROOT, 'templates')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Invitation"
    msg['From'] = me
    msg['To'] = you
    text = "Hello!!!!!"
    myRecipient = User.query.all()
    result = Guest.query.with_entities(Guest.user_id)
    #answer = db.session.query.filter(~User.notin_(result))
    answer2 = db.session.query(Guest).filter(Guest.event_id != ev_id)
    #answer3 = db.session.query(Guest).filter(Guest.event_id != ev_id)
    answer4 = db.session.query(User.email).join(answer2)
    #answer5 = db.session.query(User.email).join(answer4)
    userList = db.session.query(Guest,User).filter_by(event_id=ev_id)
    answer100 = db.session.query(Guest)
    #answer44 = db.session.query(User.email).join(answer4)
    invite_list = db.session.query(User).join(answer2).all()
    #print(invite_list[0].email)
    #print(invite_list[1].email)


    for i in range(len(invite_list)):
        with open(os.path.join(APP_STATIC, 'invitation.html')) as f:
            html = f.read()
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(render_template("invitation.html",
                               myRecipient=invite_list[i], id = ev_id), 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("event.management.tcd@gmail.com", "tcdtcd12")
        server.sendmail("event.management.tcd@gmail.com", invite_list[i].email, msg.as_string())
        check = invite_list[i].last_name
        #print("Look here:**:", check)
        index = i
    return render_template('send_emails.html', myRecipient=invite_list)



@app.route('/',  methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    user = g.user
    form = LoginForm()
    if form.validate_on_submit():
        error = try_login(form.username.data, form.password.data)
        if not error:
            session['logged_in'] = True
            if user.admin:
                session['admin'] = True
            return redirect('/index')
    return render_template('login.html', form=form)


# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect('/login')




def try_login(name,password):
    user = User.query.filter_by(username=name).first()
    if user is not None:
        #if user.hashed_password == sha256_crypt.encrypt(str(password)):#password:
        if sha256_crypt.verify(str(password), user.hashed_password):
            login_user(user)
            return False
    return True

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        error =try_register(form.email.data, form.username.data, form.password.data, form.confirm.data,form.last_name.data,form.first_name.data)
        if not error:

            #Need to decide on Database
            #flash('you have sucessfully registered')
            return redirect('/login')
    return render_template('register.html', form = form)

#logic of how to register
def try_register(email,name,password,confirm_pass,f_name,l_name):
    #if (email is None) or (name is None) or (password is None) or (confirm_pass is None)
    if password != confirm_pass:
        flash(u'Password is incorrect', category='error')
        return True
    user = User.query.filter_by(username=name).first()
    if user is not None:
        flash(u'Username is already present', category='error')
        return True
    user = User.query.filter_by(email=email).first()
    if user is not None:
        flash(u'Email is already present', category='error')
        return True
    if verifyEmailSynatax(email) == False:
        flash(u'Email is not correct', category='error')
        return True
    user = User(
      username = name,
      email = email,
      hashed_password = sha256_crypt.hash(str(password)), #password , #Hashing added
      first_name = f_name,
      last_name = l_name
    )
    db.session.add(user)
    db.session.commit()
    return False



@app.before_request
def before_request():
    g.user = current_user

@app.route('/setting', methods=['GET','POST'])
@login_required
def settings():
    form = ChangePassForm()
    error = None
    if form.validate_on_submit():
        old = form.oldPassword.data
        new_pass = form.newPassword.data
        confirm = form.confirmPassword.data
        error = changePass(old, new_pass, confirm)
        if error is None:
            return redirect('/index')
        else:
            flash(error)
    return render_template('settings.html', form = form )

def changePass(old, new, confirm):
    usr = g.user
    error = "Old password is incorrect"
    if sha256_crypt.verify(str(old), usr.hashed_password):

        if new!=confirm:
            error = "new passwords do not match"
            flash(error)
            return error
        error=None
        password = sha256_crypt.hash(str(new))
        usr.hashed_password = password
        db.session.commit()
    return error


@app.route('/group_email', methods=['GET', 'POST'])
@login_required
def group_email():
    form = GroupEmailForm()
    if form.validate_on_submit():#
        print("your in")
        title = form.title.data
        body = form.body.data
        myRecipient = User.query.all()
        me = "Event Company"
        you = "Wessam Gholam"
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        APP_STATIC = os.path.join(APP_ROOT, 'templates')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = me
        msg['To'] = you
        text = "Hello!!!!!"
        print(title)
        print(body)
        myRecipient = User.query.all()
        for i in range(len(myRecipient)):
            with open(os.path.join(APP_STATIC, 'invitation.html')) as f:
                html = f.read()
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("event.management.tcd@gmail.com", "tcdtcd12")
            server.sendmail("event.management.tcd@gmail.com", myRecipient[i].email, msg.as_string())
        #flash('Email Sent', 'success')
        print("added")
        #return redirect('/menulist')
    return render_template('group_email.html', form = form)


#### Event page functions ########


@app.route('/events')
@login_required
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)


@app.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    form = EventForm()

    if form.validate_on_submit():
        title = form.title.data
        location = form.location.data
        description = form.description.data

        event = Event(
            title=title,
            location=location,
            description=description
        )
        db.session.add(event)
        db.session.commit()
        events = Event.query.all()
        return render_template('events.html', events=events)
    return render_template('add_event.html', form=form)

@app.route('/event/<ev_id>', methods=['GET', 'POST'])
@login_required
def event_details(ev_id):
    event = Event.query.filter_by(id=ev_id).first_or_404()
    return render_template('event.html', event=event)

@app.route('/event_del/<id>')
@login_required
def event_del(id):
    event = Event.query.filter_by(id=id).first_or_404()
    db.session.delete(event)
    db.session.commit()
    return redirect('/events')


@app.route('/event/<ev_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(ev_id):
    event = Event.query.filter_by(id=ev_id).first_or_404()
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.location = form.location.data
        event.description = form.description.data
        db.session.add(event)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('event_details', ev_id=event.id))
    else:
        form.title.data = event.title
        form.location.data = event.location
        form.description.data = event.description
    return render_template('add_event.html', form=form)

@app.route('/event/tickets/<int:id>', methods=['GET', 'POST'])
@login_required
def event_ticket(id):
    event = Event.query.filter_by(id=id).first_or_404()
    return render_template('tickets.html', event=event, event_title = event.title, location= event.location, id=id)

### Guest list functs ###

@app.route('/event/guests/<int:id>')
@login_required
def guest_list2(id):
    if request.method == 'POST':
        print('hi')

    event = Event.query.filter_by(id=id).first_or_404()
    guests = event.guests
    return render_template('guests.html', guests=guests, event=event)


@app.route('/event/event_tickets/<int:eventid>')
@login_required
def event_tickets(eventid):
    if request.method == 'POST':
        print('hi')
    alltickets =  Event.query.filter_by(id=eventid).first_or_404().guests
    return render_template('event_tickets.html', tickets=alltickets)




#Need to fidure out how I query assoctiaon table
@app.route('/event/guests/<string:id>/register', methods=['GET', 'POST'])
def add_guest_to_event(id):
    form = RegisterForm()
    event = Event.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        error =try_register(form.email.data, form.username.data, form.password.data, form.confirm.data,form.last_name.data,form.first_name.data)
        if not error:
            user =  User.query.filter_by(username=form.username.data).first_or_404()
            assign_ticket(id,user.id)
            return redirect(url_for('guest_list2', id=id))
            #return redirect(url_for('guests',guests=usrs, event=event))
            #return render_template('guests.html', guests=usrs, event=event)
    return render_template('register.html', form = form)


@app.route('/event/<int:id>/guests')
@login_required
def guest_list(id):
    if request.method == 'POST':
        print('hi')
    guestlist = Event.query.filter_by(id=id).first_or_404().guests
    return render_template('guests.html', guests = guestlist, event = Event.query.filter_by(id=id).first_or_404())


@app.route('/guests/<id>')
@login_required
def remove_guest(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    usrs = User.query.all()
    return render_template('guests.html', guests=usrs)


def get_total_raised():
    t = Total.query.get(1)
    if t is None:
        t2 = 0.0
    else:
        t2 = t.total
    return jsonify(current=t2)

def add_to_total_raised(x):
    t = Total.query.get(1)
    if t is None:
        ts = Total(total=x)
        db.session.add(ts)
    else:
        t.total += x
    db.session.commit()

def get_total_raised_tester():
    t = Total.query.get(1)
    if t is None:
        return 0
    else:
        return t.total

@app.route('/total-raised')
@login_required
def totalraised():
    return render_template('total-raised.html')

@app.route('/update-total-raised')
def updater():
    return get_total_raised()

#Following func used to generate ticket code, later will be checked against existing entry in DB and assigned to a guest in table
def generateTicketCode():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

def assign_ticket(event,user):
    x = generateTicketCode()
    #guests.insert().values(event_id=event, user_id=user, code=x)
    guestlist = Event.query.filter_by(id=event).first_or_404().guests
    u = User.query.filter_by(id=user).first_or_404()
    existsalready = False
    for guest in guestlist:
        if u.username == guest.user.username:
            existsalready = True

    if not existsalready:
        g = Guest(code=x)
        g.user = User.query.filter_by(id=user).first_or_404()
        e = Event.query.filter_by(id=event).first_or_404()
        e.guests.append(g)
        db.session.commit()
        return x
    else:
        return None

@app.route('/event/ticket/<int:eventid>')
@login_required
def ticket_view(eventid):
    ticket = assign_ticket(eventid,current_user.id)
    if ticket is not None:
        return render_template('ticket.html', code = ticket)
    else:
        t = ""
        guestlist = Event.query.filter_by(id=eventid).first_or_404().guests
        for g in guestlist:
            if g.user.username == current_user.username:
                t = g.code
        return render_template('already_ticketed.html', code = t)
