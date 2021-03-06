from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm, menu_views
from app.menu_views import *
from flask import g,render_template, flash, redirect, session, Flask, url_for, request
from .forms import LoginForm, RegisterForm, MenuForm,ChangePassForm, GroupEmailForm, EventForm, EmailAddresses, SearchAdminForm, PastebinEntry, EditAccountForm, EmailAddresses2, Invitation_temp,SizeForm, TableNameForm, CorpTableNameForm
from .models import User, Menu, Total, Event, Guest, Choice, Mailing_list, Recipient, Non_user_recipient, MoneyRaised, Event_Table, Table_Attendee
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
from wtforms import StringField, PasswordField, FileField, BooleanField, TextAreaField, IntegerField, DateTimeField,SelectField,SelectMultipleField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from flask.ext.wtf import Form
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
from flask.ext.sqlalchemy import SQLAlchemy
from functools import partial
from sqlalchemy import orm
from flask.ext.wtf import FlaskForm
from flask import Flask, abort, request
import json
from werkzeug.datastructures import MultiDict
import time
from datetime import datetime
from urllib import urlencode, quote, unquote
#global id_number_for_form = 0;
ev_num = 0



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


########table management##############

@app.route('/event/<string:event_id>/tableArrangement',methods=['GET', 'POST'])
def tableArrangement(event_id):
    tables = Event_Table.query.filter_by(event_id = event_id)
    guests =db.session.query(Guest).filter_by(event_id = event_id)
    return render_template('table_arrangement.html', guests=guests, tables = tables,event_id=event_id)

@app.route('/event/<string:event_id>/tableArrangement/addtable',methods=['GET', 'POST'])
def addTable(event_id):
    tables = Event_Table.query.filter_by(event_id = event_id)
    i = 1
    for t in tables:
        i = i+1
    table= Event_Table(
            event_id = event_id,
            table_num = i
            )
    db.session.add(table)
    db.session.commit()
    guests =db.session.query(Guest).filter_by(event_id = event_id)
    return redirect(url_for('tableArrangement', event_id=event_id))

@app.route('/event/<string:event_id>/tableArrangement/<string:table_id>/edit/corporate', methods=['GET', 'POST'])
def corporate_table(event_id,table_id):
    corpNameForm =CorpTableNameForm()
    table = Event_Table.query.filter_by(id=table_id).first()
    if corpNameForm.validate_on_submit():
        name = corpNameForm.name.data
        table.table_name = name
        table.corprate_table = True
        db.session.commit()
        return redirect(url_for('editSeating', event_id=event_id, table_id=table_id))
    return render_template('corpSeating.html', corpNameForm= corpNameForm,t=table_id)
 


@app.route('/event/<string:event_id>/tableArrangement/<string:table_id>/edit', methods=['GET', 'POST'])
def editSeating(event_id,table_id):
    users = Guest.query.filter_by(event_id=event_id).filter_by(seated=False).all()
    form = SearchAdminForm()
    sizeForm = SizeForm()
    nameForm = TableNameForm()
    table = Event_Table.query.filter_by(id=table_id).first()
    msg="that user isn't attending the event"

    if nameForm.validate_on_submit():
        name = nameForm.name.data
        table.table_name = name
        table.is_corprate = False
        db.session.commit()
        return render_template('seating.html',sizeForm=sizeForm,form=form,table_id=table_id,myUser=None, users=users, event_id=event_id, t = table, nameForm=nameForm)
    if sizeForm.validate_on_submit():
        size = sizeForm.size.data
        table.free_seats = size - table.free_seats
        return render_template('seating.html', sizeForm=sizeForm,form=form,table_id=table_id,myUser=None, users=users, event_id=event_id, t = table, nameForm=nameForm)
    if form.validate_on_submit():
        usr = User.query.filter_by(username= form.username.data).first()
        myUser = Guest.query.filter_by(user_id=usr.id).first()
        if myUser != None:
            return render_template('seating.html',sizeForm=sizeForm,form=form,table_id=table_id,myUser=usr, users=users, event_id=event_id, t = table,nameForm=nameForm)
        flash(msg)
    return render_template('seating.html', sizeForm=sizeForm,form=form, table_id=table_id,myUser=None,users=users, event_id = event_id, t=table,nameForm=nameForm)

@app.route('/event/<string:event_id>/tableArrangement/<string:table_id>/edit/<string:user_id>/add', methods=['GET', 'POST'])
def addUserToTable(event_id,table_id,user_id):
    table = Event_Table.query.filter_by(id = table_id).first()
    if table.corprate_table:
        flash("cannot add guest, table is booked or full")
        return redirect(url_for('editSeating', event_id=event_id, table_id=table_id))
    gst = Guest.query.filter_by(user_id = user_id).first()
    if gst.seated:
        gst.seated=True
        flash("user is already seated")
        return redirect(url_for('editSeating', event_id=event_id, table_id=table_id))
    atnd = Table_Attendee(table_id = table_id,
                        user_id = user_id
                        )
    db.session.add(atnd)
    table.free_seats-=1
    gst.seated=True
    db.session.commit()
    return redirect(url_for('editSeating', event_id=event_id, table_id=table_id))
