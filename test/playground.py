from src.models import World
from src.models.elements import Character, Object, Attribute, Setting
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

    current_event_list = []
    current_sentence_list = []

    prev_sentence = "<START>"
    curr_sentence = ""


    for event_entity, sentence in zip(event_entities, sentence_references):
        if prev_sentence == "<START>":
            prev_sentence = ""
            curr_sentence = sentence.text
        else:
            prev_sentence = curr_sentence
            curr_sentence = sentence.text

        sequence_no = len(world.event_chains)
        print("==============================")
        print("EVENT #: %d" % (sequence_no))
        print("==============================")
        print("ET     : %s" % event_entity)
        print("SR     : %s" % sentence)

        print(prev_sentence + " vs " + curr_sentence)
        if prev_sentence != curr_sentence:
            # print("CHECKING FOR SETTINGS")
            for ent in sentence.ents:
                setting = None
                if ent.label_ == 'TIME':
                    setting = Setting(type=SETTING_TIME, value=ent.text)
                elif ent.label_ == 'DATE':
                    setting = Setting(type=SETTING_DATE, value=ent.text)
                elif ent.label_ in ['PLACE', 'GPE', 'LOC', 'FAC']:
                    setting = Setting(type=SETTING_PLACE, value=ent.text)

                if setting is not None:
                    world.add_setting(setting)


        event = None

        event_type = event_entity[0]
        event_entity = event_entity[1:]

        if event_type == EVENT_CREATION:


            # Create an object corresponded by this event (NOT CHARACTER)
            new_char = Object.create_object(sentence=sentence, token=event_entity[SUBJECT])
            new_char.mention_count += 1

            # Create the creation event and add the new character to the world
            event = CreationEvent(len(world.event_chains), subject=new_char)
            world.add_character(new_char)


        elif event_type == EVENT_DESCRIPTION:


            # Get the whole relation entity object passed from the extractor
            relation_entity = event_entity[0]
            print(relation_entity)

            # Convert the relation entity into an attribute entity. Attributes can be used to describe any given object/character
            attribute_entity = Attribute.create_from_relation(relation_entity)

            # Find the object/entity that will be described. Object may or may not be a character.
            # If not yet existing, create an instance of the object, and add it to the world.
            subject = world.get_character(relation_entity.first_token.text)
            if subject == None:
                subject = world.get_object(event_entity[ACTOR].text)
                if subject == None:
                    subject = Object.create_object(sentence=sentence, token=relation_entity.first_token)
                    subject.mention_count += 1
                    world.add_object(subject)

            # Create the description event
            event = DescriptionEvent(len(world.event_chains), subject=subject, attributes=attribute_entity)


        elif event_type == EVENT_ACTION:


            # Find the actor in the world characters.
            # If existing as an object, convert the object into a character.
            # If not existing anywhere, create it as a new CHARACTER (not an object)
            actor = world.get_character(event_entity[ACTOR].text)
            if actor == None:
                actor = world.get_object(event_entity[ACTOR].text)
                if actor == None:
                    actor = Character.create_character(sentence=sentence, token=event_entity[ACTOR])
                    world.add_character(actor)
                else:
                    actor = Character.create_character(world.remove_object(actor))
                    world.add_character(actor)
            actor.mention_count += 1

            # Almost the same as the one above, except this is for the direct objects and not for the actors
            direct_object = None
            if event_entity[DIRECT_OBJECT] is not None:
                direct_object = world.get_character(event_entity[DIRECT_OBJECT].text)
                if direct_object == None:
                    direct_object = world.get_object(event_entity[DIRECT_OBJECT].text)
                    if direct_object == None:
                        direct_object = Object.create_object(sentence=sentence, token=event_entity[DIRECT_OBJECT])
                        world.add_object(direct_object)
                    else:
                        direct_object = Object.create_object(world.remove_object(direct_object))
                        world.add_object(direct_object)
                direct_object.mention_count += 1

            print("Actor  :", actor)
            event = ActionEvent(len(world.event_chains),
                                subject=actor,
                                verb=event_entity[ACTION],
                                direct_object=direct_object,
                                adverb=event_entity[ADVERB],
                                preposition=event_entity[PREPOSITION],
                                object_of_preposition=event_entity[OBJ_PREPOSITION])


        current_event_list.append(event)
        current_sentence_list.append(sentence)
        # world.add_event(event, sentence)




    for i in range(len(current_event_list)):
        world.add_event(current_event_list[i], current_sentence_list[i])

    print()
    print()
    print("#############################")
    print("# Current world events ######")
    print("#############################")

    for i in range(len(world.event_chains)):
        event = world.event_chains[i]
        print(str(event))
        # print(event.subject.name)
        # for t in event.subject.type:
        #     print(">>:", t)

    print()
    print("#############################")
    print("CURRENT CHARACTERS:")
    for i in range(len(world.characters)):
        character = world.characters[i]
        print(str(character))

    print()
    print("#############################")
    print("CURRENT OBJECTS:")
    for i in range(len(world.objects)):
        object = world.objects[i]
        print(str(object))

    print()
    print("#############################")
    print("CURRENT SETTINGS:")
    for i in range(len(world.settings)):
        setting = world.settings[i]
        print(str(setting))


def display_tokens(doc):
    extractor = EizenExtractor()
    for sent in doc.sents:
        extractor.display_tokens(sent)


# story = "Once upon a time, there was a boy named Mario."
# story= "Hansel chopped the garlic, Mary killed the bees and flew to the moon, and Susan fried the onions and peeled the potatoes."
# story= "Pepper is barking at the delivery man angrily."
# story= " delivery man was hastily approached by the young man."
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
# story = "Once upon a time, there was a boy named John. John, the ruler of the seas, is angry. John angrily kicked a ball."
# story = "The sweet girl is happy."
# story = "happy is the sweet girl."
# story = "Mark is a knight."
# story = "My mother's name is Sasha. My mother likes dogs."
# story = "I will go there at 5pm."
story = "Today I don't feel like doing anything in the Philippines"

annotator = Annotator()
annotator.annotate(story)

doc = annotator.get_annotated()
world = World()

extract(story, world)
# display_tokens(doc)
