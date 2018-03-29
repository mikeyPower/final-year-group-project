Setup:
       1: install pip using 'sudo apt install python-pip'
Run The Following Commands:
       2: pip install virtualenv
       3: virtualenv flask
       4: source flask/bin/activate (this starts the environment)
       5: ./install.sh
       6: ./run.py to run the app 
       7: in your web browser localhost:5000

Running pytest:
	   1. py.test -v


Feature Number 1 | Administrator | I want to be able to login (change password/details/create account)
Steps:
      User:
      1. To Register account click the button under the sign-in and you can enter your details
      2. Once registered you can then login
      3. to change your password navigate to settings in the navbar
      4. once you fill in your old and new passwords and submit your changes will be saved
      5. You can logout and log back in with your new password 

      Administrator:
      1. Login as an admin with,Username=Admin and password = password
      2. to change your password navigate to settings in the navbar
      3. once you fill in your old and new passwords and submit your changes will be saved
      4. You can logout and log back in with your new password 

Feature Number 2|Administrator| I want to be able to give admin access to other people
      1. navigate to the admin page in the navbar
      2. here you will see a list of users, you can search for a name in the search bar.
      3. once you have searched for a user their name will appear under the search bar.
      4. if you then click the name this will make them an admin
      5. this new admin will now have the same ability to create another admin from the list of users

Feature Number 4 | Administrator | I would like to be able to create an event e.g. a dinner:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Click "Add Event"
      3. Input a title of your event
      4. Input a the location of the event
      5. Select the day, month and year of the event
      6. Input the time of the event e.g "15:00 - 20:00"
      7. Input a description of your event
      8. When satisfied with what you have entered hit "Submit"
      9.You will know be brought back to the event list page with your event being added.

Feature Number 5 | Administrator | I want to be able to update event information and submit event updates
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "View"
    3. Click Edit Event
    4. Make edits
    5. Submit update
    6. You will return to the event page where you can view the changes you have just made

Feature Number 13| Administrator|As staff, I need to register a guest for one event (including their details), so I can track what is needed for the event
Steps:
      1.Navigate and Click on 'Event' in the navigation bar
      2.You should be now on the events page listing the all the events
      3.Click on 'View' under 'Event Page'
      4.You should now be able to see the individual details of that event
      5.Click on 'View Guest List'
      6.You should now be able to see all the Guest info including contact details
      7.Now Click on 'add guest' you will be brought to a registration form to fill out
      8.Fill in the guest details and hit 'register' you will now be brought back to the Guest list with the registered guest included


Feature Number 11| Administrator | I want to see guests contact details:
Steps:
      1.Navigate and Click on 'Event' in the navigation bar
      2.You should be now on the events page listing all the events
      3.Click on 'View' under 'Event Page'
      4.You should now be able to see the individual details of that event
      5.Click on 'View Guest List'
      6.You should now be able to see all the Guest info including contact details


Feature Number 29|Administrator|I want to create menus:
Steps:
       1.Navigate and click on "Menu List" in the navigation bar
       3.Click "Add Menu"
       2.Input a title of your proposed Menu
       3.Input the contents/body of the Menu
       4.When satisfied with what you have entered hit "Submit"
       5.You will know be brought back to the menu list page with your menu being added, you may click on this menu
         to see that the contents are the same as you have entered

Feature Number 51 | Administrator | I want to see how much is raised so far:
Steps:
       This feature can be found by clicking "Total Raised" on the navbar at the top of the screen.
       Here you will see the total amount raised displayed.
       1.With the app running, open a new terminal and navigate to the root folder
       2.In console, run the following commands:
            1.source flask/bin/activate
            2.  python
            Now the python interpreter is launched, enter the following:
            3. from app import app, views
            4. from app.views import *
            5. add_to_total_raised( <ADD CUSTOM AMOUNT> )
       3.When you enter your amount, you will see that the amount raised updates to the new amount on the website.


Feature Number 8 | Administrator | I want to sent invitations to a mailing list, so that people know to come and that they are invited
Feature Number 9 | Administrator | Send out inivitation(s)
Feature Number 14 | Administrator | I want to be able to send automated invitations, with link to register for the event
Steps:
  	1. Navigate and click on "Event" in the navigation bar
  	2. Click "View" for the particular event you want
  	3. Click "Guest List"
  	4. Click on "Send customised invitations"
  	5. Input email addresses separated by a semicolon ";", include an email you can access
    	to allow you to verify the receipt of the email.
  	6. Click submit
  	7. You will know be brought to a page says "email sent". Where invitations are sent to email addresses you've entered
  	8. Please check your email's inbox

Feature Number 20 | Administrator | I would like to email (legitimately) subscribed users:
Steps:
  	1. Navigate and click on "Event" in the navigation bar
  	2. Click "View" for the particular event you want
  	3. Click "Guest List"
  	4. Click on "Send emails to registered users"
  	5. Enter the title of email
  	6. Enter the body of email
  	7. You will now be brought to a page says "email sent". Emails are sent to all registered users
  	8. Please check your email's inbox

Feature Number 21 | Administrator | I want to be able to contact attendees easily e.g. group emails:
Steps:
  	1. Navigate and click on "Event" in the navigation bar
  	3. Click "View" for the particular event you want
  	4. Click "Guest List"
      	5. Click on "Send email to guests"
  	6. Input the title of email
  	7. Enter the body of email
  	8. You will now be brought to a page says "email sent". Emails are sent to attendees
  	9.. Please check your email's inbox


Feature Number 27 | Administrator | I want to be able to manage the guest list
Feature Number 28 | Administrator | I want to be able to add/remove attendees from the guest list
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "View"
    3. Click "Guest List"
    4. Click on "Add Guest"
    5.1. To add existing users find the user in the table and click add on the user row
    5.2  To view the guestlist click "Event" on the navbar then click the guestlist of the event you wish to view
    6.1. To add an unregistered guest go back to the add guest page and fill out Guest registration details then click submit
    6.2. You will know be brought to the Guestlist page for that event with the updated list
    7. To remove a guest from the list click remove on the row of the specific guest

Feature Number 6|Administrator|Keep Track of Possible/Previous Guests:
Steps:
    1. Navigate and click on "Guests" in the navigation bar
    2. You are now shown a list of all possible and previous guestsA

Feature Number 10 | Administrator| I want to see the invite list:
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "Invite List" for the particular event you want
    3. You will be brought to a page which contains the invite list for that particular event

Feature Number 15 | Administrator | Set up a ticketing service, so people can buy tickets without human interaction
Steps:
      1.Ensure an event is already created
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


Feature Number 12 | Administrator | I need to be able to manage  the responses so I can know who is attending
Feature Number 22 | Administrator | I want to be able to see the rsvp list
Feature Number 24 | Administrator | I want to be able to see a report of who is attending an event
Feature Number 25 | Administrator | I want confirmation that people are registered to attend (RSVP’d) in order to have the correct number of staff for the event

      1.In order to view who is attending an event, follow the following steps:
            1.Click Event in the navbar
            2.Click Guest List for the event you wish to see the RSVP list of
            3.You will be shown a list of RSVP'd guests.
      2.To manage this list, it is possible to add a guest (as shown before by clicking Add Guest)
      3.It is possible to delete a guest by clicking Remove Guest

