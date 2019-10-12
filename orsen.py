#from src.run import extract_info, new_world
#from src.dialoguemanager.DialoguePlanner import *
from flask import Flask
from flask import jsonify
from flask import request
from flask import json
from src.googlehome import json_reply

#from src.dialoguemanager.story_generation import generate_basic_story, generate_collated_story
#from src.inputprocessor.infoextraction import getCategory, CAT_STORY
#import logging
app = Flask(__name__)


@app.route('/orsen', methods=["POST"])
def orsen():
	print("YOLO")
	#print(json.dumps(request.get_json()))
	requestJson = request.get_json()
	
	focus = requestJson["inputs"][0]#["rawInputs"][0]["query"]
	print(focus["intent"])

	output_reply = "Hi! Let's create a story. You start."

	rawTextQuery = requestJson["inputs"][0]["rawInputs"][0]["query"]
	if focus["intent"] == "actions.intent.TEXT":
		print(rawTextQuery)
		output_reply = "PEW PEW"

	'''data = \
		{"conversationToken":"{\"state\":null,\"data\":{}}",
		"expectUserResponse":True,
		"expectedInputs":[{
			"inputPrompt":{
				"initialPrompts":[{
					"textToSpeech":""+output_reply+""}]},
			"possibleIntents":[{
				"intent":"actions.intent.TEXT"}]}]
		}'''
	
	data = json_reply.response(output_reply)


	if rawTextQuery == "bye":
		output_reply = "Bye Bye~"
		#data = {"expectUserResponse": False, "finalResponse": {"speechResponse": {"textToSpeech": ""+output_reply+""}}}
		data = json_reply.final_response(output_reply)

	return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)