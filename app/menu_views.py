from app import app, db
from .forms import MenuForm
from .models import Menu, Event
from app.views import *
from flask import g,render_template, flash, redirect, session, Flask, url_for, request, Markup#, IntegrityError
import time
import datetime
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.path.abspath("../GroupDesignProject/app/static/")
#UPLOAD_FOLDER = '/home/michael/Desktop/gfyp/GroupDesignProject/app/static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







@app.route('/menu/', methods=['GET', 'POST'])
@login_required
def menu():
    form = MenuForm()
    if form.validate_on_submit():#
        #print("you're in")
        upload =False
        if add_menu(form.title.data,form.body.data,upload) == True:
            return redirect('/menulist')
        else:
            flash('Menu has not been added')
    return render_template('menu/menu.html', form = form)

def add_menu(title_data,body_data,upload):
    title = title_data
    body = body_data
    menu = Menu(
      title = title,
      body = body,
      created_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
      upload=upload
    )
    try:
        db.session.add(menu)
        db.session.commit()
        return True
    except:
        return False

    return True

@app.route('/event/<string:id1>/menu/')
@login_required
def show_menu_to_event(id1):
    menus = Menu.query.all()
    return render_template("menu/menulist.html",
                           title="Menu List",
                           menus=menus,
                           event=id1)

@app.route('/event/<string:id1>/menu/<string:id2>')
@login_required
def add_menu_to_event(id1,id2):
    menu = Menu.query.filter_by(id=id2).first_or_404()
    event = Event.query.filter_by(id=id1).first_or_404()
    menu.events.append(event)
    db.session.commit()
    menu = Menu.query.filter_by(id=id2).first_or_404().events
    #return render_template('event.html', event=event)
    #return redirect('/event/1')
    return redirect(url_for('event_details', ev_id=id1))

@app.route('/menu/<string:id>/')
@login_required
def menu_details(id):

    menu = Menu.query.filter_by(id=id).first()

    return render_template('menu/menu_details.html', menu=menu)


@app.route('/menulist', methods=['GET', 'POST'])
def menus():
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            body = None
            title = file.filename
            add_menu(title,body,True)
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return render_template("menu/test_menu.html",filename='file:///'+UPLOAD_FOLDER+file.filename)

    menus = Menu.query.all()
    return render_template("menu/menulist.html",
                           title="Menu List",
                           menus=menus)




# Edit Menu
@app.route('/edit_menu/', methods=['GET', 'POST'])
#@login_required
def edit_menu(id):
    menu = Menu.query.filter_by(id=id).first()
    # Get form
    form = MenuForm()

    # Populate article form fields
    form.title.data = menu.title
    form.body.data = menu.body

    if form.validate_on_submit():#
        form = MenuForm()
        #title1 = form.title.data
        #body1 = form.body.data
        #admin = Menu.query.filter_by(id=id).update(dict(title=title1))
        #db.session.commit()
        #admin = Menu.query.filter_by(id=id).update(dict(body=body1))
        #db.session.commit()
        menu.title =  form.title.data
        menu.body = form.body.data
        db.session.commit()
        flash('Menu Updated', 'success')

        return redirect('/menulist')

    return render_template('menu.html', form=form)
