from src.dbo.user import DBOUser
from src.models.user import User

#Database access
dbo_user = DBOUser('users', User)

#User objects
curr_user = None

def login_signup():
    print("Hi! Do you have an account? (Y/N)")
    user_input = input()

    if user_input == "Y": #login
        login()
    else:
        signup()
    print(curr_user)

def login():
    # ask for user details
    is_done = False

    while not is_done:
        print("What's your username?")
        name = input()
        print("What's is the secret code?")
        code = input()

        temp_user = dbo_user.get_specific_user(name, code)

        if temp_user is None:
            print("I don't think that's right. Can you try again?")

        else:
            #store user
            set_global_curr_user(temp_user)
            print("Hi! Welcome back ", name)
            is_done = True

def signup():
    print("What's your username?")
    name = input()
    print("What's is the secret code?")
    code = input()

    set_global_curr_user(dbo_user.add_user(User(-1, name,code)))

def set_global_curr_user(user):
    global curr_user
    curr_user = user

#start here
login_signup()
