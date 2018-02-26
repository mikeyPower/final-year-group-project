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

Feature Number 11 Administrator I want to see guests contact details:
Steps:
      1.Navigate and Click on 'Event' in the navigation bar
      2.You should be now on the events page listing all the events
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

Feature Number 29 Administrator I want to create menus:
Steps:
       1.Navigate and click on "Menu List" in the navigation bar
       3.Click "Add Menu"
       2.Input a title of your proposed Menu
       3.Input the contents/body of the Menu
       4.When satisified with what you have entered hit "Submit"
       5.You will know be brought back to the menulist page with your menu being added, you may click on this menu
         to see that the contents are the same as you have entered

Feature Number 51,52,53,54 Administrator:
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

Feature Number 4 Administrator Create Event :
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Click "Add Event"
      3. Input a tilte of your event
      4. Input a the location of the event
      5. Input a description of your event
      6. When satisified with what you have entered hit "Submit"
      5.You will know be brought back to the event list page with your event being added.

Feature Number 8,9 and 14 Administrator Send Invitations:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Create an event, see feature number 4 above
      3. Click "View"
      4. Click "Guest List"
      5. Click on "Send customised invitations"
      6. Input email addresses separated by a semicolon ";", include an email you can access
        to allow you to verify the receipt of the email.
      7. Click submit
      8. You will know be brought to a page says "email sent". Where invitations are sent to email addresses you've entered
      9. Please check your email's inbox

Feature Number 20 Send group email to registered users:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Click "View" for the particular event you want
      3. Click "Guest List"
      4. Click on "Send emails to regestered users"
      5. Enter the title of email
      6. Enter the body of email
      7. You will now be brought to a page says "email sent". Emails are sent to all registered users
      8. Please check your email's inbox

Feature Number 21 Send group emails to guests:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Create an event, see feature number 4 above
      3. Click "View" for the particular event you want
      4. Click "Guest List"
      5. Click "Add guest", you will be brought to a registration form to fill out
      6.Fill in the guest details and hit 'register' you will now be brought back to the Guest list with the registered guest included
      7. Click on "Send email to guests"
      8. Input the title of email
      9. Enter the body of email
      10. You will now be brought to a page says "email sent". Emails are sent to attendees
      11. Please check your email's inbox


Feature Cluster 5 (features 27 and 28) Administrator:
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "View"
    3. Click "Guest List"
    4. Click on "Add Guest"
    5. Fill out Guest registration details
    6. Submit
    7. You will know be brought to the Guestlist page for that event with the updated list
    8. To remove a guest from the list click remove on the row of the specific guest

Feature Number 5 Administrator Update Event
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "View"
    3. Click Edit Event
    4. Make edits
    5. Submit update
    6. You will return to the event page where you can view the changes you have just made

Feature Number 6 Keep Track of Possible/Previous Guests:
Steps:
    1. Navigate and click on "Guests" in the navigation bar
    2. You are now shown a list of all possible and previous guests

Feature Number 10 Administrator View invite list:
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "Add event"
    3. Input a tilte of your event
    4. Input a the location of the event
    5. Input a description of your event
    6. When satisified with what you have entered hit "Submit"
    7.You will know be brought back to the event list page with your event being added.
    8. Click "Invite List" for the particular event you want
    9. You will be brough to a page which contains the invite list for that particular event

Feature Number 15, 16, 18 Administrator:
Steps:
      1.Create an event
      2.As an admin, you can register a guest for an event by doing the following:
            1.Click the guest list for an event
            2.Click add guest
            3.Type in the new guests registration details (note they cannot be an existing user)
            4.Click Register and you will return to the guest list where you can see the ticket code
      3.As a non-admin user, to get a ticket for yourself, follow the following steps:
            1.Click Event in the navbar
            2.Click view event page
            3.Click get a ticket
            4.You will be presented with your ticket Reference code

Feature Number 12, 22, 24, 25:
      1.In order to view who is attending an event, follow the following steps:
            1.Click Event in the navbar
            2.Click Guest List for the event you wish to see the RSVP list of
            3.You will be shown a list of RSVP'd guests.
      2.To manage this list, it is possible to add a guest (as shown before by clicking Add Guest)
      3.It is possible to delete a guest by clicking Remove Guest
