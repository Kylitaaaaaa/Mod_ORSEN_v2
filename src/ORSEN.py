from src.dataprocessor import Annotator
from src.models import World, Attribute
from src.models.elements import Object, Character
from src.textunderstanding import InputDecoder, EizenExtractor
from src.constants import *
from . import Logger
from src.textunderstanding.InputDecoder import InputDecoder
from src.dialoguemanager import *
from src.models.events import *


class ORSEN:

    def __init__(self):
        super().__init__()

        self.annotator = Annotator()
        self.extractor = EizenExtractor()

        self.dialogue_planner = DialoguePlanner()
        self.content_determination = ContentDetermination()

        self.world = World()
        self.turn_count = 1
        self.prereqs = []
        self.prereqs_pointer = [0, 0]

    def add_prereq(self, prereq):
        self.prereqs.append(prereq)

    def is_done_with_prereqs(self):
        return True

    def execute_text_understanding(self, input):
        result = InputDecoder.annotate_input(input)
        print("Printing result")
        print(result)

    def talk(self):
        if self.is_done_with_prereqs() == False:
            pass
            # TODO implement the modularization of pre-required dialogues
            # WHAT I'M THINKING IS GAWIN NATIN NA PARANG CLASS UGN MGA SHIT NA NILALAGAY BEFORE THE ACTUAL STORYTELLING THING
            # prereq_dialogue = self.prereqs[0]
            # prereq_dialogue.talk(prereq_dialogue[0])

        if self.is_story_done:
            pass
        else:
            result = None

    def is_end_story(self, response):
        if response == 'the end':
            return True
        return False

    def get_response(self, response):


        """"
        Executes text understanding part. This includes the extraction of important information in the text input 
        (using previous sentences as context). This also including breaking the sentences into different event entities.  
        """""
        ORSEN.perform_text_understanding(self, response)

        """" 
        Executing Dialogue Manager 
        """""
        ORSEN.perform_dialogue_manager(self, response)

        # if self.endstory:
        #     if (not self.endstorygen):
        #         if response.lower() in IS_AFFIRM:
        #             pass
        #         else:
        #             pass
        #     elif self.endstorygen:
        #         if response.lower() in IS_AFFIRM:
        #             pass
        #         else:
        #             pass
        # elif response.lower() in IS_END:
        #     pass
        # else:
        #     pass

    def perform_text_understanding(self, response):
        story = response

        # self.world = InputDecoder.get_instance().perform_input_decoding(response, self.world)

        self.annotator.annotate(story)

        event_entities, sentence_references = self.extractor.parse_user_input(story, self.world)

        for event_entity, sentence in zip(event_entities, sentence_references):
            sequence_no = len(self.world.event_chains)
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

                event = CreationEvent(len(self.world.event_chains),
                                      subject=new_char)
                self.world.add_character(new_char)

            elif event_type == EVENT_ACTION:
                print("Finding actor object with name %s" % (event_entity[ACTOR].text))
                actor = self.world.get_character(event_entity[ACTOR].text)
                if actor == None:
                    print("START CREATION FROM EVENT_ACTION")
                    print(event_entity[ACTOR])
                    print(type(event_entity[ACTOR]))
                    actor = Character.create_character(sentence=sentence, token=event_entity[ACTOR])
                    print("FINISH CREATION FROM EVENT_ACTION")

                actor.mention_count += 1

                print("Actor  :", actor)
                event = ActionEvent(len(self.world.event_chains),
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
                actor = self.world.get_character(relation_entity.first_token.text)
                if actor == None:
                    print("START CREATION FROM EVENT_ACTION")
                    print(event_entity[ACTOR])
                    print(type(event_entity[ACTOR]))
                    actor = Character.create_character(sentence=sentence, token=relation_entity.first_token)
                    print("FINISH CREATION FROM EVENT_ACTION")

                event = DescriptionEvent(len(self.world.event_chains),
                                         subject=actor,
                                         attributes=attribute_entity)

            self.world.add_event(event, sentence)

    def perform_dialogue_manager(self, response):

        # curr_event = None
        curr_event = self.world.curr_event

        # choose dialogue move
        move_to_execute = self.dialogue_planner.perform_dialogue_planner()

        # time to choose the template to be used
        # self.world.objects.append(Object(name="ball"))
        # self.world.objects.append(Object(name="ball"))
        # self.world.add_character(Character(name="Winfred"))
        # print("BALL TYPE: ", type("ball"))
        # print("WINFRED TYPE: ", type("Winfred"))

        # send current event to ContentDetermination
        move_to_execute = 'specific' # TODO Delete this after finishing the testing of this particular dialogue move.
        self.content_determination.set_state(move_to_execute, curr_event)
        self.content_determination.perform_content_determination()

        return None
