Setup: 1: you need to install pip if you haven't already(you can skip this if you want but i'd recommend it),
          if you dont replace 'pip' with 'sudo apt-get install'
       2: pip install virtualenv
       2.5: pip install flask-socketio
       3: virtualenv flask
       4: mkdir tmp
       5: ./setup.txt(you may need to change permissions)
       6: next do, source flask/bin/activate (this starts the enviornment)
       7: ./db_create.py
       8: ./db_migrate.py
       9: ./run.py to run the app
