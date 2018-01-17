# Title: Chore Emailer
# Author: Russell Wong
# Date: 11/25/2017 [Merry Christmas]
# Description: Emailer sends out weekly chore instructions to users' emails from a given list
# Assumptions: ChoreList.txt has fewer weekly chores than email addresses

import smtplib
import sys
import ctypes

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


x = Mbox("EMAILS GONNA GET SENT", "This will send a bunch of emails. \n Are you sure you want to proceed?", 4)
if x == 7:
    exit()

EMAIL = ""
PASSWORD = ""
EMAILFILE = "EmailAddresses.txt"
CHOREFILE = "ChoreList.txt"
HISTORYFILE = "ChoreHistory.txt"

# set up emails
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(EMAIL, PASSWORD)

# import files
with open(EMAILFILE) as OpenFile:
    readThings = OpenFile.read()
    emails = readThings.split("\n")  # list of emails

with open(CHOREFILE) as OpenFile:
    readThings = OpenFile.read()
    choreStrings = readThings.split("\n")  # liminated strings of chores, descriptions and frequencies
# remove the first line
choreStrings.pop(0)

with open(HISTORYFILE) as f:
    read = f.read()
    history = read.split("\n")

# Compare chore list with history
for n in range(0, choreStrings.__len__()):
    checkingChore = choreStrings[n].split(";")[0]
    token = True
    for m in range(0, (history.__len__() - 1).__floordiv__(3) + 1):
        if history[m * 3] == checkingChore:
            token = False
            break
    if token:
        if not history[0]:
            history[0] = checkingChore
        else:
            history.append(checkingChore)
        history.append("")
        history.append(choreStrings[n].split(";")[1])

thisWeeksChores = []
# Create a list of chores that need to get done
# First we add the weekly chores
for n in range(0, choreStrings.__len__()):
    chores = choreStrings[n].split(";")
    if chores[1] is "1":
        thisWeeksChores.insert(thisWeeksChores.__len__() + 1, choreStrings[n])
        history[history.index(chores[0]) + 2] = "1"

# Pick chores so chore list is the same as number of emails
tempHist = history + ["."]
tempHist.pop(tempHist.__len__() - 1)  # BECAUSE FUCK THIS ASSHOLE LANGUAGE
# remove the weekly chores from tempHist
for n in thisWeeksChores:
    try:
        x = tempHist.index(n.split(";")[0])
        for m in range(0, 3):
            tempHist.pop(x)
    except ValueError:
        pass

# Find more chores to assign if there aren't enough
mostNeg = 0
while (thisWeeksChores.__len__() < emails.__len__()) & (mostNeg < 1):
    # Search for most negative number in the history
    mostNeg = 1
    for n in range(0, (tempHist.__len__() - 1).__floordiv__(3) + 1):
        if int(tempHist[(n * 3) + 2]) < int(mostNeg):
            mostNeg = int(tempHist[(n * 3) + 2])
    # if a chore is found
    if mostNeg < 1:
        # find the full chore string of the chosen chore
        tempChore = 0
        for n in choreStrings:
            x = str(tempHist[tempHist.index(str(mostNeg)) - 2])
            p = str(n.split(";")[0])
            if x == p:
                tempChore = n
        # put it into thisWeeksChores
        thisWeeksChores.insert(thisWeeksChores.__len__() + 1, tempChore)
        # remove the entry from tempHist
        ind = tempHist.index(str(mostNeg))
        for m in range(0, 3):
            tempHist.pop(ind - m)

# FINALLY all the emails are picked. Just reset the new values of the chores done and decrement
# the ones that didn't get done. Oh and send the emails
# decrement all values in the history file
for n in range(0, (history.__len__() - 1).__floordiv__(3) + 1):
    history[(n * 3) + 2] = int(history[(n * 3) + 2])
    history[(n * 3) + 2] -= 1

# reset the chores that get done
for n in range(0, thisWeeksChores.__len__()):
    history[history.index(thisWeeksChores[n].split(";")[0]) + 2] = thisWeeksChores[n].split(";")[1]

