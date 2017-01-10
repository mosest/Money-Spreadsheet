# +-----------------------------------------------------+
# | === MONEY-SPREADSHEET UPDATER: AS OF 01/09/2017 === |
# | =================== Tara Moses ==================== |
# |                                                     |
# | Updates the spreadsheet on Google Drive called "Mo' |
# | Money, Mo' Problems," which tracks money owed b/t   |
# | the four of us who live at Fair Park.               |
# |                                                     |
# | Here I will explain how the spreadsheet works!      |
# |                                                     |
# | There are six pages: Totals, Occasions, and a debt  |
# | page for each person.                               |
# |                                                     |
# | The Totals page shows the total money owed between  |
# | any two people. For a certain box, the row name     |
# | owes the column name the amount. If the box is red, |
# | then it's reversed. :3                              |
# |                                                     |
# | The Occasions page has 7 columns: Occasion, Date,   |
# | the name of who paid, and four columns for whatever |
# | anybody else owes that person for that occasion.    |
# | E.g., if we went out for ice cream and Jacob picked |
# | up the check just out of ease, and say maybe Lucas  |
# | and I got $5 milkshakes and William didn't get      |
# | anything, the record would look like:               |
# |                                                     |
# | Occasion    Date   WhoPaid Tara Lucas William Jacob |
# | --------------------------------------------------- |
# | Ice Cream / Jan 9 / Jacob /  5 /  5  /       /    / |
# |                                                     |
# | Regardless of how much Jacob spent on his ice cream |
# | his $$$ isn't put into the spreadsheet because he   |
# | doesn't owe himself anything...                     |
# |                                                     |
# | Each debt page has 5 columns: three for the names   |
# | of all the possible people that person could owe,   |
# | an Occasion column, and a Date column. Building off |
# | the example above, both Lucas's and my debt sheets  |
# | would look like:                                    |
# |                                                     |
# | (LUCAS)                                             |
# | Jacob   Tara    William   Occasion    Date          |
# | --------------------------------------------------- |
# |   5   /       /         / Ice Cream / Jan 9 /       |
# |                                                     |
# | (TARA)                                              |
# | Jacob   Lucas    William   Occasion    Date         |
# | --------------------------------------------------- |
# |   5   /       /         / Ice Cream / Jan 9 /       |
# |                                                     |
# | because we both owe Jacob for that instance. In     |
# | each debt page record, there will only be a number  |
# | in one of the three columns with names. There's no  |
# | reason you'd owe both William and Jacob, say, for   |
# | a certain occasion.                                 |
# +-----------------------------------------------------+ 

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

# +-----------------------------------------------------+
# | ====================== MAIN ======================= |
# |                                                     |
# | Gives the user two options:                         |
# |                                                     |
# | (1) Using the command line, add an occasion to the  |
# |     spreadsheet by typing in your answer for each   |
# |     field. Fields include occasion, the name of who |
# |     paid (any case), and how much everybody owes.   |
# |                                                     |
# | (2) Look through the records (starting from the one |
# |     at the bottom of the spreadsheet, since it was  |
# |     probably entered most recently), and check if   |
# |     the occasion and date are found in anybody's    |
# |     debt page. (The Total page is only correct if   |
# |     all of the occasion records are in their appro- |
# |     priate debt pages.) If the pair is found in     |
# |     one, then it is in everybody's.                 |
# |                                                     |
# |     If the record isn't found in the debt pages,    |
# |     add it in.
# |                                                     |
# |     If we find a record that's already in the debt  |
# |     pages (i.e. finished), then we stop because     |
# |     that means that all records are in the debt     |
# |     pages. (Assuming that once we find a finished   |
# |     record, all the ones before that one are        |
# |     finished as well.)                              |
# |                                                     |
# | Extra options:                                      |
# |                                                     |
# | (3) Go through all the records and make sure the    |
# |     debts have been added to everybody's debt page. |
# |     This is the same as (2), but we don't assume    |
# |     that once we find a finished record, all the    |
# |     records before it are finished too.             |
# +-----------------------------------------------------+

# variables

names = ["Jacob","Lucas","William","Tara"]

choice      = 1
again       = "y"

occasion    = ""
date        = ""
whoPaid     = ""