@app.route('/event/<string:event_id>/tableArrangement/<string:table_id>/edit/<string:user_id>/remove', methods=['GET', 'POST'])
def removeUserfromtable(user_id,table_id,event_id):
    atnd = Table_Attendee.query.filter_by(user_id=user_id).first()
    guest = Guest.query.filter_by(user_id=user_id).first()
    table = Event_Table.query.filter_by(event_id=event_id).first()
    guest.seated=False
    table.free_seats+=1
    db.session.delete(atnd)
    db.session.commit()
    return redirect(url_for('editSeating', event_id=event_id, table_id=table_id))


###########End Table management##########


###########admin stuff############

def confirmation_required(desc_fn):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.args.get('confirm') != '1':
                desc = desc_fn()
                return redirect(url_for('confirm',
                    desc=desc, action_url=quote(request.url)))
            return f(*args, **kwargs)
        return wrapper
    return inner

@app.route('/confirm')
def confirm():
    desc = request.args['desc']
    action_url = unquote(request.args['action_url'])

    return render_template('_confirm.html', desc=desc, action_url=action_url)

def you_sure():
    return "do you want to make this user an admin?"


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
    msg="that user doesn't exist, or is already an admin"
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            return render_template('create_admin.html',form=form, users=users,myUser=user)
        else:
            flash(msg)
    return render_template('create_admin.html',form=form ,users = users,myUser=None)


@app.route("/make_admin/<usr_id>",methods=['GET','POST'])
@confirmation_required(you_sure)
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
    ev = Event.query.filter_by(id = ev_id).all()
    eventt = ev[0]
    me = "Event Company"
    you = "Wessam Gholam"
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
    APP_STATIC = os.path.join(APP_ROOT, 'templates')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Invitation"
    msg['From'] = me
    msg['To'] = you
    #text = "Hello!!!!!"
    guest_list = db.session.query(Guest.user_id).filter_by(event_id = ev_id)
    myRecipient = User.query.all()
    answer = db.session.query(User).filter(~User.id.in_(guest_list))
    index = 0
    for item in answer:
        with open(os.path.join(APP_STATIC, 'invitation.html')) as f:html = f.read()
        #part1 = MIMEText(text, 'plain')
        #part2 = MIMEText(render_template("invitation.html", myRecipient=answer[index], id = ev_id), 'html')
        if eventt.use_default_invitation is False:
            print('mmm')
            print(eventt.invitation_template)
            part2 = MIMEText(eventt.invitation_template, 'plain')
        else:
            part2 = MIMEText(render_template("invitation.html", myRecipient=myRecipient, id = ev_id, title = eventt.title, location = eventt.location, date = eventt.date), 'html')

        #msg.attach(part1)
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
    flash('Email sent!!')
    return redirect(url_for('guest_list', id =ev_id))
    #return render_template('send_emails.html', myRecipient=answer)


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
            redirect('/events/')
    #flash('Emails sent!!')
        #string = "http://127.0.0.1:5000/select_users_for_group_email_to_mailing_list"
        string = "http://127.0.0.1:5000/mailing_lists"
    #return redirect(url_for('select_users_to_emails_to_mailing_list'))
        return render_template('send_emails.html', st = string)
    #return redirect(url_for('guest_list', id =ev_id))
    return render_template('group_email.html', form = form)


#Send group email to guest and invite lists
@app.route('/group_email_to_guest_invite_lists/<int:ev_id>', methods=['GET', 'POST'])
@login_required
def group_email_to_guest_and_invite_lists(ev_id):
    form = GroupEmailForm()

    str_of_redirect = "http://127.0.0.1:5000/event/ev_id/guests"
    #string = "http://127.0.0.1:5000/select_users_foev_idoup_email_to_mailing_list"
    string = "http://127.0.0.1:5000/mailing_lists"
    if form.validate_on_submit():#
        print("your in")
        title = form.title.data
        body = form.body.data
        myRecipient = User.query.all()
        guest_list = db.session.query(Guest.user_id).filter_by(event_id = ev_id)
        myRecipient = User.query.all()
        answer = db.session.query(User.email).filter(~User.id.notin_(guest_list)).first()

        #print(answer[0])

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
        flash('Email sent!!')
        return redirect(url_for('guest_list', id =ev_id))
            #return render_template('send_emails.html', st = str_of_redirect, ev_id = ev_id)
            #return redirect(url_for('send_email', ev_id=ev_id, st = str_of_redirect))
    return render_template('group_email_to_guest_invite_lists.html', form = form, st = str_of_redirect)


#Send group email to guest and invite lists
@app.route('/invite/<int:ev_id>', methods=['GET', 'POST'])
@login_required
def customised_invitations(ev_id):
    form = EmailAddresses()
    if form.validate_on_submit():#
        print("Maaaagic")
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


