from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm, menu_views
from app.menu_views import *
from flask import g,render_template, flash, redirect, session, Flask, url_for, request
from .forms import LoginForm, RegisterForm, MenuForm,ChangePassForm, GroupEmailForm, EventForm, EmailAddresses, SearchAdminForm, MoneyRaisedForm
from .models import User, Menu, Total, Event, Guest, MoneyRaised
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
@requires_roles('admin')
def create_admin():
    users = User.query.filter_by(admin=False).all()
    form = SearchAdminForm()
    msg="that user doesn't exist"
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            msg=None
        flash(msg)
        return render_template('create_admin.html',form=form, users=users,myUser=user)
    return render_template('create_admin.html',form=form ,users = users,myUser=None)


@app.route("/make_admin/<usr_id>",methods=['GET','POST'])
def make_admin(usr_id):
    user = User.query.filter_by(username = usr_id).first()
    msg = "failed to create admin"
    if user:
        user.admin= True
        db.session.commit()
        msg = "admin created"
        flash(msg)
    return redirect("/create_admin")

##for testing purposes
def admin_test_function(name):
    user = User.query.filter_by(username = name).first()
    if user:
        user.admin= True
        db.session.commit()
    return
#######end admin##########




@app.route('/index')
@login_required
def index():
    return redirect('/events')


#################### Mailing and Invitations Stuff ##################
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



