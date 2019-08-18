from src.run import extract_info, new_world, get_unkown_word
from src.dialoguemanager.DialoguePlanner import *
from flask import Flask
from flask import jsonify
from flask import request
from flask import json
import datetime
import requests
import re
from src.dialoguemanager.story_generation import generate_basic_story, generate_collated_story
from src.inputprocessor.infoextraction import getCategory, CAT_STORY
from src.db import DBO_User, User
#import logging
app = Flask(__name__)

#gunicorn_error_logger = logging.getLogger('gunicorn.error')
#app.logger.handlers.extend(gunicorn_error_logger.handlers)
#app.logger.setLevel(logging.DEBUG)
#app.logger.debug('this will show in the log')

storyId = -1
output = "Hello, I am ORSEN. Let's start."
retrieved = None
nIR = {"I can't hear you", "Sorry. What did you say again?", "Okay"}
tts = "Sorry. What did you say again?"
dt = "Sorry. What did you say again?"

focus = None

manwal_kawnt = 0
MAKSIMUM_KAWNT = 5
endstory = False
endstorygen = False
endconvo = False

story_list = []
turn_count = 0
userid = -1
username = ""
secret_code = ""

#FOR FILES
convo_path ="D:/Desktop/Jilyan/Academics/College/THESIS/Conversation Logs"
information_path ="D:/Desktop/Jilyan/Academics/College/THESIS/Information Extraction Logs"
dialogueLogs ="D:/Desktop/Jilyan/Academics/College/THESIS/Dialogue Model Logs"

date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

def main_intent():
	return None


@app.route('/', methods=["GET","POST"])
def home():
	print("HOME")
	return jsonify({"Page":"Home"})
	
