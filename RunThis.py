import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

# --- FUNCTIONS ---------------------------------------------

# getWhoPaidColumn(list, whoPaid). Returns the column number that
# matches the name of whoPaid.

def getWhoPaidColumn(listOfNames, string):
    for i in range(len(listOfNames)):
        if string == listOfNames[i]:
            return i
    return 6

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
        devanOwes = occasionData[4]
    else:
        devanOwes = 0
        
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

    if float(devanOwes) > 0:
        if occasionInNameSheet("Devan", occasion, date):
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

# editNameSheet(name, nameOwes, occasion, date). Edits <name>'s <name>Sheet
# by putting in the occasion, date, and whatever <name> owes.

def editNameSheet(name, nameOwes, occasion, date, whoPaid):
    
    nameSheet  = wholeBook.worksheet(name)
    whoPaidCol = getWhoPaidColumn(nameSheet.row_values(2), whoPaid)
    
    nameSheet.insert_row(["0","0","0",occasion,date], nameSheet.row_count + 1)
    nameSheet.update_cell(nameSheet.row_count, whoPaidCol + 1, nameOwes)

    print(name + "'s sheet successfully edited.")

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
        devanOwes = occasionData[4]
    else:
        devanOwes = 0
        
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
        
    if float(devanOwes) > 0:
        editNameSheet("Devan", devanOwes, occasion, date, whoPaid)       
        
    if float(williamOwes) > 0:
        editNameSheet("William", williamOwes, occasion, date, whoPaid)
        
    if float(taraOwes) > 0:
        editNameSheet("Tara", taraOwes, occasion, date, whoPaid)
        
# --- MAIN --------------------------------------------------

# variables

names = ["Jacob","Devan","William","Tara"]

choice      = 1
again       = "y"

occasion    = ""
date        = ""
whoPaid     = ""

jacobOwes   = 0
devanOwes   = 0
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
devanSheet       = wholeBook.worksheet("Devan")
williamSheet     = wholeBook.worksheet("William")
taraSheet        = wholeBook.worksheet("Tara")

# so basically this program is supposed to either:
# 
# (A) take in user input for the occasion
#     and put it into the spreadsheet (so the
#     user doesn't have to open their browser), or
#
# (B) check the last few rows of the occasionSheet
#     to see if there are any new occasions that
#     someone else added! if there are any, add
#     them to the other <name>Sheets and update
#     totalsSheet <3

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
            
        if whoPaid != "Devan":
            devanOwes   = input("Devan owes: $")
            
        if whoPaid != "William":
            williamOwes = input("William owes: $")
            
        if whoPaid != "Tara":
            taraOwes    = input("Tara owes: $")

        # let's add the occasion into occasionsSheet (as the last row)

        currentRow = [occasion,     date,
                      whoPaid,      jacobOwes,
                      devanOwes,    williamOwes,
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
            print("no more new rows!")
            break























