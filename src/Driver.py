from src.dbo.user import DBOUser
from src.models.user import User
from src import Logger, IS_AFFIRM, IS_DENY, IS_END, UserHandler, DIALOGUE_TYPE_E_END, DIALOGUE_TYPE_RECOLLECTION, Pickle
from src.ORSEN import ORSEN
from src.textunderstanding.InputDecoder import InputDecoder
import datetime

import time

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

def clean_user_input(response):
    response = response.strip()
    if response.endswith(".") == False:
        response = response + "."

    return response

def start_storytelling():
    is_end_story = False
    while not is_end_story:
        start_time = time.time()
        user_input = get_input() #TODO: Uncomment after testing

        print("TRYING TO GET TIME %s: " % (time.time() - start_time))
        print("TRYING TO GET TIME again : ", str(time.time() - start_time))

        Logger.log_conversation("LATENCY TIME (seconds): " + str(time.time() - start_time))
        # user_input = "John kicked the love"
        user_input = clean_user_input(user_input)

        Logger.log_conversation("User : " + str(user_input))

        is_end_story = orsen.is_end_story(user_input)
        print("IS END STORY: ", is_end_story)

        if not is_end_story:
            orsen_response = orsen.get_response(user_input)
            print("=========================================================")
            print("EDEN:", orsen_response)
            print("=========================================================")
            Logger.log_conversation("EDEN: " + str(orsen_response))
            is_end_story = orsen.is_end_story(user_input)
        else:
            """EDEN"""
            # orsen_response = orsen.get_response("", move_to_execute = DIALOGUE_TYPE_E_END)
            orsen_response = orsen.get_response("", move_to_execute = DIALOGUE_TYPE_RECOLLECTION)
            # orsen_response = orsen_response + orsen.get_response("", move_to_execute = DIALOGUE_TYPE_RECOLLECTION)
            print("=========================================================")
            print("EDEN:", orsen_response)
            print("=========================================================")
            Logger.log_conversation("EDEN: " + str(orsen_response))




            # is_end_story = True

            # """ORSEN"""
            # print("Thank you for the story! Do you want to hear it again?")
            # user_input = get_input()
            # if user_input.lower() in IS_AFFIRM:
            #     print(orsen.repeat_story())

orsen = ORSEN()

# start here
# Initialize loggers
Logger.setup_loggers()

#Retrieve User Details --- User objects
print("---------Retrieving User Details---------")
login_signup()
print("done")

# pickle_filepath = '../logs/user world/' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + "-" + UserHandler.get_instance().curr_user.name
pickle_filepath = '../logs/user world/' + UserHandler.get_instance().curr_user.name
# pickle_filepath = '../Mod_ORSEN_v2//logs/user world/' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + "-" + UserHandler.get_instance().curr_user.name

# try:
#
#
#
#     print("---------Launching ORSEN---------")
#
#     #TODO: uncomment after testing
#     #for repeating the story
#     is_engaged = True
#     while is_engaged:
#         orsen.initialize_story_prerequisites()
#         print("Let's make another story! You go first")
#         start_storytelling()
#
#         #save story world
#         Pickle.pickle_world_wb(pickle_filepath, orsen.world.get_pickled_world())
#
#         print("Do you want to make another story?")
#         user_input = get_input()
#         if user_input.lower() in IS_DENY:
#             is_engaged = False
#         # else:
#             # pickle_filepath = '../logs/user world/' + datetime.datetime.now().strftime(
#             #     "%Y-%m-%d %H-%M-%S") + "-" + UserHandler.get_instance().curr_user.name
#             # pickle_filepath = '../Mod_ORSEN_v2//logs/user world/' + datetime.datetime.now().strftime(
#             #     "%Y-%m-%d %H-%M-%S") + "-" + UserHandler.get_instance().curr_user.name
#
#
# except:
#     print("Something went wrong when writing to the file")
# finally:
#     print("AT FINALLY")
#     Pickle.pickle_world_wb(pickle_filepath, orsen.world.get_pickled_world())
#     Pickle.pickle_world_rb(pickle_filepath)
# print("---------Closing ORSEN---------")



# Logger.setup_loggers()
# print("---------Launching ORSEN---------")
# orsen.initialize_story_prerequisites()
# print("Let's make another story! You go first")
# start_storytelling()
# print("---------Closing ORSEN---------")


print("---------Launching ORSEN---------")

# #TODO: uncomment after testing
#for repeating the story
is_engaged = True
while is_engaged:
    orsen.initialize_story_prerequisites()
    print("Let's make another story! You go first")
    start_storytelling()

    #save story world
    Pickle.pickle_world_wb(pickle_filepath, orsen.world.get_pickled_world())

    print("Do you want to make another story?")
    user_input = get_input()
    if user_input.lower() in IS_DENY:
        is_engaged = False