from app import app, db
from flask import render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from .models import User
from flask_wtf import Form as BaseForm

@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/',  methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        error = try_login(form.username.data, form.password.data)
        if not error:
            return redirect('/index')
    return render_template('login.html', form=form)

def try_login(name,password):
    user = User.query.filter_by(username=name).first()
    if user is not None:
        if user.hashed_password == password:
            return False
    return True

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        error =try_register(form.email.data, form.username.data, form.password.data, form.confirm.data)
        if not error:
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
      hashed_password = password #will add the hashing at some point
    )
    db.session.add(user)
    db.session.commit()
    return False








