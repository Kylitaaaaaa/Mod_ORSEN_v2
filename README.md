# Modularized Orsen 1.0

Recent Innovative practices in man-machine interaction can be achieved through intelligent conversations in the form of stories and storytelling between the human users and the conversational agent. The goal is for the agent to provide the necessary support needed to enable the human user, in this case, young learners or children, to construct a story. A combination of text understanding and text generation approaches will be applied. Text understanding involves identifying and extracting relevant information from the story that has been exchanged in the conversation thus far, and subsequently building an abstract representation to allow the conversational agent to track the story elements (characters, setting, events, objects). This representation is then used during text generation to enable the agent to converse intelligently with the human user, either through prompting the user to further elicit details regarding story events, or providing appropriate responses that align with the topic of the conversation. A set of domain knowledge about everyday things that people talk about, and linguistics knowledge to provide appropriate feedback and responses will also be included.

## Current Agendas
- [x] ```Relation``` and ```Concept``` utilization on level similar to previous level 
- [ ] ```Relation``` and ```Concept``` utilization dependent on extracted event type from input and expected event type for output (```Suggesting```)
- [x] ```EventExtractor``` using a different approach based on ```EVENT_TYPE```
- [x] Basic ```DialoguePlanner```
- [ ] Follow-up ```DialoguePlanner```
- [ ] ```LinguisticRealization```



## Testing
Things below are stuff that we still need to test.

#### Test case 1: 
**Wrong inference of event types in the start.** Since extraction of event hardly relies on event type inference, this immediately causes errors.

	e.g. Winfred scored a goal  
	    Expected: EVENT_ACTION
		Actual  : Sometimes EVENT_CREATION, other times EVENT_ACTION

#### Test case 2: 
**No captured events in most recent user input.** This _might_ cause an error since ```curr_event``` entity inside the world will most likely be empty.
	
### Test case 3: 
**Unlucky RNG.** What happens if I get one template in a row more than three times? What happens if the fallback dialogue template is used three time?
	
#### Test case 4:
**Input with a lot of typos.** Should a threshold checking how many typos (as in, words with wrong spelling) should be present at most?
	
#### Test case 5:
**Action events with negation modifiers**. They didn't take note of negated events (as in, only the verb is being recorded without context if it is negative or not)