@app.route('/send_emails/', methods=['GET', 'POST'])
@login_required
def email_sent_confirmation():
    #time.sleep(5)
    #string = "http://127.0.0.1:5000/select_users_for_group_email_to_mailing_list"
    string = "http://127.0.0.1:5000/mailing_lists"
    #return redirect(url_for('select_users_to_emails_to_mailing_list'))
    return render_template('send_emails.html', st = string)

@app.route('/group_email_to_mailing_list', methods=['GET', 'POST'])
@login_required
def g_emails_to_mailing_list():
    form = GroupEmailForm()
    users =  request.args.getlist('json')
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        me = "Event Company"
        you = "Wessam Gholam"
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        APP_STATIC = os.path.join(APP_ROOT, 'templates')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = me
        msg['To'] = you
        text = "Hello"
        for i in range(len(users)):
            with open(os.path.join(APP_STATIC, 'invitation.html')) as f:html = f.read()
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("event.management.tcd@gmail.com", "tcdtcd12")
            server.sendmail("event.management.tcd@gmail.com", users[i], msg.as_string())
        return redirect(url_for('email_sent_confirmation'))
    #print('ooopa loopa')
    print(users)
    #print(users[0])
    #print(users[1])
    #print(users[2])
    #return redirect(url_for('email_sent_confirmation'))
    return render_template('group_email_to_mailing_list.html', form=form)


@app.route('/mailing_list_error_handling', methods=['GET', 'POST'])
@login_required
def empty_mailing_list():
    return render_template('mailing_list_error.html')


@app.route('/select_users_for_group_email_to_mailing_list', methods=['GET', 'POST'])
@login_required
def select_users_to_emails_to_mailing_list():
    form = Mailing_list_choice()
    list_of_mailing_lists = []
    ids_list = []
    send_invitations_to = []
    if request.method == 'POST':
        #print(form.a.data)
        print('JUST BEFORE ERROR')
        list_of_mailing_lists = form.a.data
        print(list_of_mailing_lists)
        if not list_of_mailing_lists:
            print('ERROR 404 $$$$$$$$$$$$$$$$$$$$$$$4')
            redirect(url_for('email_sent_confirmation'))
            flash('please select mailing list, or add one if you havent done so')
            return render_template('select_users_for_group_emails.html', form=form)
        for i in range(len(list_of_mailing_lists)):
            ids_list.append(list_of_mailing_lists[i].id)
        #session['users'] = list_of_users
        for i in range(len(list_of_mailing_lists)):
            recipient_list = Recipient.query.filter_by(mailing_list_id = list_of_mailing_lists[0].id).all()
            if not recipient_list:
                print('innnnnn')
                flash('Mailing list is empty, please make sure the mailing list has email addresses')
                return render_template('select_users_for_group_emails.html', form=form)
            #print(recipient_list)
            #print(recipient_list[0].user_id)
            #print(recipient_list[1].user_id)
            #print(recipient_list[0].mailing_list_idd)
            #print(recipient_list[1].mailing_list_idd)
            for j in range(len(recipient_list)):
                users_list = User.query.filter_by(id = recipient_list[j].user_id).all()
                #print(users_list)
                for k in range(len(users_list)):
                    #print(users_list[k].email)
                    send_invitations_to.append(users_list[k].email)
        for i in range(len(list_of_mailing_lists)):
            #print('foucking inside 1')
            non_user_recipient_list = Non_user_recipient.query.filter_by(mailing_list_idd = list_of_mailing_lists[0].id).all()
            for j in range(len(non_user_recipient_list)):
                #print('foucking inside 2')
                send_invitations_to.append(non_user_recipient_list[j].email)
        #url_for('.do_foo', messages=messages)
        #url_for('show_list', some_list=comma_separated)
        #event_data = {'data_1': list_of_users}
        print('visca barca!! ####')
        print(send_invitations_to)
        event_data = {'users': ids_list}
        return redirect(url_for('g_emails_to_mailing_list', json=send_invitations_to))
        #######return redirect(url_for('g_emails_to_mailing_list', some_list=list_of_users))
        #return render_template('select_users_for_group_emails.html', form=form)

        #return redirect('/group_email_to_mailing_list',listt = list_of_users)
        #return render_template('group_email_to_mailing_list.html', listt = list_of_users)
    return render_template('select_users_for_group_emails.html', form=form)
    #group_email_to_mailing_list





def invitations_to_a_mailing_list(addresses2,ev_id):

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
        return redirect(url_for('email_sent_confirmation'))
        #return redirect('/events')
    #flash('Invitations are sent!')
    #return redirect('/send_emails/{{ev_id}}')
        #return redirect(url_for('send_emails', id=ev_id))
        #return redirect(url_for('send_email', ev_id=ev_id))
    #return render_template('invite.html', form = form)


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
        error =try_register(form.email.data, form.username.data, form.password.data,
         form.confirm.data,form.first_name.data,form.last_name.data, form.has_dietary_requirements.data,
         form.dietary_requirements.data, form.phone.data)
        if not error:

            #Need to decide on Database
            #flash('you have sucessfully registered')
            return redirect('/login')
    return render_template('register.html', form = form)

