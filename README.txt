Setup:
       1: install pip using 'apt install python-pip'
Run The Following Commands:
       2: pip install virtualenv
       3: virtualenv flask
       4: source flask/bin/activate (this starts the enviornment)
       5. ./install.sh
       6: ./run.py to run the app


Running pytest:
	   1. py.test -v


Feature Number 29:
Steps:
       1.Navigate and click on "Menu List" in the navigation bar
       3.Click "Add Menu"
       2.Input a title of your proposed Menu
       3.Input the contents/body of the Menu
       4.When satisified with what you have entered hit "Submit"
       5.You will know be brought back to the menulist page with your menu being added, you may click on this menu
         to see that the contents are the same as you have entered

Feature Cluster 12: (features 51,52,53)
Steps:
       This feature can be found by clicking "Total Raised" on the navbar at the top of the screen.
       Here you will see the total amount raised displayed.
       1.With the app running, open a new terminal and navigate to the root folder
       2.In console, run the following commands:
            1. python
            Now the python interpreter is launched, enter the following:
            2. from app import app, views
            3. from app.views import *
            4. add_to_total_raised( <ADD CUSTOM AMOUNT> )
       3.When you enter your amount, you will see that the amount raised updates to the new amount on the website.
