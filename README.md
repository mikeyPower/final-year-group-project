## Open the terminal and navigate to the app’s root folder.
Setup:
'''
       1: install pip using 'sudo apt install python-pip'
       Run The Following Commands:
       2: sudo pip install virtualenv
       3: virtualenv flask
       4: source flask/bin/activate (this starts the environment)
       5: ./install.sh
       6: ./run.py to run the app 
       7: in your web browser localhost:5000
'''

## Running pytest:
1. flask/bin/pytest
Note: This only works with a clean db. To test locally do make fresh first (THIS WILL CLEAR THE DATABASE). For development purposes, the tests are executed automatically by Travis-CI


Feature Number 1 | Administrator | I want to be able to login (change password/details/create account)
Feature Number 62 | Attendee | Create an account/register
Feature Number 63 | Attendee | Login to account
Steps:
      User:
      1. To Register account click the ‘here’ button under sign-in as detailed and you can enter your details
      2. Once registered you can then login by typing in your username and password and clicking sign in.
      3. to change your password navigate to ‘My Account’ in the navbar and click ‘Change Password’
      4. fill in your old and new password and submit, your changes will be saved
      5. You can logout and log back in with your new password 
      6. To change your account details, navigate to ‘My Account’ in the navbar and click ‘Edit Account Details’.
      7. Change your details as desired, click the special dietary requirements checkbox if necessary. Click  ‘Update Account’ to save your changes

      Administrator:
     If already logged in, click ‘Logout’ in the top right
      1. Login as an admin with,Username=Admin and password = password
      2. We recommend to change the password for this account immediately. The steps are the same as mentioned above.



Feature Number 2|Administrator| I want to be able to give admin access to other people
      1. navigate to the admin page in the navbar
      2. here you will see a list of users, you can search for a name in the search bar.
      3. once you have searched for a user a button with “Make” name “an Admin” will appear under the search bar.
      4. if you then click this button, and click confirm on the next screen. This will make them an admin
      5. this new admin will now have the same ability to create another admin from the list of users

Feature Number 4 | Administrator | I would like to be able to create an event e.g. a dinner:
Steps:
      1. Navigate and click on "Event" in the navigation bar
      2. Click "Add Event"
      3. Input a title for your event
      4. Input the location of the event
      5. Input the day, month and year of the event, followed by the time below.
      5. Input a description for your event
      6. When satisfied with what you have entered hit "Submit"
      5.You will now be brought back to the event list page with your event being added.

Feature Number 5 | Administrator | I want to be able to update event information and submit event updates
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "View" on the desired event page
    3. Click ‘Edit Event’
    4. Update the info as desired
    5. Click Submit to submit the update, or cancel, to cancel any changes.
    6. You will return to the event page where you can view the changes you have just made

Feature Number 29|Administrator|I want to create menus:
Steps:
       1.Navigate and click on "Menu List" in the navigation bar
       3.Click "Create Menu"
       2.Input a title of your proposed Menu
       3.Input the contents/body of the Menu
       4.When satisfied with what you have entered hit "Submit"
       5.You will know be brought back to the menu list page with your menu being added, you may click on this menu to see that the contents are the same as you have entered
       6.In order to upload a pdf file of your menu click ‘Browse..’ button
       7.a pop up of your file manager will appear, search your file manager and double click on your desired pdf file to add, the name of the file will appear beside the ‘Browse..’ button
       8.Click ‘Upload Menu’ button to add the menu to the menulist    
       9.The menu should now be added to the menu list
       10. To view the menus you have created, click on the title of the menu to view it 

Feature Number 51 | Administrator | I want to see how much is raised so far:
Steps:
      1. First click on ‘Event’ on the navbar.
      2. Then click view, on the event you wish to see the money raised for.
      3. Then click “View total money raised”
  To Test the feature:
      4. In a new tab, navigate to the same event page.
      5. Click ‘Record a Donation’
      6. Input the amount raised.
      7. If the money was raised from a user donation, select the user from the dropdown
      8. If the money is from another source, click the checkbox and enter the source.
      9. Click Submit to record the donation.
      10. Go back to the “View total money raised” page and the total will update.

Feature Number 54 | Administrator | I want to track current amount raised:
Steps:
      1. First click on ‘Event’ on the navbar.
      2. Then click view, on the event you wish to see the money raised for.
      3. Then in the Admin Tools section click “View donations”
      4. This will show a more detailed page of raised money for admins to see info about each donation



Feature Number 7 | Administrator | Track which guests are big spenders and/or regular donors
Steps:
      1. Click on the “Users” heading on the navbar
      2. Click the “View Top Donors” button
      3. You will be redirected to a list of all users showing how much each has donated

Feature Number 8 | Administrator | I want to send invitations to a mailing list, so that people know to come and that they are invited
Steps:
1.  To create an mailing list,  navigate and click on “Mailing lists” in the navigation bar
2. Click on “Add Mailing list”
3. Enter a title of the mailing list and select email addresses you want to add to the mailing list then click on “Submit”, or click on “Add emails manually” to add emails that are not on the list and enter a title for the mailing list and type in emails addresses separated by a semicolon then click on “Submit”
4. Navigate and click on “Event” in the navigation bar
5. Click on “Guest List” for the particular event you want
6. Click on “Send invitations to mailing list”
7. Please select a mailing list from the list
8. Click on “Submit”
9. You will be brought back to guest list page for that particular event with a message on top says “Invitation sent”