#logic of how to register
def try_register(email,name,password,confirm_pass,f_name,l_name,has_reqs,reqs,phone):
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
    if has_reqs == False:
        reqs=None
    user = User(
      email = email,
      username = name,
      hashed_password = sha256_crypt.hash(str(password)), #password , #Hashing added
      first_name = f_name,
      last_name = l_name,
      has_dietary_requirements = has_reqs,
      dietary_requirements = reqs,
      phone = phone
    )
    db.session.add(user)
    db.session.commit()
    return False



@app.before_request
def before_request():
    g.user = current_user

@app.route('/my_account/change_password', methods=['GET','POST'])
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

@app.route('/mailing_lists', methods=['GET','POST'])
@login_required
def mailing_lists():
    mailing_listss = Mailing_list.query.all()
    print('test test')
    try:
        print(mailing_listss[-1].id)
        mailing_list_id = mailing_listss[-1].id + 1
    except:
        mailing_list_id = 1
    return render_template('mailing_lists.html',mailing_listss=mailing_listss, mailing_list_id=mailing_list_id)

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



@app.route('/event/<int:ev_id>/customise_invitation', methods=['GET','POST'])
@login_required
def customise_invitation(ev_id):
    form = Invitation_temp()
    #print(form.invitation.data)
    event = Event.query.filter_by(id = ev_id).all()
    print(event[0].invitation_template)
    if form.validate_on_submit():
    #if request.method == 'POST':
        event[0].use_default_invitation = False
        event[0].invitation_template = form.invitation.data
        db.session.commit()
        return redirect(url_for('guest_list', id=ev_id))
    else: print(form.errors)
    form.invitation.data = event[0].invitation_template


    return render_template('customise_invitation_template.html', form=form)


@app.route('/edit_mailing_list/<int:mailing_list_id>', methods=['GET','POST'])
@login_required
def edit_mailing_lists(mailing_list_id):
    global id_number_for_form
    id_number_for_form = mailing_list_id
    print(id_number_for_form)
    form = Choice_partial_Form()
    list_mail = Mailing_list.query.filter_by(id = mailing_list_id).all()
    ml = list_mail[0]
    mailing_listss = []
    if request.method == 'POST':
        print('ON SUBMIT')
    #form.title.data = event.title
        mailing_listss = Mailing_list.query.all()
        wanted_users = form.a.data
        ml.title = form.title.data
        db.session.add(ml)
        db.session.commit()
        for i in range(len(wanted_users)):
            print(mailing_list_id)
            print(wanted_users[i].email)
            recipient = Recipient(
                user_id = wanted_users[i].id,
                mailing_list_id=mailing_list_id
            )
            db.session.add(recipient)
            db.session.commit()
        if not wanted_users:
            flash('Title has been updated')
        else:
            flash('User added to mailing list')
    else:
        form.title.data = ml.title


    return render_template('edit_mailing_list.html',mailing_listss=mailing_listss, mailing_list_id=mailing_list_id, form=form)





def choice_partial_query(columns='email'):

    mlist = Mailing_list.query.filter_by(id=id_number_for_form).all()
    users = db.session.query(User.id, User.email)
    recipient_list = db.session.query(Recipient).filter_by(mailing_list_id = id_number_for_form).all()
    print('inside partial')
    print(mlist)
    print(recipient_list)
    list_of_users = []
    mlist = Mailing_list.query.filter_by(id=id_number_for_form).all()
    users = db.session.query(User).all()
    recipient_list = db.session.query(Recipient).filter_by(mailing_list_id = id_number_for_form).all()
    print('before deletion')
    print(users)
    for i in range(len(recipient_list)):
        llist = db.session.query(User).filter_by(id = recipient_list[i].user_id).all()
        print(llist)
        print(users)
        if llist[0] in users:
            users.remove(llist[0])
        else:
            print(' ')
        print('after deletion')
        print(users)
        print('-----------------------')
        index = index = 1


    u = User.query
    return users

def getUserFactory(columns='email'):
    return partial(choice_partial_query, columns=columns)

class Choice_partial_Form(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    a = QuerySelectMultipleField(query_factory=getUserFactory('email'), get_label='email')





##########################################33
def choose_mailing_list(columns='email'):
    print('inside partial')

    u = Mailing_list.query
    return u

def getUserFactory(columns='email'):
    return partial(choose_mailing_list, columns=columns)

class Mailing_list_choice(Form):
    a = QuerySelectMultipleField(query_factory=getUserFactory('email'), get_label='title')
##########################################33

#### Event page functions ########


@app.route('/events')
@login_required
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)

#db = SQLAlchemy(app)




def choice_query(columns='email'):
    users = db.session.query(User.id, User.email)
    u = User.query
    return u

def getUserFactory(columns='email'):
    return partial(choice_query, columns=columns)

class ChoiceForm(Form):
    title = StringField('Title:', validators=[DataRequired()])
    a = QuerySelectMultipleField(query_factory=getUserFactory('email'), get_label='email')



