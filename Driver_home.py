"""
This is the driver file for Google Home/ Google Assistant
The other files needed can be dound under the src folder then googlehome folder
Don't forget to delete creds.data 
"""


from src.dbo.user import DBOUser
from src.models.user import User
from src import Logger, IS_AFFIRM, IS_DENY, IS_END, UserHandler, Pickle, CURR_ORSEN_VERSION
from src.ORSEN import ORSEN
from src.textunderstanding.InputDecoder import InputDecoder
from src.googlehome import json_reply
from src.constants import *
from flask import Flask
from flask import jsonify
from flask import request
from flask import json
import time

# change status to "login_signup" creates/logins users at the start
# change status to "start_storytelling" does not creates/logins users at the start. 
## It starts storytelling right away
status = "login_signup"
name = ""
code = ""
have_account = ""
pickle_filepath = '../Mod_ORSEN_v2/logs/user world/'

def initialize_orsen():
    orsen.initialize_story_prerequisites()
    orsen.world.reset_world()
    orsen.dialogue_planner.reset_new_world()

def account_status(user_input):
    global have_account
    if user_input.lower() in IS_AFFIRM:
        have_account = True
    else:
        have_account = False

def login_signup():
    if have_account == True:
        # Verify Account
        return login()
    else:
        # Create Account
        return signup()
        
def login():
    global status, dbo_user, pickle_filepath, orsen

    temp_user = dbo_user.get_specific_user(name, code)

    if temp_user is None:
        status = "ask_code"
        return "I don't think that's right. Can you try again? What's your username?"
    else:
        UserHandler.get_instance().set_global_curr_user(temp_user)
        status = "storytelling"
        pickle_filepath = pickle_filepath + name
        
        initialize_orsen()

        temp_welcome = orsen.get_response(move_to_execute=orsen.dialogue_planner.get_welcome_message_type())
        return "Hi! Welcome back " + name + " . " + temp_welcome

def signup():
    global status, dbo_user, pickle_filepath, orsen

    UserHandler.get_instance().set_global_curr_user(dbo_user.add_user(User(-1, name, code)))
    status = "storytelling"
    pickle_filepath = pickle_filepath + name
    
    initialize_orsen()

    temp_welcome = orsen.get_response(move_to_execute=orsen.dialogue_planner.get_welcome_message_type())
    return "Alright " + name + " . " + temp_welcome

def is_end_story_func(response):
    return orsen.is_end_story(response)

# Initialize Google Home
app = Flask(__name__)

# Database access
dbo_user = DBOUser('users', User)

# start here
# Initialize loggers
Logger.setup_loggers()

print("---------Launching ORSEN---------")
orsen = ORSEN()

@app.route('/orsen', methods=["POST"])
def driver():

    global status, name, code, have_account, orsen
    global pickle_filepath

    requestJson = request.get_json()
    focus = requestJson["inputs"][0]
    data = {}
    user_input = ""

    if focus["intent"] != "actions.intent.NO_INPUT":
        user_input = requestJson["inputs"][0]["rawInputs"][0]["query"]

    if focus["intent"] == "actions.intent.NO_INPUT":
        orsen_response = "I can't seem to hear you. What did you say?"
        Logger.log_conversation("NO INPUT : " + str(orsen_response))
        data = json_reply.response(orsen_response)


    # Greet the User
    elif focus["intent"] == "actions.intent.MAIN":

        orsen_response = "Hi! I'm " + CURR_ORSEN_VERSION + ". "

        if status == "login_signup":
            orsen_response += "Do you have an account?"
            status = "account_status"
            
        elif status == "start_storytelling":
            initialize_orsen()

            temp_welcome = orsen.get_response(move_to_execute=orsen.dialogue_planner.get_welcome_message_type())
            orsen_response += temp_welcome
            status = "storytelling"
        
        data = json_reply.response(orsen_response)
    
    else:
        # LOGIN SIGNUP
        if status == "account_status":
            account_status(user_input)
            status = "ask_username"

        if status == "ask_username":
            orsen_response = "What's your username?"
            status = "ask_code"

        elif status == "ask_code":
            name = user_input
            orsen_response = "What's your code?"
            status = "login_signup"
        
        elif status == "login_signup":
            code = user_input
            orsen_response = login_signup()
        
        # STORYTELLING
        elif status == "storytelling":
            if UserHandler.get_instance().curr_user is None:
                Logger.log_conversation("User : " + str(user_input))
            else:
                Logger.log_conversation(UserHandler.get_instance().curr_user.name.strip() + ": " + str(user_input))

            is_end_story = is_end_story_func(user_input)

            if not is_end_story:
                # TODO Connect to back end, get the response
                orsen_response = orsen.get_response(user_input)
                Logger.log_conversation(CURR_ORSEN_VERSION + ": " + str(orsen_response))
                is_end_story = is_end_story_func(user_input)
                print("IM AT END STORY FIRST")

            if is_end_story:
                if CURR_ORSEN_VERSION == EDEN:
                    try:
                        Pickle.pickle_world_wb(pickle_filepath, orsen.world.get_pickled_world())
                        print("TRYING TO STORE PICKLE")
                    except Exception as e:
                        print("Error: ", e)

                    # orsen_response = orsen_response + " Do you want to make a new story?"
                    orsen_response = "Do you want to share another story?"
                    print("IM AT END STORY STATUS")
                    status = "create_another_story"
                else:
                    orsen_response = "Thank you for the story! Do you want to hear it again?"
                    status = "repeat_story"

        elif status == "repeat_story":
            if user_input.lower() in IS_AFFIRM:
                # TODO Connect to back end, get repetition
                orsen_response = orsen.repeat_story()
                # orsen_response = "Repeating Story..."
            orsen_response += " Do you want to create another story?"
            status = "create_another_story"
        
        elif status == "create_another_story":
            print("IM AT CREATE NEW STORY")
            if user_input.lower() in IS_AFFIRM:
                initialize_orsen()

                temp_welcome = orsen.get_response(move_to_execute=orsen.dialogue_planner.get_welcome_message_type())
                # orsen_response = "Ok! Let's make another story! You go first"
                orsen_response = "Ok! " + temp_welcome

                status = "storytelling"
            else:
                orsen_response = "Ok! Goodbye."
                status = "end_session"
    
    if status == "end_session":
        data = json_reply.final_response(orsen_response)
    else:
        data = json_reply.response(orsen_response)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)