# Send Invitations
@app.route('/send_emails/<int:ev_id>', methods=['GET', 'POST'])
@login_required
def send_email(ev_id):
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
    guest_list = db.session.query(Guest.user_id).filter_by(event_id = ev_id)
    myRecipient = User.query.all()
    answer = db.session.query(User).filter(~User.id.in_(guest_list))
    index = 0
    for item in answer:
        with open(os.path.join(APP_STATIC, 'invitation.html')) as f:html = f.read()
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(render_template("invitation.html", myRecipient=answer[index], id = ev_id), 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("event.management.tcd@gmail.com", "tcdtcd12")
        server.sendmail("event.management.tcd@gmail.com", answer[index].email, msg.as_string())
        check = answer[index].last_name
        if index < answer.count():
            index = index + 1
        else:
            break
    return render_template('send_emails.html', myRecipient=answer)


#Send group email
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
        text = "Hello"
        myRecipient = User.query.all()
        for i in range(len(myRecipient)):
            with open(os.path.join(APP_STATIC, 'invitation.html')) as f:html = f.read()
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("event.management.tcd@gmail.com", "tcdtcd12")
            server.sendmail("event.management.tcd@gmail.com", myRecipient[i].email, msg.as_string())
    return render_template('group_email.html', form = form)


#Send group email to guest and invite lists
@app.route('/group_email_to_guest_invite_lists/<int:ev_id>', methods=['GET', 'POST'])
@login_required
def group_email_to_guest_and_invite_lists(ev_id):
    form = GroupEmailForm()
    if form.validate_on_submit():#
        print("your in")
        title = form.title.data
        body = form.body.data
        myRecipient = User.query.all()
        guest_list = db.session.query(Guest.user_id).filter_by(event_id = ev_id)
        myRecipient = User.query.all()
        answer = db.session.query(User.email).filter(~User.id.notin_(guest_list)).first()

        print(answer[0])

        me = "Event Company"
        you = "Wessam Gholam"
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        APP_STATIC = os.path.join(APP_ROOT, 'templates')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = me
        msg['To'] = you
        text = "Hello"
        myRecipient = User.query.all()
        for i in range(len(answer)):
            with open(os.path.join(APP_STATIC, 'invitation.html')) as f:html = f.read()
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("event.management.tcd@gmail.com", "tcdtcd12")
            server.sendmail("event.management.tcd@gmail.com", answer[i], msg.as_string())
            #return redirect('/send_emails/{{ev_id}}')
            #return redirect(url_for('send_emails', id=ev_id))
            return redirect(url_for('send_email', ev_id=ev_id))
    return render_template('group_email_to_guest_invite_lists.html', form = form)


#Send group email to guest and invite lists
@app.route('/invite/<int:ev_id>', methods=['GET', 'POST'])
@login_required
def customised_invitations(ev_id):
    form = EmailAddresses()
    if form.validate_on_submit():#
        print("your in")
        adressess = form.addresses.data
        myRecipient = User.query.all()
        guest_list = db.session.query(Guest.user_id).filter_by(event_id = ev_id)
        myRecipient = User.query.all()
        answer = db.session.query(User.email).filter(~User.id.notin_(guest_list)).first()
        addresses2 = []
        addresses2 = adressess.split(";")
        print(addresses2)
        print(addresses2[0])

        me = "Event Company"
        you = "Wessam Gholam"
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        APP_STATIC = os.path.join(APP_ROOT, 'templates')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Invitation"
        msg['From'] = me
        msg['To'] = you
        text = "Hello"
        myRecipient = User.query.all()
        for i in range(len(addresses2)):
            with open(os.path.join(APP_STATIC, 'invitation.html')) as f:html = f.read()
            part1 = MIMEText(text, 'plain')
            #part2 = MIMEText(body, 'html')
            part2 = MIMEText(render_template("invitation.html", myRecipient=myRecipient, id = ev_id), 'html')
            msg.attach(part1)
            msg.attach(part2)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("event.management.tcd@gmail.com", "tcdtcd12")
            server.sendmail("event.management.tcd@gmail.com", addresses2[i], msg.as_string())
            #return redirect('/send_emails/{{ev_id}}')
            #return redirect(url_for('send_emails', id=ev_id))
            return redirect(url_for('send_email', ev_id=ev_id))
    return render_template('invite.html', form = form)


#################### End of Mailing and Invitations Stuff #########################




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
    session['admin'] = False
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
        error =try_register(form.email.data, form.username.data, form.password.data, form.confirm.data,form.first_name.data,form.last_name.data)
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
        start_time = form.start_time.data
        date = form.date.data
        description = form.description.data

        event = Event(
            title=title,
            location=location,
            start_time = start_time,
            date = date,
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
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.description = form.description.data
        db.session.add(event)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('event_details', ev_id=event.id))
    else:
        form.title.data = event.title
        form.location.data = event.location
        form.date.data = event.date
        form.start_time.data = event.start_time
        form.description.data = event.description
    return render_template('add_event.html', form=form)

@app.route('/event/tickets/<int:id>', methods=['GET', 'POST'])
@login_required
def event_ticket(id):
    event = Event.query.filter_by(id=id).first_or_404()
    return render_template('tickets.html', event=event, event_title = event.title, location= event.location, id=id)

### Guest list functs ###



@app.route('/event/<int:ev_id>/guest/<int:guest_id>/rem')
@login_required
def rem_guest(ev_id, guest_id):
    event = Event.query.filter_by(id=ev_id).first_or_404()
    guest = Guest.query.filter_by(user_id=guest_id).first_or_404()
    event.guests.remove(guest)
    db.session.commit()
    return redirect(url_for('guest_list', id=ev_id))

def rem_guest_tester(ev_id, guest_id):
    event = Event.query.filter_by(id=ev_id).first_or_404()
    guest = Guest.query.filter_by(user_id=guest_id).first_or_404()
    event.guests.remove(guest)
    db.session.commit()
    return True

@app.route('/event/event_tickets/<int:eventid>')
@login_required
def event_tickets(eventid):
    if request.method == 'POST':
        print('hi')
    alltickets =  Event.query.filter_by(id=eventid).first_or_404().guests
    return render_template('event_tickets.html', tickets=alltickets)

@app.route('/event/invite_list/<int:ev_id>')
@login_required
def event_invite_list(ev_id):
    if request.method == 'POST':
        print('hi')
    #alltickets =  Event.query.filter_by(id=eventid).first_or_404().guests
    guest_list = db.session.query(Guest.user_id).filter_by(event_id = ev_id)
    myRecipient = User.query.all()
    answer = db.session.query(User).filter(~User.id.in_(guest_list)).all()
    return render_template('event_invite_list.html', list = answer)




#Need to fidure out how I query assoctiaon table
@app.route('/event/<string:id>/guests/register', methods=['GET', 'POST'])
def add_guest_to_event(id):
    form = RegisterForm()
    event = Event.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        error =try_register(form.email.data, form.username.data, form.password.data, form.confirm.data,form.first_name.data,form.last_name.data)
        if not error:
            user =  User.query.filter_by(username=form.username.data).first_or_404()
            assign_ticket(id,user.id)
            return redirect(url_for('guest_list', id=id))
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

@app.route('/guests')
@login_required
def all_guests():
    guests = User.query.filter_by(admin=False)
    return render_template('all_guests.html', guests=guests)



def get_total_raised(eventid):
    d_list = Event.query.get(eventid).moneyraised
    t = sum(x.amount for x in d_list)
    if t is None:
        t2 = 0.0
    else:
        t2 = t
    return jsonify(current=t2)

@app.route('/total-raised/<int:eventid>')
@login_required
def totalraised(eventid):
    return render_template('total-raised.html', event=Event.query.get(eventid))

@app.route('/update-total-raised/<int:eventid>')
def updater(eventid):
    return get_total_raised(eventid)

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

@app.route('/event/record-money-raised/<int:eventid>', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def record_money_raised_view(eventid):
    form = MoneyRaisedForm()
    if form.validate_on_submit():
        m = MoneyRaised(source=form.source.data, amount=form.money_raised.data, event_id=eventid)
        db.session.add(m)
        db.session.commit()
        flash('Money Recorded! - Source: ' + form.source.data + ',  Amount: ' + str(form.money_raised.data))
        return redirect('/event/record-money-raised/' + str(eventid))
    return render_template('input_money_raised.html', form=form,event = Event.query.get(eventid))

@app.route('/event/view-money-raised/<int:eventid>')
@login_required
@requires_roles('admin')
def view_money_raised_view(eventid):
    d_list = Event.query.get(eventid).moneyraised
    totalraised = sum(x.amount for x in d_list)
    return render_template('admin_view_donations.html', total = totalraised, event = Event.query.get(eventid),donations=d_list)