@app.route('/create_mailing_list/add_emails/<int:mailing_list_id>',methods=['GET', 'POST'])
@login_required
def add_emails_manually_to_mailing_list(mailing_list_id):
    form = EmailAddresses2()
    oo = Non_user_recipient.query.all()
    print(oo)
    #db.session.query(Non_user_recipient).delete()
    #db.session.commit()
    #oo = Non_user_recipient.query.all()
    #print(oo)
    if form.validate_on_submit():
    #if request.method == 'POST':
        print(form.title.data)
        tit = form.title.data
        adressess1 = form.addresses.data
        print("Maaaagic")
        print(form.addresses.data)
        addresses2 = []
        addresses2 = adressess1.split(";")
        print(addresses2)
        print('-------------------------------')
        print(' ')
        print('before loop')
        oo = Non_user_recipient.query.all()
        print(oo)
        mailing_list = Mailing_list(
            title = tit
        )
        print('Mailing title is: ')
        print(tit)
        db.session.add(mailing_list)
        db.session.commit()
        #rr =
        for i in range(len(addresses2)):
            addr = addresses2[i]
            print(addresses2[i])
            non_user_recipient = Non_user_recipient(
                mailing_list_idd=mailing_list_id,
                email = addresses2[i]
            )
            db.session.add(non_user_recipient)
            db.session.commit()


        oo2 = Non_user_recipient.query.all()
        print('after loop')
        print(oo2)
        return redirect(url_for('mailing_lists'))
    else:
        print(form.errors)





    #events = Event.query.all()
    return render_template('invite2.html', form=form)

@app.route('/create_mailing_list/add_emails_v2/<int:mailing_list_id>',methods=['GET', 'POST'])
@login_required
def add_emails_manually_to_mailing_list_v2(mailing_list_id):
    form = EmailAddresses()
    if form.validate_on_submit():#
        adressess1 = form.addresses.data
        print("Maaaagic")
        print(form.addresses.data)
        addresses2 = []
        addresses2 = adressess1.split(";")
        print(addresses2)
        print('-------------------------------')
        print(' ')
        print('before loop')
        oo = Non_user_recipient.query.all()
        #print(oo)

        for i in range(len(addresses2)):
            addr = addresses2[i]
            #print(addresses2[i])
            non_user_recipient = Non_user_recipient(
                mailing_list_idd=mailing_list_id,
                email = addresses2[i]
            )
            db.session.add(non_user_recipient)
            db.session.commit()


        oo2 = Non_user_recipient.query.all()
        print('after loop')
        print(oo2)
        return redirect(url_for('mailing_lists'))





    #events = Event.query.all()
    return render_template('invite.html', form=form)


@app.route('/mailing_list_del/<int:mailing_list_id>')
@login_required
def mailing_list_del(mailing_list_id):
    print('before deletion')
    all_lists = Mailing_list.query.all()
    all_rec = Recipient.query.all()
    print('Look carefully')
    print(all_lists)
    print(all_rec)
    mlist = Mailing_list.query.filter_by(id=mailing_list_id).first_or_404()
    recipient_list = db.session.query(Recipient).filter_by(mailing_list_id = mailing_list_id).all()
    non_user_recipient_list = db.session.query(Non_user_recipient).filter_by(mailing_list_idd = mailing_list_id).all()

    print('content of query of rec list')
    print(recipient_list)
    index = 0;
    for i in range(len(recipient_list)):
        print('inside fooor loop')
        print(recipient_list[i])
        db.session.delete(recipient_list[i])
        db.session.commit()

    for i in range(len(non_user_recipient_list)):
        db.session.delete(non_user_recipient_list[i])
        db.session.commit()

    db.session.delete(mlist)
    db.session.commit()
    print('deletion is done')
    print(all_lists)
    print(all_rec)
    return redirect('/mailing_lists')

@app.route('/mailing_list/<int:mailing_listt_id>/delete_email/<int:recipient_id>',methods=['GET', 'POST'])
@login_required
def remove_email_from_mailing_list(mailing_listt_id,recipient_id):
    recipient_list = db.session.query(Recipient).filter_by(user_id = recipient_id).all()
    print(recipient_id)
    print('well im here')
    print(recipient_list)
    try:
        print(' ')
        #print(recipient_list[0].user_id)
        #print(recipient_list[1].user_id)
    except:
        print('err')

    print('getting type')
    print(type(recipient_list[0]))
    print(recipient_list[0])
    print(hasattr(recipient_list[0], 'iddd'))
    if(recipient_list[0] == Recipient):
        print('its a Recipient')



    db.session.delete(recipient_list[0])
    db.session.commit()
    return redirect('/mailing_lists')


