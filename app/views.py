from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm
from flask import render_template, flash, redirect, session, Flask, url_for, request
from .forms import LoginForm, RegisterForm, MailingForm, MenuForm,ChangePassForm
from .models import User, Recipient, Menu, Total
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


# Send emails
@app.route('/send_emails', methods=['GET', 'POST'])
@login_required
def send_email():
    me = "Event Company"
    you = "Wessam Gholam"
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
    APP_STATIC = os.path.join(APP_ROOT, 'templates')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Invitation"
    msg['From'] = me
    msg['To'] = you
    text = "Hello!!!!!"
    with open(os.path.join(APP_STATIC, 'invitation.html')) as f:
        html = f.read()
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("event.management.tcd@gmail.com", "tcdtcd12")
    myRecipient = Recipient.query.all()
    for i in range(len(myRecipient)):
        server.sendmail("event.management.tcd@gmail.com", myRecipient[i].email, msg.as_string())
        check = myRecipient[i].last_name
        print("Look here:**:", check)
    return render_template('send_emails.html', myRecipient=myRecipient)



@app.route('/event')
@login_required
def event():
    return render_template('event.html')

@app.route('/',  methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        error = try_login(form.username.data, form.password.data)
        if not error:
            return redirect('/index')
    return render_template('login.html', form=form)


# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
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
            flash('you have sucessfully registered')
            return redirect('/login')
    return render_template('register.html', form = form)

#logic of how to register
def try_register(email,name,password,confirm_pass):
    #if (email is None) or (name is None) or (password is None) or (confirm_pass is None)
    if password != confirm_pass:
        return True
    user = User.query.filter_by(username=name).first()
    if user is not None:
        return True
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return True
    user = User(
      username = name,
      email = email,
      hashed_password = sha256_crypt.hash(str(password)) #password , #Hashing added
    )
    db.session.add(user)
    db.session.commit()
    return False

@app.route('/setting', methods=['GET','POST'])
@login_required
def settings():
    form = ChangePassForm()
    error = None
    if form.validate_on_submit():
        old = form.oldPassword
        new_pass = form.newPassword
        confirm = form.confirmPassword
        error = changePass(old, new_pass, confirm)
    return render_template('settings.html', form = form )

def changePass(old, new, confirm):
    usr = g.user
    error = "Old password is incorrect"
    if sha256_crypt.verify(str(old), usr.hashed_password):
        if new!=confirm:
            error = "passwords do not match"
            return error
        error=None
        password = sha256_crypt.hash(str(password))
        usr.hashed_password = password
    return error

@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    form = MenuForm()
    if form.validate_on_submit():#
        print("your in")
        title = form.title.data
        body = form.body.data

        menu = Menu(
          title = title,
          body = body
        )
        db.session.add(menu)
        db.session.commit()

        flash('Menu Created', 'success')
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

@app.route('/total-raised')
@login_required
def totalraised():
    total = get_total_raised().total
    print total
    return render_template('total-raised.html', total=total)

def get_total_raised():
    t = Total.query.get(1)
    if t is None:
        return 0
    else:
        return t

#@app.route('/updater')
#def updater():
#    print "okay"
#    try:
#        t = Total.query.get(1)
#        if t is None:
#            t = 0
#        return jsonify(current=t.total)
#    except Exception, e:
#        return(str(e))
