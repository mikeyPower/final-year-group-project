from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm
from flask import render_template, flash, redirect, session, request
from flask_table import Table, Col, LinkCol
from .forms import LoginForm, RegisterForm
from .models import User
from flask_wtf import Form as BaseForm
from functools import wraps
from flask import Flask, url_for
from passlib.hash import sha256_crypt




@app.route('/index')
@login_required
def index():
    return render_template('index.html')

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


@app.route('/guests', methods=['GET', 'POST'])
def guest_list():
    if request.method == 'POST':
        print('hi')
    usrs = User.query.all()
    return render_template('guests.html', guests=usrs)


@app.route('/guests/<id>')
def remove_guest(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    usrs = User.query.all()
    return render_template('guests.html', guests=usrs)