@app.route('/orsen', methods=["POST"])
def orsen():
	global manwal_kawnt, storyId, endstory, endstorygen, story_list, turn_count, userid, username, secret_code
	
	#print(json.dumps(request.get_json()))
	requestJson = request.get_json()
	
	focus = requestJson["inputs"][0]#["rawInputs"][0]["query"]
	#print(focus["intent"])
    
    #FOR FILES - OPEN
	dm_fileWriter = open(dialogueLogs+ "/" + date+".txt", "a")
	convo_fileWriter = open(convo_path+ "/" + date+".txt", "a")
	ie_fileWriter = open(information_path+ "/" + date+".txt", "a")
	
	#When the app invocation starts, create storyid and greet the user and reset reprompt count
	if focus["intent"] == "actions.intent.MAIN":
		storyId = storyId + 1
		print("STORY ID ",storyId)
		new_world(storyId)
		#reset reprompt count
		manwal_kawnt = 0
		turn_count = 1
		story_list = []
		#greet user (app.ask)
		data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Hi! What's your name?"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
        
		#FOR 
		convo_fileWriter.write(date + "\n")
		ie_fileWriter.write(date + "\n")
		dm_fileWriter.write(date + "\n")
		convo_fileWriter.write("ORSEN: Hi! What's your name?" + "\n")

	elif focus["intent"] == "actions.intent.GIVE_IDEA_ORSEN":
		data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Okay, I will give you a hint"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
        
        #FOR FILES
		convo_fileWriter.write("ORSEN: Okay, I will give you a hint" + "\n")
	
	
	#When there is no input: ask the user (prompt from model) until maximum count is reached 
	elif focus["intent"] == "actions.intent.NO_INPUT":
		#increment reprompt count
		manwal_kawnt = manwal_kawnt + 1
		#app termination when maximum reprompt count is reached
		if manwal_kawnt == MAKSIMUM_KAWNT:
			data = {"expectUserResponse": False, "finalResponse": {"speechResponse": {"textToSpeech": "Okay. Goodbye"}}}
            
			#FOR FILES - CLOSE
			convo_fileWriter.write("ORSEN: Okay. Goodbye" + "\n")
			convo_fileWriter.close()
			ie_fileWriter.write("~~~ Story Ends Because of No Input ~~~" + "\n")
			ie_fileWriter.close()


			world = server.get_world(storyId)
			dm_fileWriter.write("\n\n")
			dm_fileWriter.write("---DIALOGUE MOVE COUNTS--- \n")
			dm_fileWriter.write("FEEdBACK COUNTS: "+ str(world.feedback_count) + "\n")
			dm_fileWriter.write("GENERAL COUNTS: "+ str(world.general_pump_count) + "\n")
			dm_fileWriter.write("SPECIFIC COUNTS: " + str(world.specific_pump_count) + "\n")
			dm_fileWriter.write("PROMPT COUNTS: " + str(world.prompt_count) + "\n")
			dm_fileWriter.write("HINT COUNTS: " + str(world.hint_count) + "\n")
			dm_fileWriter.write("SUGGEST COUNTS: " + str(world.suggest_count) + "\n")
			dm_fileWriter.write("FOLLOWUP1 COUNTS: " + str(world.followup1_count) + "\n")
			dm_fileWriter.write("FOLLOWUP2 COUNTS: " + str(world.followup2_count) + "\n")

			dm_fileWriter.write("---COMBINATION DIALOGUE MOVE COUNTS--- \n")
			dm_fileWriter.write("F + General: "+ str(world.feedback_general_count) + "\n")
			dm_fileWriter.write("F + Specific: "+ str(world.feedback_specific_count) + "\n")
			dm_fileWriter.write("F + Hinting: "+ str(world.feedback_hint_count) + "\n")
			dm_fileWriter.write("F + Suggesting: "+ str(world.feedback_suggest_count) + "\n")

			dm_fileWriter.write("---SUGGESTION YES/NO--- \n")
			dm_fileWriter.write("Yes: "+ str(world.yes) + "\n")
			dm_fileWriter.write("No: "+ str(world.no) + "\n")

			dm_fileWriter.write("---Follow Up1 Don'tLike/Wrong--- \n")
			dm_fileWriter.write("Don't Like: "+ str(world.dontLike) + "\n")
			dm_fileWriter.write("Wrong: "+ str(world.wrong) + "\n")

			dm_fileWriter.write("---Follow Up2 in/not--- \n")
			dm_fileWriter.write("In Choices: "+ str(world.inChoices) + "\n")
			dm_fileWriter.write("None of the Above: "+ str(world.notInChoices) + "\n")

			dm_fileWriter.write("---GLOBAL + LOCAL CONCEPTS --- \n")
			dm_fileWriter.write("GLOBAL CONCEPT LIST: " + str(world.global_concept_list) + "\n")
			dm_fileWriter.write("LENGTH GLOBAL CONCEPT LIST: " + str(len(world.global_concept_list)) + "\n")
			dm_fileWriter.write("LOCAL CONCEPT LIST: " + str(world.local_concept_list) + "\n")
			dm_fileWriter.write("LENGTH LOCAL CONCEPT LIST: " + str(len(world.local_concept_list)) + "\n")
			dm_fileWriter.write("END OF SESSION")

			dm_fileWriter.close()
		#reprompt user
		else:
			#get the reprompt
			retrieved = retrieve_output("", storyId, userid, dm_fileWriter)
			
			if retrieved.type_num == MOVE_HINT:
				extract_info(userid, retrieved.get_string_response())
	
			output_reply = retrieved.get_string_response()
			#reprompt user
			data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":""+output_reply+""}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
	
	elif turn_count == 1:
		rawTextQuery = requestJson["inputs"][0]["rawInputs"][0]["query"]
		turn_count = turn_count + 1
		username = str(rawTextQuery).split()
		username = username[len(username)-1].lower()
		convo_fileWriter.write("CHILD: My name is " + username + "\n")
		ie_fileWriter.write("Child name is " + username + "\n")
		data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Do we have a secret code?"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
		
	elif turn_count == 2:
		rawTextQuery = requestJson["inputs"][0]["rawInputs"][0]["query"]
		if "yes" in str(rawTextQuery).lower():
			turn_count = turn_count + 2
			data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"I see, can you tell me what it is?"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
		else:
			turn_count = turn_count + 1
			data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"I see, let's make one then. So what will it be?"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
		
	elif turn_count == 3:
		rawTextQuery = requestJson["inputs"][0]["rawInputs"][0]["query"]
		if str(rawTextQuery) != "":
			secret_code = str(rawTextQuery).split()
			secret_code = secret_code[len(secret_code)-1].lower()
			turn_count = turn_count + 2
			# add to DB
			user = User.User(-1, username, secret_code)
			if DBO_User.get_user_id(username, secret_code) == -1:
				DBO_User.add_user(user)
			# get user id
			userid = DBO_User.get_user_id(username, secret_code)
			data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Yey, a new friend! Let's make a story. You go first " + username + "."}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}

	elif turn_count == 4:
		rawTextQuery = requestJson["inputs"][0]["rawInputs"][0]["query"]
		secret_code = str(rawTextQuery).split()
		secret_code = secret_code[len(secret_code)-1].lower()
		# check if username and secret code match in db

		userid = DBO_User.get_user_id(username, secret_code)
		
		if userid != -1:
			turn_count = turn_count + 1
			data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Oh, you remembered " + username + "! Okay, let's make a story then. You start!"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
		else:
			print("try again")
			data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Hmm, I don't think that was our secret code. Why don't you give it another try " + username + "?"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}

	#When there is input, simply pass to model and get reply
	else:
		rawTextQuery = requestJson["inputs"][0]["rawInputs"][0]["query"]
	
		manwal_kawnt =0
		# userId = requestJson["user"]["userId"] # some really long id
		data = {}
		genstory = ""
	
		#print(rawTextQuery + " ["+userId+"]")

		if endstory:
			rawTextQuery = requestJson["inputs"][0]["rawInputs"][0]["query"]
			#If user wants to create another story, create new story and reset reprompt counts
			# if user wants to hear the whole story
			if (not endstorygen) and (rawTextQuery == "yes" or rawTextQuery == "yes." or rawTextQuery == "sure" or rawTextQuery == "sure." or rawTextQuery == "yeah" or rawTextQuery == "yeah."):
				#(edit-addhearstory-p2)swapped the contents of first and this condition
				output_reply = generate_collated_story(server.get_world(storyId))
				print("-----======= GENERATED STORY =======------")
				print(output_reply)
				data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":""+output_reply+""+". Do you want to create another story?"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
				endstorygen = True
                
				#FOR FILES
				convo_fileWriter.write("CHILD: "+ rawTextQuery + "\n")
				convo_fileWriter.write("ORSEN: "+ output_reply + "Do you want to create another story?" + "\n")
			
			# user does not want to hear the full story
			elif not endstorygen:
				#(edit-addhearstory-p1) changed prompt from 'hear story' to 'create story'
				data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Okay. Do you want to create another story?"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
				endstorygen = True
                
				#FOR FILES
				convo_fileWriter.write("CHILD: "+ rawTextQuery + "\n")
				convo_fileWriter.write("ORSEN: Okay. Do you want to create another story?" + "\n")
				
			# user wants to create a new story
			elif endstorygen and (rawTextQuery == "yes" or rawTextQuery == "yes." or rawTextQuery == "sure" or rawTextQuery == "sure." or rawTextQuery == "yeah" or rawTextQuery == "yeah."):
				#(edit-addhearstory-p2) swapped the contents of first and this condition
				data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Okay then, Let's create a story. You start"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
				manwal_kawnt = 0
				storyId = storyId + 1
				print("STORY ID ",storyId)
				new_world(storyId)
				endstorygen = False
				endstory = False
				story_list = []
				turn_count = 0
                
				#FOR FILES
				convo_fileWriter.write("CHILD: "+ rawTextQuery + "\n")
				convo_fileWriter.write("ORSEN: Okay then, Let's create a story. You start" + "\n")
				
			#If the user does not want to create a new story 
			else:
				#inserted, generatestory
				data = {"expectUserResponse": False, "finalResponse": {"speechResponse": {"textToSpeech": "Thank you. Goodbye"}}}
				endstorygen = False
				endstory = False
				story_list = []
				turn_count = 0
                
				#FOR FILES - CLOSE
				convo_fileWriter.write("CHILD: "+ rawTextQuery + "\n")
				convo_fileWriter.write("ORSEN: Thank you. Goodbye" + "\n")
				end = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
				convo_fileWriter.write(end)
				convo_fileWriter.close()

				ie_fileWriter.write("~~~ End Session ~~~")
				ie_fileWriter.write(end)
				ie_fileWriter.close()
				
		#when the user says they want to stop telling the story
		elif rawTextQuery.lower() == "bye" or rawTextQuery.lower() == "the end" or rawTextQuery.lower() == "the end.":
			#(edit-addhearstory-p1) changed the prompt from 'create another story' to 'hear full story'
			data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":"Wow. Thanks for the story. Do you want to hear the full story?"}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
			endstory = True
            
			#FOR FILES
			convo_fileWriter.write("CHILD: "+ rawTextQuery + "\n")
			convo_fileWriter.write("ORSEN: Wow. Thanks for the story. Do you want to hear the full story?" + "\n")
            
		else:
			result = None
			story_list.append(rawTextQuery)
			# if the reply is a story, then extract info and add in story. If not, then don't add
			if getCategory(rawTextQuery) == CAT_STORY:
				# you can pass user id here
				story_list[len(story_list)-1] = extract_info(userid, story_list, ie_fileWriter)
				result = get_unkown_word()
			
			if result != None:
				output_reply = "I need help! Please use " + result + " in a sentence."

			else:
				#dialogue
				#get the dialogue regardless of type
				retrieved = retrieve_output(rawTextQuery, storyId, userid, dm_fileWriter)

				if retrieved.type_num == MOVE_HINT:
					extract_info(userid, retrieved.get_string_response(), ie_fileWriter)

				output_reply = retrieved.get_string_response()
				
			data = {"conversationToken":"{\"state\":null,\"data\":{}}","expectUserResponse":True,"expectedInputs":[{"inputPrompt":{"initialPrompts":[{"textToSpeech":""+output_reply+""}],"noInputPrompts":[{"textToSpeech":tts,"displayText":dt}]},"possibleIntents":[{"intent":"actions.intent.TEXT"}]}]}
	
			print("I: ", rawTextQuery)
			print("O: ", output_reply)

			convo_fileWriter.write("Child: " + rawTextQuery + "\n")
			convo_fileWriter.write("ORSEN: " + output_reply + "\n")
	
	
	#if expectedUserResponse is false, change storyId
	
	return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)