@app.route('/mailing_list/<int:mailing_listt_id>/delete_email_non_users/<int:recipient_id>',methods=['GET', 'POST'])
@login_required
def remove_email_from_mailing_list_for_non_users(mailing_listt_id,recipient_id):
    recipient_list = db.session.query(Non_user_recipient).filter_by(id = recipient_id).all()
    print(recipient_id)
    print('well im here')
    print(recipient_list)
    try:
        print(' ')
        #print(recipient_list[0].user_id)
        #print(recipient_list[1].user_id)
    except:
        print('err')


    print('getting type')



    db.session.delete(recipient_list[0])
    db.session.commit()
    return redirect('/mailing_lists')




@app.route('/mailing_list/<int:mailing_list_id>',methods=['GET', 'POST'])
@login_required
def mailing_list(mailing_list_id):
    if request.method == 'POST':
        print('hi')

    list_of_users=[]
    print('ma list')
    print(list_of_users)
    recipient_list = db.session.query(Recipient).filter_by(mailing_list_id = mailing_list_id).all()
    print('WEEEEEEESAM')
    print(recipient_list)
    index = 0;

    for i in range(len(recipient_list)):
        llist = db.session.query(User).filter_by(id = recipient_list[i].user_id).all()
        list_of_users.append(llist[0])
        index = index = 1
    addresses2 = Non_user_recipient.query.filter_by(mailing_list_idd = mailing_list_id).all()
    print(addresses2)

    email_address_for_non_users = []
    for i in range(len(addresses2)):
        addr = addresses2[i]
        email_address_for_non_users.append(addresses2[i].email)
    try:
        print('Watch ooot')
    except:
        print('nope')


    return render_template('mailing_list.html', mailinglists=list_of_users, id=mailing_list_id, email_address_for_non_users = addresses2)


@app.route('/create_mailing_list/<int:mailing_list_id>',methods=['GET', 'POST'])
@login_required
def create_mailing_list(mailing_list_id):
    form = ChoiceForm()
    user=None
    if form.validate_on_submit():
        print('Validated')
    else: print(form.errors)
    if form.validate_on_submit():
        if form.title.data is None or form.a.data is None:
            flash('please type in title and pick mailing list ')
    #if request.method == 'POST':
        try:
            title_assigned = form.title.data
            user = form.a.data
            print('Look Here')
            print(title_assigned)
            mailing_list = Mailing_list(
                title = title_assigned
            )
            db.session.add(mailing_list)
            db.session.commit()
            lists = Mailing_list.query.all()
            particular_mailing_list = db.session.query(Mailing_list).filter_by(id = mailing_list_id)
            print(lists)
            for i in range(len(user)):
                print(mailing_list_id)
                print(user[i].email)
                recipient = Recipient(
                    user_id = user[i].id,
                    mailing_list_id=mailing_list_id
                )
                db.session.add(recipient)
            #db.session.add(mailing_list)
            db.session.commit()
            recipient_list = db.session.query(Recipient).filter_by(mailing_list_id = mailing_list_id).all()
            ll = Recipient.query.all()
            print(ll)

            print(recipient_list)
            print(recipient_list[0].mailing_list_id)
            return redirect(url_for('mailing_lists', form = form,id=mailing_list_id))


        except:
            print('error2')
    else:
        print('NOT SUBMITTED')
        #if form.title.data is None or form.a.data is None:
        if request.method == 'POST':
            flash('please type in title and pick mailing list ')

    return render_template('create_mailing_list.html',form = form,id=mailing_list_id)


@app.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    form = EventForm()

    if form.validate_on_submit():
        title = form.title.data
        location = form.location.data
        start_time = form.time.data
        tmp = form.day.data + "-" + form.month.data + "-" + form.year.data
        description = form.description.data

        event = Event(
            title=title,
            location=location,
            start_time = start_time,
            date = tmp,
            description=description,
            use_default_invitation = True,
            invitation_template = " "
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
        tmp = form.day.data + "-"+ form.month.data + "-" + form.year.data
        event.date = tmp
        event.start_time = form.time.data
        event.description = form.description.data
        db.session.add(event)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('event_details', ev_id=event.id))
    else:
        form.title.data = event.title
        form.location.data = event.location
        tmp = event.date.split("-")
        form.month.data = tmp[1]
        form.day.data = tmp[0]
        form.year.data = tmp[2]
        form.time.data = event.start_time
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

    # Users not already signed up to event
    guestlist = event.guests
    users_list = User.query.all()
    users = []
    for u in users_list:
        vis = 0
        for g in guestlist:
            if (u.id == g.user_id):
                vis = 1
        if (vis == 0):
            users.append(u)

    if form.validate_on_submit():
        error =try_register(form.email.data, form.username.data, form.password.data,
         form.confirm.data,form.first_name.data,form.last_name.data, form.has_dietary_requirements.data,
         form.dietary_requirements.data, form.phone.data)
        if not error:
            user =  User.query.filter_by(username=form.username.data).first_or_404()
            assign_ticket(id,user.id)
            return redirect(url_for('guest_list', id=id))
    return render_template('registration.html', form = form, event = event, usrs = users)


# Add existing user to guestlist of an event
@app.route('/event/<string:id>/guests/register/user/<int:user_id>')
@login_required
def add_user_to_guestlist(id, user_id):
    assign_ticket(id, user_id)
    return redirect(url_for('add_guest_to_event', id=id))



