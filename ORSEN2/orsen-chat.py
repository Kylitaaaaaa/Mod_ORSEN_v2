from src.run import extract_info, new_world
from src.dialoguemanager.DialoguePlanner import *
from flask import Flask
from flask import jsonify
from flask import request
from flask import json, make_response
from flask_cors import CORS
import requests
import re
from src.dialoguemanager.story_generation import generate_basic_story, generate_collated_story
#import logging
app = Flask(__name__)
CORS(app)

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
startconvo = False
endstory = False
endstorygen = False


def main_intent():
	return None


@app.route('/', methods=["GET","POST"])
def home():
	print("HOME")
	return jsonify({"Page":"Home"})
	
@app.route('/orsen', methods=["POST"])
def orsen():
	global manwal_kawnt, storyId, startconvo, endstory, endstorygen
	
	print(json.dumps(request.get_json()))
	requestJson = request.get_json()
	
	focus = requestJson["text"]
	print(focus)
	
	output_reply = '~~Orsen is sleeping. Tell Orsen to "make a story"~~'
	
	#first conditional chain
	if not startconvo and (focus == "I want to make a story" or 
	focus == "I want to tell a story" or focus == "Tell a story" or focus == "Make a story" or focus == "make a story"):
		output_reply = 'Okay. Let us create a story, you start!' #generate_collated_story(server.get_world(storyId))
		storyId = storyId + 1
		print("STORY ID ",storyId)
		#new_world(storyId)
		startconvo = True
		endstory = False
		endstorygen = False
	
	elif ("The end" in focus) and startconvo and not endstory:
		output_reply = 'Wow. Thanks for the story. Do you want to hear the full story?'
		endstory = True
		
	elif endstory and not endstorygen and focus == "yes" and startconvo:
		output_reply = 'here is the generated story.'+generate_collated_story(server.get_world(storyId))+ ' Do you want to create another story?' 
		endstorygen = True
		
	elif endstory and not endstorygen and startconvo:
		output_reply = 'Okay. Do you want to create another story?'
		endstorygen = True
	
	elif endstory and endstorygen and focus == "yes" and startconvo:
		output_reply = 'Okay. Let us create a story, you start!'
		storyId = storyId + 1
		print("STORY ID ",storyId)
		#new_world(storyId)
		endstory = False
		endstorygen = False
	
	elif endstory and endstorygen and startconvo:
		output_reply = 'Goodbye!'
		startconvo = False
	
	elif startconvo:
		extract_info(focus)
		retrieved = retrieve_output(focus, storyId)
		
		if retrieved.type_num == MOVE_HINT:
			extract_info(retrieved.get_string_response())
		
		output_reply = retrieved.get_string_response()
	
	resp = make_response(jsonify({'name': 'Orsen', 'text': output_reply}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.headers['Access-Control-Allow-Methods:'] =  'GET, POST, PATCH, PUT, DELETE, OPTIONS'
	resp.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
	
	return resp
	

if __name__ == '__main__':
    app.run(debug = True)