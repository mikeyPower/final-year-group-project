from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm
from flask import g,render_template, flash, redirect, session, Flask, url_for, request
from .forms import LoginForm, RegisterForm, MenuForm,ChangePassForm, GroupEmailForm, EventForm
from .models import User, Menu, Total, Event
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
def try_register_guest(email,f_name,l_name, form):
    #if (email is None) or (name is None) or (password is None) or (confirm_pass is None)
    if verifyEmailSynatax(email) == False:
        flash(u'Email is not correct', category='error')
        return True
    guest = Guest(
            email = email,
            last_name = l_name,
            first_name = f_name
        )
    db.session.add(guest)
    db.session.commit()
    return False


# Send emails
@app.route('/send_emails', methods=['GET', 'POST'])
@login_required
def send_email():
    index = 0
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
    for i in range(len(myRecipient)):
        with open(os.path.join(APP_STATIC, 'invitation.html')) as f:
            html = f.read()
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(render_template("invitation.html",
                               myRecipient=myRecipient[i]), 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("event.management.tcd@gmail.com", "tcdtcd12")
        server.sendmail("event.management.tcd@gmail.com", myRecipient[i].email, msg.as_string())
        check = myRecipient[i].last_name
        print("Look here:**:", check)
        index = i
    return render_template('send_emails.html', myRecipient=myRecipient)



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
        error =try_register(form.email.data, form.username.data, form.password.data, form.confirm.data)
        if not error:

            #Need to decide on Database
            #flash('you have sucessfully registered')
            return redirect('/login')
    return render_template('register.html', form = form)

#logic of how to register
def try_register(email,name,password,confirm_pass):
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
      hashed_password = sha256_crypt.hash(str(password)) #password , #Hashing added
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


@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    form = MenuForm()
    if form.validate_on_submit():#
        print("you're in")
        title = form.title.data
        body = form.body.data

        menu = Menu(
          title = title,
          body = body
        )
        db.session.add(menu)
        db.session.commit()

        #flash('Menu Created', 'success')
        print("added")
        return redirect('/menulist')
    return render_template('menu.html', form = form)


@app.route('/menu/<string:id>/')
@login_required
def menu_details(id):

    menu = Menu.query.filter_by(id=id).first()

    return render_template('menu_details.html', menu=menu)


@app.route('/menulist')
def menus():
    menus = Menu.query.all()
    return render_template("menulist.html",
                           title="Menu List",
                           menus=menus)


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

@app.route('/event/<id>', methods=['GET', 'POST'])
@login_required
def event_details(id):
    event = Event.query.filter_by(id=id).first_or_404()
    return render_template('event.html', event=event)

@app.route('/event_del/<id>')
@login_required
def event_del(id):
    event = Event.query.filter_by(id=id).first_or_404()
    db.session.delete(event)
    db.session.commit()
    return redirect('/events')


### Guest list functs ###

@app.route('/event/guests/<int:id>')
@login_required
def guest_list2(id):
    if request.method == 'POST':
        print('hi')
    #usrs = Event.query.join(id=id).join(Guest).query.all()
    usrs =  User.query.all()
    #usrs = Event.guests.query.filter_by(id=id).first_or_404()
    event = Event.query.filter_by(id=id).first_or_404()

    return render_template('guests.html', guests=usrs, event=event)





#Need to fidure out how I query assoctiaon table
@app.route('/event/guests/<string:id>/register', methods=['GET', 'POST'])
def add_guest_to_event(id):
    form = RegisterForm()
    event = Event.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        error =try_register(form.email.data, form.username.data, form.password.data, form.confirm.data)
        if not error:
            usrs =  User.query.all()
            #return redirect(url_for('guests',guests=usrs, event=event))
            return render_template('guests.html', guests=usrs, event=event)
    return render_template('register.html', form = form)


@app.route('/event/<int:id>/guests')
@login_required
def guest_list(id):
    if request.method == 'POST':
        print('hi')
    usrs = Guest.query.all()
    return render_template('guests.html', guests=usrs)


@app.route('/guests/<id>')
@login_required
def remove_guest(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    usrs = User.query.all()
    return render_template('guests.html', guests=usrs)



@app.route('/total-raised')
@login_required
def totalraised():
    return render_template('total-raised.html')

@app.route('/updater')
def updater():
    try:
        t = Total.query.get(1)
        if t is None:
            t2 = 0.0
        else:
            t2 = t.total
        return jsonify(current=t2)
    except Exception, e:
        return(str(e))

#Following func used to generate ticket code, later will be checked against existing entry in DB and assigned to a guest in table
def generateTicketCode():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

@app.route('/ticket')
@login_required
def ticket_view():
    ticket = generateTicketCode()
    return render_template('ticket.html', code = ticket)