@app.route('/event/<int:id>/guests')
@login_required
def guest_list(id):
    if request.method == 'POST':
        print('hi')
    guestlist = Event.query.filter_by(id=id).first_or_404().guests
    return render_template('guests.html', guests = guestlist, event = Event.query.filter_by(id=id).first_or_404())

###########################################################
@app.route('/event/<int:id>/invite_mailing_list',methods=['GET', 'POST'])
@login_required
def invite_mailing_list_to_event(id):
    form = Mailing_list_choice()
    send_invitations_to = []
    guestlist = []
    if request.method == 'POST':
    #if form.validate_on_submit():
        #print('hiiiiiiiiii')
        print(form.a.data)
        ml = form.a.data
        st = "http://127.0.0.1:5000/event/"
        print(st)
        st += str(id)
        st += "/guests"
        print(ev_num)
        global ev_num
        ev_num = id
        print(ev_num)

        print(st)
        if not ml:
            print('ERROR 404 @@@@@@@@')
            flash('Please select a mailing list, or create one if you havent done so')
            return render_template('invite_mailing_list.html', guests = guestlist, form = form)


        done = 0
        print(ml)
        for i in range(len(ml)):
            recipient_list = Recipient.query.filter_by(mailing_list_id = ml[0].id).all()
            print(recipient_list)
            if recipient_list is None:
                if request.method == 'POST':
                    flash('Mailing list is empty, please make sure the mailing list has email addresses')
                    return render_template('invite_mailing_list.html', guests = guestlist, form = form)
            #print(recipient_list[0].user_id)
            #print(recipient_list[1].user_id)
            #print(recipient_list[0].mailing_list_idd)
            #print(recipient_list[1].mailing_list_idd)
            for j in range(len(recipient_list)):
                users_list = User.query.filter_by(id = recipient_list[j].user_id).all()
                print(users_list)
                for k in range(len(users_list)):
                    print(users_list[k].email)
                    send_invitations_to.append(users_list[k].email)
        for i in range(len(ml)):
            #print('foucking inside 1')
            non_user_recipient_list = Non_user_recipient.query.filter_by(mailing_list_idd = ml[0].id).all()
            for j in range(len(non_user_recipient_list)):
                #print('foucking inside 2')
                send_invitations_to.append(non_user_recipient_list[j].email)
                #done =1
        #redirect('/event/record-money-raised/' + str(eventid))
        #return redirect('/send_emails/' + str(id))
    #invitations_to_a_mailing_list(send_invitations_to,id)
        addresses2 = send_invitations_to
        print('content of list')
        print(addresses2)
        if not addresses2:
            print('innnnnn')
            flash('Mailing list is empty, please make sure the mailing list has email addresses')
            return render_template('invite_mailing_list.html', guests = guestlist, form = form)
        ev_id = id
        ev = Event.query.filter_by(id = ev_id).all()
        eventt = ev[0]
        if eventt.use_default_invitation is False:
            print('FAAAAAAAAAAAAAAALSE')
        else:
            print('TRUEEEEEEEEEEE')
        me = "Event Company"
        you = "Wessam Gholam"
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        APP_STATIC = os.path.join(APP_ROOT, 'templates')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Invitation to " + eventt.title + " event"
        msg['From'] = me
        msg['To'] = you
        #text = " "
        part2 = " "
        myRecipient = User.query.all()
        for i in range(len(addresses2)):
            with open(os.path.join(APP_STATIC, 'invitation.html')) as f:html = f.read()
            #part1 = MIMEText(text, 'plain')
            #ev = Event.query.filter_by(id = ev_id).all()
            print(ev)
            print(ev[0].title)
            print(eventt)
            #part2 = MIMEText(body, 'html')
            if eventt.use_default_invitation is False:
                print('mmm')
                print(eventt.invitation_template)
                part2 = MIMEText(eventt.invitation_template, 'plain')
            else:
                part2 = MIMEText(render_template("invitation.html", myRecipient=myRecipient, id = ev_id, title = eventt.title, location = eventt.location, date = eventt.date), 'html')
                #msg.attach(part1)
                msg.attach(part2)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login("event.management.tcd@gmail.com", "tcdtcd12")
                server.sendmail("event.management.tcd@gmail.com", addresses2[i], msg.as_string())
                #return redirect(url_for('email_sent_confirmation'))
                flash('Invitations sent!!')
                return redirect(url_for('guest_list', id =ev_id))

            print(send_invitations_to)
            #return redirect(url_for('email_sent_confirmation'))

    guestlist = Event.query.filter_by(id=id).first_or_404().guests
    return render_template('invite_mailing_list.html', guests = guestlist, form = form)


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