Feature Number 9 | Administrator | Send out invitations)
Feature Number 14 | Administrator | I want to be able to send automated invitations, with link to register for the event
Steps:
  	1. Navigate and click on "Event" in the navigation bar
  	2. Click "View" for the particular event you want
  	3. Click "Guest List"
  	4. Click “Send invitations to non guests” to send invitations.
5. To customise the invitation that is sent out, click customise invitations button, and enter an email. Otherwise a default template is sent out.

Feature Number 20 | Administrator | I would like to email (legitimately) subscribed users:
Steps:
  	1. Navigate and click on "Mailing lists" in the navigation bar
  	2. To send an email to all users, click ‘“Send emails to all registered users”
3. Enter the title and body of the email, then click submit to send
4. The email will be sent to all registered users.
5. To email a mailing list, click on "Mailing lists" in the navigation bar
6. Click “Send email to users”
7. Select the mailing lists to which you want to send your email.
8. Enter the title and body of the email, then click submit to send

Feature Number 21 | Administrator | I want to be able to contact attendees easily e.g. group emails:
Steps:
  	1. Navigate and click on "Event" in the navigation bar
  	3. Click "View" for the particular event you want
  	4. Click "View Guest List"
      	5. Click on "Send email to guests"
  	6. Input the title of email
  	7. Enter the body of email
  	8. Click Submit
  	9. Your email will be sent to the guest list

Feature Number 13| Administrator|As staff, I need to register a guest for one event (including their details), so I can track what is needed for the event
Feature Number 27 | Administrator | I want to be able to manage the guest list
Feature Number 28 | Administrator | I want to be able to add/remove attendees from the guest list
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "View"
    3. Click "Guest List"
    4. Click on "Add Guest"
    5.1. To add existing users find the user in the table and click add on the user row
    5.2  To view the guestlist click "Event" on the navbar then click the guestlist of the event you wish to view
    6.1. To add an unregistered guest go back to the add guest page, click Register New Guest and fill out Guest registration details then click register
    6.2. You will know be brought to the Guestlist page for that event with the updated list
    7. To remove a guest from the list click remove on the row of the specific guest
    8. To edit a guests dietary needs as an Admin, go to Users on the navbar, click View Details for the user which you want to edit. Click edit account details, then add any changes. Click update, and the changes will be saved.

Feature Number 11| Administrator | I want to see guests contact details:
Steps:
      1.Navigate and Click on 'Event' in the navigation bar
      2.You should be now on the events page listing all the events
      3.Click on 'View' under 'Event Page’
      4.Click on 'View Guest List'
      5.You should now be able to see all the Guest info including contact details

Feature Number 6|Administrator|Keep Track of Possible/Previous Guests:
Steps:
    1. Navigate and click on "Users" in the navigation bar
    2. You are now shown a list of all possible and previous guests that are not admins

Feature Number 10 | Administrator| I want to see the invite list:
Steps:
    1. Navigate and click on "Event" in the navigation bar
    2. Click "Invite List" for the particular event you want
    3. You will be brought to a page which contains the invite list for that particular event

Feature Number 15 | Administrator | Set up a ticketing service, so people can buy tickets without human interaction
Steps:
      1.Ensure an event is already created
      2.As a non-admin user, to get a ticket for yourself, follow the following steps:
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



Feature Number 34 | Administrator | i want to be able to manage table setting
    1. click the Event tab in the nav bar
    2. at the bottom of the page under AdminTools is a button called manage seating arrangement, that will bring you the seating arrangement page
    3. once on this page you can add a table by clicking the add table button. this will create an empty table. This page also shows all the unseated guests.
    4. once a table is created you can edit a table by clicking the edit table button beside the table you wish to edit
    5. once on this table you have a list of users that are unseated and people who are seated at this table, if a user is seated at a different table they will not appear on the table on the left also Users will only appear in the unseated table if they have a ticket for the event
    6. to add a user to the table search for the by username in the search bar. once submitted a button will appear "add 'Username' to table", clicking this will add them to the seated table on the right
    7. once added to the "Seated" table beside the user's name is a "remove" button, this will remove that user from the table and put them back in the "unseated " table 
    8.(feature 35) to make a table owned by a corporate entity click the corporate table button, this will bring you to a page where you can enter a name for the table. Entering the name and submitting will make the table owned by a company. This will mean you can’t add other users to the table
    9.(feature 35) for changing the name of the table,  If you enter a name if the text box and submit it will change the name, which you can see at the top of the page, if a table is corporate entity entering a name in this box and submitting will change the table back so any user can sit at it. 
    10. to navigate back to the previous page click "here" at the bottom of the page
    11. you are now back to the manage table page. if you click "here" at the bottom of that page it will bring you back to the event page you started on 



Feature Number 114 | Administrator | Admins can delete events
Steps:
      1.Click “Event” on navbar
      2. Locate the event you wish to delete from list of events
      3.Click “Delete Event” on the event row
      4.The list of events will be updated to show the event has been deleted