jacobOwes   = 0
lucasOwes   = 0
williamOwes = 0
taraOwes    = 0

currentRow  = []
whoPaidCol  = 6

# authenticate credentials

json_key = json.load(open('mo-money-mo-problems-ef769f001aed.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)

#get all the sheets!

global wholeBook
wholeBook        = gc.open("Mo' Money, Mo' Problems")

totalsSheet      = wholeBook.worksheet("Totals")
occasionsSheet   = wholeBook.worksheet("Occasions")
jacobSheet       = wholeBook.worksheet("Jacob")
lucasSheet       = wholeBook.worksheet("Lucas")
williamSheet     = wholeBook.worksheet("William")
taraSheet        = wholeBook.worksheet("Tara")

# ask user which task they want the program to do

choice = input("(1) user input, or (2) check rows? ")

if choice == "1":
    
    # user wants to input data on her own!

    while again == "y":

        occasion    = input("Occasion: ")
        date        = input("Date: ")

        # check whether the user input of "who paid"
        # is acceptable

        whoPaid = input("Who paid: ")
        whoPaid = whoPaid[:1].upper() + whoPaid[1:].lower()
            
        while not whoPaid in names:
            whoPaid = input("Who paid: ")
            whoPaid = whoPaid[:1].upper() + whoPaid[1:].lower()

        print("\n")
        
        # now get into the whole "who owes what" stuff, but
        # it depends on who paid, so let's put it inside
        # some if-statements

        if whoPaid != "Jacob":
            jacobOwes   = input("Jacob owes: $")
            
        if whoPaid != "Lucas":
            lucasOwes   = input("Lucas owes: $")
            
        if whoPaid != "William":
            williamOwes = input("William owes: $")
            
        if whoPaid != "Tara":
            taraOwes    = input("Tara owes: $")

        # let's add the occasion into occasionsSheet (as the last row)

        currentRow = [occasion,     date,
                      whoPaid,      jacobOwes,
                      lucasOwes,    williamOwes,
                      taraOwes]

        occasionsSheet.insert_row(currentRow, occasionsSheet.row_count + 1)

        # now we can add the row into the rest of the spreadsheet!

        print("\n")
        addRow(currentRow)

        again = input("\nInput another occasion (y/n)? ")
        print("\n")
        
else:
    
    # user wants this program to check the spreadsheet!

    # so... i guess... uh...
    # just check the last row? check whether the row's
    # values were all in the workbook already? if it isn't,
    # add it in AND THEN look at the row before that one,
    # and keep going until you find a row that's already
    # in there

    currentRow = occasionsSheet.row_values(occasionsSheet.row_count)

    for i in range(occasionsSheet.row_count - 1): # we don't want to end up reading the header row hehe

        currentRow = occasionsSheet.row_values(occasionsSheet.row_count - i)
        
        # we have to take the $ out of the strings! :(
        # IF THEY EXIST, THAT IS

        for r in range(len(currentRow) - 3):
            if not currentRow[r+3] is None:
                currentRow[r+3] = currentRow[r+3][1:]

        # don't want to pass a NoneType to addRow() :/
        
        for j in range(len(currentRow) - 3):
            if currentRow[j + 3] is None:
                currentRow[j + 3] = "0"
        
        if isNewRow(currentRow):

            print("row #" + str(i) + " is new!")
            
            # now we can add it in <3
            
            addRow(currentRow)

        else:
            if choice == "2":
                print("no more new rows!")
                break
            else:
                print("not a new row, but we're gonna keep on trucking")

# +-----------------------------------------------------+
# | =================== FUNCTIONS ===================== |
# |                                                     |
# | This is the last section, so I guess all the        |
# | function descriptions will be right above the func- |
# | tions themselves. I just wanted a block so you (I?) |
# | can tell that the main function ended. :)           |
# +-----------------------------------------------------+

# ---------------------------------------------------------------
# getWhoPaidColumn(list, whoPaid). Returns the column number that
# matches the name of whoPaid.

def getWhoPaidColumn(listOfNames, string):
    for i in range(len(listOfNames)):
        if string == listOfNames[i]:
            return i
    return 6

# ---------------------------------------------------------------
# occasionInNameSheet(name, occasion, date). True if
# occasion and date are found in a single row
# on any <name>Sheet.

def occasionInNameSheet(name, occasion, date):

    nameSheet = wholeBook.worksheet(name)
    
    # get all the dates for nameSheet

    dateColumn = nameSheet.col_values(5)

    # if any of the dates match the date of this occasion,
    # then check the occasion of that date. if the
    # occasion matches too, then return false. (this
    # way, we don't have to open up every row :D we just
    # have to open up one column and one row. #timesaver)
    
    for i in range(nameSheet.row_count - 2):
        if dateColumn[nameSheet.row_count - i - 1] == date:
            currentRow = nameSheet.row_values(nameSheet.row_count - i)
            if currentRow[3] == occasion:
                print("date(" + date + ") and occasion(" + occasion + ") match row " + str(i) + " of " + name + "'s sheet")
                return True
    print("date(" + date + ") and occasion(" + occasion + ") don't match " + name + "'s sheet.")
    return False

# ---------------------------------------------------------------
# isNewRow(list). True if the row wasn't already added to the
# <name>Sheets <3

def isNewRow(occasionData):

    occasion    = occasionData[0]
    date        = occasionData[1]
    whoPaid     = occasionData[2]
    
    if len(occasionData) >= 4:
        jacobOwes   = occasionData[3]
    else:
        jacobOwes = 0
        
    if len(occasionData) >= 5:
        lucasOwes = occasionData[4]
    else:
        lucasOwes = 0
        
    if len(occasionData) >= 6:
        williamOwes = occasionData[5]
    else:
        williamOwes = 0
    
    if len(occasionData) == 7:
        taraOwes = occasionData[6]
    else:
        taraOwes = 0

    # only check the <name>Sheets of people who owed something :/

    if float(jacobOwes) > 0:
        if occasionInNameSheet("Jacob", occasion, date):
            return False

    if float(lucasOwes) > 0:
        if occasionInNameSheet("Lucas", occasion, date):
            return False

    if float(williamOwes) > 0:
        if occasionInNameSheet("William", occasion, date):
            return False

    if float(taraOwes) > 0:
        if occasionInNameSheet("Tara", occasion, date):
            return False
                
    # if we get all the way to here without returning,
    # the row must be new! :D
    
    return True

# ---------------------------------------------------------------
# editNameSheet(name, nameOwes, occasion, date). Edits <name>'s <name>Sheet
# by putting in the occasion, date, and whatever <name> owes.

def editNameSheet(name, nameOwes, occasion, date, whoPaid):
    
    nameSheet  = wholeBook.worksheet(name)
    whoPaidCol = getWhoPaidColumn(nameSheet.row_values(2), whoPaid)
    
    nameSheet.insert_row(["0","0","0",occasion,date], nameSheet.row_count + 1)
    nameSheet.update_cell(nameSheet.row_count, whoPaidCol + 1, nameOwes)

    print(name + "'s sheet successfully edited.")

# ---------------------------------------------------------------
# addRow(list). Adds the row to the <name>Sheets

def addRow(occasionData):

    occasion    = occasionData[0]
    date        = occasionData[1]
    whoPaid     = occasionData[2]
    
    if len(occasionData) >= 4:
        jacobOwes   = occasionData[3]
    else:
        jacobOwes = 0
        
    if len(occasionData) >= 5:
        lucasOwes = occasionData[4]
    else:
        lucasOwes = 0
        
    if len(occasionData) >= 6:
        williamOwes = occasionData[5]
    else:
        williamOwes = 0
    
    if len(occasionData) == 7:
        taraOwes = occasionData[6]
    else:
        taraOwes = 0
    
    # now we add the occasion to the pages of whoever owes stuff. basically
    # if <name>Owes > 0, then we add something to <name>Sheet's
    # last row, in the column that matches whoPaid.
    
    if float(jacobOwes) > 0:
        editNameSheet("Jacob", jacobOwes, occasion, date, whoPaid)
        
    if float(lucasOwes) > 0:
        editNameSheet("Lucas", lucasOwes, occasion, date, whoPaid)       
        
    if float(williamOwes) > 0:
        editNameSheet("William", williamOwes, occasion, date, whoPaid)
        
    if float(taraOwes) > 0:
        editNameSheet("Tara", taraOwes, occasion, date, whoPaid)
        
