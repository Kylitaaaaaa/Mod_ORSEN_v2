from src.models import World, Attribute
from src.models.elements import Character, Object
from src.textunderstanding import InputDecoder, EizenExtractor
from src.dataprocessor import Annotator
from src.models.events import CreationEvent, ActionEvent, DescriptionEvent
from src.constants import *

def extract(story, world):
    extractor = EizenExtractor()
    print(doc[2])
    print("TYPE: ", extractor.check_token(doc[2]))
    print(extractor.is_action_verb(doc[2]))

    event_entities, sentence_references = extractor.parse_user_input(story, world)

    for event_entity, sentence in zip(event_entities, sentence_references):
        sequence_no = len(world.event_chains)
        print("==============================")
        print("EVENT #: %d" % (sequence_no))
        print("==============================")
        print("ET     : %s" % event_entity)
        print("SR     : %s" % sentence)

        event = None

        event_type = event_entity[0]
        event_entity = event_entity[1:]

        if event_type == EVENT_CREATION:
            print(event_entity)
            new_char = Character.create_character(sentence=sentence, token=event_entity[SUBJECT])
            new_char.mention_count += 1

            event = CreationEvent(len(world.event_chains),
                                  subject=new_char)
            world.add_character(new_char)

        elif event_type == EVENT_ACTION:
            print("Finding actor object with name %s" % (event_entity[ACTOR].text))
            actor = world.get_character(event_entity[ACTOR].text)
            if actor == None:
                print("START CREATION FROM EVENT_ACTION")
                print(event_entity[ACTOR])
                print(type(event_entity[ACTOR]))
                actor = Character.create_character(sentence=sentence, token=event_entity[ACTOR])
                print("FINISH CREATION FROM EVENT_ACTION")

            actor.mention_count += 1

            print("Actor  :", actor)
            event = ActionEvent(len(world.event_chains),
                                subject=actor,
                                verb=event_entity[ACTION],
                                direct_object=event_entity[DIRECT_OBJECT],
                                adverb=event_entity[ADVERB],
                                preposition=event_entity[PREPOSITION],
                                object_of_preposition=event_entity[OBJ_PREPOSITION])

        elif event_type == EVENT_DESCRIPTION:
            relation_entity = event_entity[0]
            print(relation_entity)
            attribute_entity = Attribute.create_from_relation(relation_entity)

            print("Finding actor object with name %s" % (relation_entity.first_token))
            actor = world.get_character(relation_entity.first_token.text)
            if actor == None:
                print("START CREATION FROM EVENT_ACTION")
                print(event_entity[ACTOR])
                print(type(event_entity[ACTOR]))
                actor = Character.create_character(sentence=sentence, token=relation_entity.first_token)
                print("FINISH CREATION FROM EVENT_ACTION")

            event = DescriptionEvent(len(world.event_chains),
                                     subject=actor,
                                     attributes=attribute_entity)
        world.add_event(event, sentence)

    for sentence in world.sentence_references:
        print(sentence)

    print("This is now the world:")
    for i in range(len(world.event_chains)):
        event = world.event_chains[i]

        print("EVENT %d: " % (i))
        print(event)

def display_tokens(doc):
    extractor = EizenExtractor()
    for sent in doc.sents:
        extractor.display_tokens(sent)


# story = "Once upon a time, there was a boy named Mario."
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
# story = "Winfred feels like giving Tyler a chance."
# story = "She can swim."
# story = "She is swimming."
# story = "Eric, the prince, was handsome, and kind"
# story = "The book was thrown by Mark."
story = "Once upon a time, there was a boy named John. John, the ruler of the seas, is angry. John kicked a ball."

annotator = Annotator()
annotator.annotate(story)

doc = annotator.get_annotated()
world = World()

extract(story, world)
# display_tokens(doc)
