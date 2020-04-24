import gspread
from oauth2client.service_account import ServiceAccountCredentials
import hashlib, binascii, os
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)
sheet = client.open('testdb').sheet1
#Sets first column to the username dictionary
usernameDictionary = (sheet.col_values(1)) #Time of O(N)

#Enters new user info into database
def insertUser(username, password):
    sheet.insert_row([username, password],2)

#Used for creating accounts
def password():
    passwordSame = False #set flag
    while passwordSame == False: #while passwords are not the same
        print('Password:')
        userPassword = input() #allow user to enter password
        print('Please verify password:')
        userPasswordCheck = input() #allow user to enter password again
        if userPassword == userPasswordCheck:
            passwordSame = True
            print('Your passwords have matched. Good job.')
        else:
            print('Your passwords are different.\n')
    return hash_password(userPassword) #Returns hashed password

#Used for creating accounts
def username():
    usernameMatch = True
    while usernameMatch == True:
        print ('Username:')
        username = input()
        print ('checking username......\n')
        if username in usernameDictionary:
            print("This username is already being used. Please try again.")
        else:
            usernameMatch = False
    return username

#Takes a password and hashes it.
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

#Takes a password from database and a user entered password and see if they match.
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

#Creates a new account
def newAccount():
    print('Creating account...!\n')
    insertUser(username(), password())

#Signs into existing account
def signIn():
    print('What is your username?')
    username = input()
    #Searches database for username
    cell = sheet.find(username)
    #Takes found username row, then finds hashed password
    hashedPassword = (sheet.cell(cell.row, 2)).value
    #Asks user for plain text password
    print('What is your password?')
    password = input()
    #Compares hashed password with plain text. Determines if correct.
    if (verify_password(hashedPassword, password)) == True:
        print('You are signed in!')
    else:
        print('Incorrect password.')

#First screen you see
def welcome():
    print('Welcome. Would you like to Sign in [1], or Sign up [2]?')
    option = input()
    if option == '1':
        signIn()
    elif option == '2':
        newAccount()
#------Start of program------
welcome()
