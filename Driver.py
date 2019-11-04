from src.dbo.user import DBOUser
from src.models.user import User
from src import Logger, IS_AFFIRM, IS_DENY, IS_END, UserHandler
from src.ORSEN import ORSEN
from src.textunderstanding.InputDecoder import InputDecoder

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
    print(UserHandler.get_instance().curr_user)

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
            UserHandler.get_instance().set_global_curr_user(temp_user)
            print("Hi! Welcome back ", name)
            is_done = True

def signup():
    print("What's your username?")
    name = input()
    print("What's is the secret code?")
    code = input()

    UserHandler.get_instance().set_global_curr_user(dbo_user.add_user(User(-1, name, code)))

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

        UserHandler.get_instance().set_global_curr_user(temp_user)
        print("Alright %s, let's make a story. You start!")

def is_end_story_func(response):
    if response.lower() in IS_END:
        return True
    return False

def clean_user_input(response):
    response = response.strip()
    if response.endswith(".") == False:
        response = response + "."

    return response


def start_storytelling():
    is_end_story = False
    while not is_end_story:
        user_input = get_input() #TODO: Uncomment after testing
        # user_input = "John kicked the love"
        user_input = clean_user_input(user_input)

        if UserHandler.get_instance().curr_user is None:
            Logger.log_conversation("User : " + str(user_input))
        else:
            Logger.log_conversation(UserHandler.get_instance().curr_user.name.strip() + ": " + str(user_input))

        is_end_story = is_end_story_func(user_input)

        if not is_end_story:
            orsen_response = orsen.get_response(user_input)
            print("ORSEN:", orsen_response)
            Logger.log_conversation("ORSEN: " + str(orsen_response))
        else:
            print("Thank you for the story! Do you want to hear it again?")
            user_input = get_input()
            if user_input.lower() in IS_AFFIRM:
                print(orsen.repeat_story())


# start here
# Initialize loggers
Logger.setup_loggers()

#Retrieve User Details --- User objects
print("---------Retrieving User Details---------")
#login_signup()
print("done")


print("---------Launching ORSEN---------")
orsen = ORSEN()

# test_sentence = "My mother's name is Sasha, she likes dogs."
# test_sentence = "John kicked the ball."
# test_sentence = "The ball was kicked by John."
# test_sentence = "John the mighty is a brave, strong warrior"
# test_sentence = "Once there was a boy"

# orsen_response = orsen.get_response(test_sentence)

#TODO: uncomment after testing
#for repeating the story
is_engaged = True
while is_engaged:
    orsen.initialize_story_prerequisites()
    print("Let's make another story! You go first")
    start_storytelling()
    print("Do you want to make another story?")
    user_input = get_input()
    if user_input.lower() in IS_DENY:
        is_engaged = False



print("---------Closing ORSEN---------")


