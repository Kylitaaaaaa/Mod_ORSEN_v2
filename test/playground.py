from src.models import World
from src.textunderstanding import InputDecoder, EizenExtractor
from src.dataprocessor import Annotator
from src.models.events import CreationEvent, ActionEvent, DescriptionEvent
from src.constants import *

annotator = Annotator()
story = "Once upon a time, there was a boy named Mario."
# story= "Hansel chopped the garlic, Mary killed the bees and flew to the moon, and Susan fried the onions and peeled the potatoes."
# story= "Pepper is barking at the delivery man angrily."
# story= "The delivery man was hastily approached by the young man."
# story= "Pepper is angrily barking at the delivery man"
# story= "Phillip sings rather enormously too loudly."
# story= angrily barking at the delivery man."
# story="Hansel quickly fetched the email in front of the house."
# story="The boy gave Kim a rose"
# story="The cake was baked by Matt."
# story = "John went to school."
# story = "Once upon a time, there was a boy."
annotator.annotate(story)

doc = annotator.get_annotated()

for sent in doc.sents:
    InputDecoder.get_instance().display_tokens(sent)


extractor = EizenExtractor()


world = World()
event_entities = extractor.parse_user_input(story, world)


for event_entity in event_entities:
    sequence_no = len(world.event_chains)
    print(event_entity)

    event = None
    if event_entity[0] == EVENT_ACTION:
        event = ActionEvent(len(world.event_chains),
                            subject=event[ACTOR],
                            verb=event[ACTION],
                            direct_object=event[DIRECT_OBJECT],
                            adverb=event[ADVERB],
                            preposition=event[PREPOSITION],
                            object_of_preposition=event[OBJ_PREPOSITION])

    elif event_entity[0] == EVENT_CREATION:
        event = CreationEvent(len(world.event_chains),
                              event[SUBJECT])
    elif event_entity[0] == EVENT_DESCRIPTION:
        pass


for sentence in world.sentence_references:
    print(sentence)