def get_total_raised_test(eventid):
    d_list = Event.query.get(eventid).moneyraised
    t = sum(x.amount for x in d_list)
    if t is None:
        t2 = 0.0
    else:
        t2 = t
    return t2

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
    form.user_source.choices = getChoices()
    if form.validate_on_submit():
        m = MoneyRaised(other_source=form.source.data, user_source = form.user_source.data,
        amount=form.money_raised.data, from_other_source=form.checkbox.data, event_id=eventid,
        date_time = datetime.now())
        if(form.user_source.data == 0 and form.checkbox.data== False):
            flash("Please Select a User or Select Other Source!")
            return redirect('/event/record-money-raised/' + str(eventid))
        db.session.add(m)
        db.session.commit()
        flash('Money Recorded! - Source: ' + form.source.data + ',  Amount: ' + str(form.money_raised.data))
        return redirect('/event/record-money-raised/' + str(eventid))
    else:
        print form.errors
    return render_template('input_money_raised.html', form=form,event = Event.query.get(eventid))

@app.route('/event/view-money-raised/<int:eventid>')
@login_required
@requires_roles('admin')
def view_money_raised_view(eventid):
    d_list = Event.query.get(eventid).moneyraised
    totalraised = sum(x.amount for x in d_list)
    sources = []
    for d in d_list:
        if(d.from_other_source==True):
            sources.append(Donation_Source(d.other_source,d.amount, d.date_time))
        else:
            sources.append(Donation_Source(d.user_backref.email,d.amount, d.date_time))
    return render_template('admin_view_donations.html', total = totalraised, event = Event.query.get(eventid),donations=sources)

class Donation_Source(object):
    def __init__(self, source, amount, date):
        self.source = source
        self.amount = amount
        self.date = date


def getChoices():
    try:
        ls = User.query.all()
        cs = [(0,None)]
        for u in ls:
            cs.append((u.id,u.email))
        return cs
    except:
        print 'ok'

class MoneyRaisedForm(Form):
    money_raised = DecimalField('Money Raised:', validators=[DataRequired()])
    checkbox = BooleanField('If from another source, click this box', default=False)
    user_source = SelectField('Users:', choices=getChoices(), coerce=int)
    source = StringField('Source:')

@app.route('/top_donors')
@login_required
@requires_roles('admin')
def top_donors():
    return render_template('top_donors.html', donors=top_donors_hidden() )

def top_donors_hidden():
    u_list = User.query.all()
    donors = []
    for u in u_list:
        donors.append(Donor(u,sum([d.amount for d in u.donations])))
    newlist = sorted(donors, key=lambda x: x.total, reverse=True)
    return newlist

class Donor(object):
    def __init__(self, user, total):
        self.user = user
        self.total = total

@app.route('/my_account')
@login_required
def my_account():
    return render_template('my_account.html', user=User.query.filter_by(id=current_user.id).first_or_404())


@app.route('/my_account/edit', methods=['GET', 'POST'])
@login_required
def edit_my_account():
    form=EditAccountForm()
    if form.validate_on_submit():
        user=g.user
        user.email=form.email.data
        user.phone=form.phone.data
        user.first_name=form.first_name.data
        print form.first_name.data
        user.last_name=form.last_name.data
        user.has_dietary_requirements=form.has_dietary_requirements.data
        user.dietary_requirements=form.dietary_requirements.data
        if form.has_dietary_requirements.data == False:
            user.dietary_requirements=None
        db.session.commit()
        return redirect('/my_account')
    else:
        print form.errors

    user=g.user
    form.email.data=user.email
    form.phone.data=user.phone
    form.first_name.data=user.first_name
    form.last_name.data=user.last_name
    form.has_dietary_requirements.data=user.has_dietary_requirements
    form.dietary_requirements.data=user.dietary_requirements

    return render_template('edit_my_account.html',form=form, user_id=g.user.id)

@app.route('/get_dietary_bool/<int:id>')
def get_dietary_bool(id):
    return jsonify(bool=User.query.filter_by(id=id).first_or_404().has_dietary_requirements)

@app.route('/view_account/<int:id>')
@login_required
@requires_roles('admin')
def view_account(id):
    return render_template('view_account.html', user=User.query.filter_by(id=id).first_or_404())

@app.route('/view_account/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def edit_account(id):
    form=EditAccountForm()
    if form.validate_on_submit():
        user=User.query.filter_by(id=id).first_or_404()
        user.email=form.email.data
        user.phone=form.phone.data
        user.first_name=form.first_name.data
        print form.first_name.data
        user.last_name=form.last_name.data
        user.has_dietary_requirements=form.has_dietary_requirements.data
        user.dietary_requirements=form.dietary_requirements.data
        if form.has_dietary_requirements.data == False:
            user.dietary_requirements=None
        db.session.commit()
        return redirect('/view_account/'+str(id))
    else:
        print form.errors

    user=User.query.filter_by(id=id).first_or_404()
    form.email.data=user.email
    form.phone.data=user.phone
    form.first_name.data=user.first_name
    form.last_name.data=user.last_name
    form.has_dietary_requirements.data=user.has_dietary_requirements
    form.dietary_requirements.data=user.dietary_requirements
    return render_template('edit_account.html',form=form, user_id=id)
