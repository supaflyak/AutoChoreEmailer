AutoChoreEmailer
Date: 1/16/2018
Author: Russell Wong

Ver 1.0.0
Initial realease

Required edits:
Put in the sending email address and password in lines 19 and 20

Required Files: "ChoreList.txt", "EmailAddresses.txt"
ChoreList.txt: This file holds the title of chore, once per how runs the chore needs to be done, and a description of the chore.
			!DO NO CHANGE THE FIRST LINE!
EmailAddresses.txt: This is a list of email addresses of recipients

Generated files: "ChoreHistory.txt"
ChoreHistory.txt: This file is a list of all of the chores, which email it was sent to last, and how soon it will be done next

Behaviors:
1. Chores to be done once a week will be assigned assigned every week
	1a. There should only be n-1 weekly chores in the chorelist otherwise no other chores will be done
2. Chores and email recipients can be added and removed without needing to reset the choreHistory

TODO:
1. Add a user-friendly way of including sending email address+password
2. Remove dependency on having a garbage first line in ChoreList.txt
3. Allow program to run in the background and trigger at a specified day and time (possibly another project altogether)
4. Separate sections into individual functions