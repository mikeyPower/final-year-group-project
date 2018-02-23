from app import app, db
from .forms import MenuForm
from .models import Menu
from app.views import *
from flask import g,render_template, flash, redirect, session, Flask, url_for, request

@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    form = MenuForm()
    if form.validate_on_submit():#
        #print("you're in")
        add_menu(form.title.data,form.body.data)

        #flash('Menu Created', 'success')
        print("added")
        return redirect('/menulist')
    return render_template('menu.html', form = form)

def add_menu(title_data,body_data):
    title = title_data
    body = body_data

    menu = Menu(
      title = title,
      body = body
    )
    db.session.add(menu)
    db.session.commit()
    return



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
