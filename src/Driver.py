from src.dbo.user import DBOUser
from src.models.user import User
from src import Logger
from src.ORSEN import ORSEN

# Database access
dbo_user = DBOUser('users', User)


""" A part of me tells me na we need to have a different method for getting input para mabilis na lang ayusin soon pag sa iba gagamitin."""
def get_input():
    user_input = input()
    return user_input

def login_signup():
    print("Hi! Do you have an account? (Y/N)")
    user_input = input()

    if user_input == "Y":  # login
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
            # store user
            set_global_curr_user(temp_user)
            print("Hi! Welcome back ", name)
            is_done = True

def signup(self):
    print("What's your username?")
    name = input()
    print("What's is the secret code?")
    code = input()

    self.set_global_curr_user(self.dbo_user.add_user(User(-1, name, code)))

def login_signup_automatic():
    print("What's your name?")
    name = get_input()

    user_list = dbo_user.get_user_by_name('name')
    if user_list is not []:
        print("Do we have a secret code?")
        has_code_answer = get_input()
        has_code = False

        if has_code_answer.lower() == "y" or has_code_answer.lower() == "yes":
            print("What is the secret code?")
            input_code = get_input()
            temp_user = dbo_user.get_specific_user(name, input_code)

        else:
            # has_code_answer.lower() == "n" or has_code_answer.lower() == "no":
            print("Alright then let's make one! What should it be?")
            input_code = get_input()
            temp_user = dbo_user.add_user(User(-1, name, input_code))

        set_global_curr_user(temp_user)
        print("Alright %s, let's make a story. You start!")


def set_global_curr_user(user):
    global curr_user
    curr_user = user


#start here
# Initialize loggers
Logger.setup_loggers()

#User objects
curr_user = None
login_signup()
print("done")

orsen = ORSEN()

is_engaged = True
while is_engaged:
    response = get_input()
    ORSEN.get_response(response)
    is_engaged = ORSEN.talk()


