data = {}

def response(orsen_response):
    data = \
		{"conversationToken":"{\"state\":null,\"data\":{}}",
		"expectUserResponse":True,
		"expectedInputs":[{
			"inputPrompt":{
				"initialPrompts":[{
					"textToSpeech":""+orsen_response+""}]},
			"possibleIntents":[{
				"intent":"actions.intent.TEXT"}]}]
		}
    
    return data

def final_response(orsen_response):
    data = \
        {"expectUserResponse": False, 
        "finalResponse": {
            "speechResponse": {
                "textToSpeech": ""+orsen_response+""
                }
            }
        }
    
    return data