# Sending email time. Also picking who does what chore
names = [[0 for x in range(emails.__len__())] for y in range(thisWeeksChores.__len__())]
# Make a list of all possible candidates for chore
for n in range(0, thisWeeksChores.__len__()):
    ind = history.index(thisWeeksChores[n].split(";")[0]) + 1  # index of the emails of those who did the chore last
    for m in range(0, emails.__len__()):
        names[n][m] = (history[ind].split(";").count(emails[m]) * -1)

# Votes contains the overall votes as a form of secondary ranking
votes = []
for n in range(0, names[0].__len__()):
    votes.append(0)

for n in range(0, names[0].__len__()):
    for m in range(0, names.__len__()):
        votes[n] += names[m][n]

# Now names array have the votes of who should not do the chore. More votes means less likely to do it.
# If there's a tie, a winner is picked arbitrarily
pickNames = []
for n in range(0, names.__len__()):
    maxVal = max(names[n])
    # If there is only one name with the max value, add it, set the vote value to the lowest possible
    if 1 == names[n].count(maxVal):
        ind = names[n].index(max(names[n]))
        votes[ind] -= 1
        pickNames.append(emails[ind])
        for m in range(0, names.__len__()):
            names[m][ind] = sys.maxsize * -1
    # If one of the top maxVal names has a higher vote rank, pick the higher vote rank name
    else:
        pick = []
        for m in range(0, names[n].__len__()):
            if maxVal == names[n][m]:
                pick.append(votes[m])
            else:
                pick.append(sys.maxsize * -1)
        pickNames.append(emails[pick.index(max(pick))])
        votes[pick.index(max(pick))] -= 1
        for m in range(0, names.__len__()):
            names[m][pick.index(max(pick))] = sys.maxsize * -1

# Remove duplicates
n = 0
while n < (pickNames.__len__() - 1):
    if pickNames[n + 1] == pickNames[n]:
        # If there is someone without a chore, give them the chore
        token = True
        for x in emails:
            if pickNames.count(x) == 0:
                token = False
                pickNames[n] = x
        if token:
            if max(names[n + 1]) >= max(names[n]):
                # set pickNames[n] to the second highest value of names[n]
                m1 = m2 = float('-inf')
                for x in names[n]:
                    if x > m2:
                        if x >= m1:
                            m1, m2 = x, m1
                        else:
                            m2 = x
                pickNames[n] = emails[m2]
            else:
                # set pickNames[n+1] to the second highest value of names[n+1]
                m1 = m2 = float('-inf')
                for x in names[n + 1]:
                    if x > m2:
                        if x >= m1:
                            m1, m2 = x, m1
                        else:
                            m2 = x
                pickNames[n + 1] = emails[m2]
    else:
        n += 1

# Add names to history file
for n in range(0, pickNames.__len__()):
    x = history[history.index(thisWeeksChores[n].split(";")[0]) + 1]
    if not history[history.index(thisWeeksChores[n].split(";")[0]) + 1]:
        history[history.index(thisWeeksChores[n].split(";")[0]) + 1] += (pickNames[n])
    else:
        history[history.index(thisWeeksChores[n].split(";")[0]) + 1] += (";" + pickNames[n])


# Write to history file
with open(HISTORYFILE, 'w') as f:
    for x in range(0, history.__len__()):
        if (x + 1) == history.__len__():
            f.writelines(str(history[x]))
        elif str(history[x]).__len__():
            f.writelines(str(history[x]) + "\n")
        else:
            f.writelines("\n")

# send the emails
msg = ("BEEP BOOP \n"
       " \n "
       "Hello, \n"
       "I am the email server giving you your weekly chore!"
       " Please complete the following chore by this Sunday night! \n"
       " \n "
       "Your chore this week is \n")
for x in range(0, thisWeeksChores.__len__()):
    thisChoreName = thisWeeksChores[x].split(";")[0]
    test = msg + thisChoreName + "\n" + thisWeeksChores[x].split(";")[2]
    server.sendmail(EMAIL, pickNames[x], test)

exit()
