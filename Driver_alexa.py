"""
This is the driver file for Alexa
"""

from src.dbo.user import DBOUser
from src.models.user import User
from src import Logger, IS_AFFIRM, IS_DENY, IS_END, UserHandler
from src.ORSEN import ORSEN
from src.textunderstanding.InputDecoder import InputDecoder

from flask import Flask, render_template, request, json
from flask_ask import Ask, statement, question, session

# change status to "login_signup" creates/logins users at the start
# change status to "start_storytelling" does not creates/logins users at the start. 
## It starts storytelling right away
status = "login_signup"
name = ""
code = ""
have_account = ""

def account_status(user_input):
    print(type(user_input))
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
    global status, dbo_user

    temp_user = dbo_user.get_specific_user(name, code)

    if temp_user is None:
        status = "ask_code"
        return "I don't think that's right. Can you try again? What's your username?"
    else:
        UserHandler.get_instance().set_global_curr_user(temp_user)
        status = "storytelling"
        return "Hi! Welcome back " + name + " . Let's make a story. You start!"

def signup():
    global status, dbo_user

    UserHandler.get_instance().set_global_curr_user(dbo_user.add_user(User(-1, name, code)))
    status = "storytelling"
    return "Alright" + name + ", let's make a story. You start!"

def is_end_story_func(response):
    if response.lower() in IS_END:
        return True
    return False

# Initialize Alexa
app = Flask(__name__)
ask = Ask(app, "/")

# Database access
dbo_user = DBOUser('users', User)

# start here
# Initialize loggers
Logger.setup_loggers()

print("---------Launching ORSEN---------")
orsen = ORSEN()

#import logging
#logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def welcome():

    global status

    orsen_response = "Hi! I'm ORSEN. "

    if status == "login_signup":
        orsen_response += "Do you have an account?"
        status = "account_status"
            
    elif status == "start_storytelling":
        orsen_response += "Let's make a story. You start!"
        status = "storytelling"

    return question(orsen_response)

@ask.intent("AMAZON.FallbackIntent")
def unknown():
    
    orsen_response = "I don't understand. Please repeat what you said"

    Logger.log_conversation("Alexa didn't get the trigger. Went to AMAZON.FallbackIntent")
    Logger.log_dialogue_model("Alexa didn't get the trigger. Went to AMAZON.FallbackIntent")

    Logger.log_conversation("ORSEN: " + str(orsen_response))
    Logger.log_dialogue_model("ORSEN: " + str(orsen_response))

    return question (orsen_response)

@ask.intent("TryAgain")
def error():
    orsen_response = "I don't understand. Please repeat what you said"

    Logger.log_conversation("Alexa didn't get the trigger. Went to TryAgain intent")
    Logger.log_dialogue_model("Alexa didn't get the trigger. Went to TryAgain intent")

    Logger.log_conversation("ORSEN: " + str(orsen_response))
    Logger.log_dialogue_model("ORSEN: " + str(orsen_response))

    return question (orsen_response) 

@ask.intent("searchQuery", convert={'query': str})
def driver(query):
    print(query)
    requestJson = request.get_json()
    print(requestJson['request']['intent']['name'])

    user_input = query
    global status, name, code, have_account

    if user_input == None:
        orsen_response = "Please try again"
        return question (orsen_response) 
    
    # if user_input == None:
    #     orsen_response = "Please try again"
    #     Logger.log_conversation("Alexa didn't get the trigger")
    #     Logger.log_dialogue_model("Alexa didn't get the trigger")

    #     Logger.log_conversation("ORSEN: " + str(orsen_response))
    #     Logger.log_dialogue_model("ORSEN: " + str(orsen_response))

    #     return question (orsen_response) 
    
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
            # orsen_response = "STORY TIME"
            Logger.log_conversation("ORSEN: " + str(orsen_response))
        else:
            orsen_response = "Thank you for the story! Do you want to hear it again?"
            status = "repeat_story"
        
    elif status == "repeat_story":
        orsen_response = ""
        if user_input.lower() in IS_AFFIRM:
            # TODO Connect to back end, get repetition 
            orsen_response = orsen.repeat_story()
            # orsen_response = "Repeating Story..."
        orsen_response += " Do you want to create another story?"
        status = "create_another_story"
        
    elif status == "create_another_story":
        if user_input.lower() in IS_AFFIRM:
            orsen_response = "Ok! Let's make another story! You go first"
            status = "storytelling"
        else:
            orsen_response = "Ok! Goodbye."
            status = "end_session"
    
    if status == "end_session":
        return statement (orsen_response) 

    return question(orsen_response)

if __name__ == '__main__':

    app.run(debug=True)