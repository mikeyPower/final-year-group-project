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

Feature Number 1 and 2, Administrator:
Steps:
      1. Login as an admin with,Username=Admin and password = password
      2. navigate to the create admin page in the navbar
      3. here you will see a list of users, you can search for a name in the search bar
      4. once you have searched for a user their name will appear under the search bar.
      5. if you then click the name this will make them an admin
      6. this new admin will now have the same ability to create other admin's from the list of users

Feature Number 11 Administrator:
Steps:
      1.Navigate and Click on 'Event' in the navigation bar
      2.You should be now on the events page listing the all the events
      3.Click on 'View' under 'Event Page'
      4.You should now be able to see the individual details of that event
      5.Click on 'View Guest List'
      6.You should now be able to see all the Guest info inlcluding contact details


Feature Number 13 Administrator:
Steps:
      1.Navigate and Click on 'Event' in the navigation bar
      2.You should be now on the events page listing the all the events
      3.Click on 'View' under 'Event Page'
      4.You should now be able to see the individual details of that event
      5.Click on 'View Guest List'
      6.You should now be able to see all the Guest info inlcluding contact details
      7.Now Click on 'add guest' you will be brought to a registration form to fill out
      8.Fill in the guest details and hit 'register' you will now be brought back to the Guest list with the registered guest included


Feature Number 29 Administrator:
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

Feature Number 4:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Click "Add Event"
      3. Input a tilte of your event
      4. Input a the location of the event
      5. Input a description of your event
      6. When satisified with what you have entered hit "Submit"
      5.You will know be brought back to the event list page with your event being added, you may click on "View"
        to see that the contents are the same as you have entered

Feature Number 8,9 and 14:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Click "View"
      3. Click "Guest List"
      4. Click on "Send customised invitations"
      5. Input email addresses separated by a semicolon ";"
      6. Click submit
      5. You will know be brought to a page says "email sent". Where invitations are sent to email addresses you've entered

Feature Number 20:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Click "View"
      3. Click "Guest List"
      4. Click on "Send emails to regestered users"
      5. Input the title of email
      6. Enter the body of email
      7. You will know be brought to a page says "email sent". Emails are sent to all regestered users

Feature Number 21:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Click "View"
      3. Click "Guest List"
      4. Click on "Send email to attendees"
      5. Input the title of email
      6. Enter the body of email
      7. You will know be brought to a page says "email sent". Emails are sent to attendees



Feature Cluster 5 (features 27 and 28):
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "View"
    3. Click "Guest List"
    4. Click on "Add Guest"
    5. Fill out Guest registration details
    6. Submit
    7. You will know be brought to the Guestlist page for that event with the updated list
    8. To remove a guest from the list click remove on the row of the specific guest

Feature Number 5 Update Event
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "View"
    3. Click Edit Event
    4. Make edits
    5. Submit update
    6. You will return to the event page where you can view the changes you have just made
