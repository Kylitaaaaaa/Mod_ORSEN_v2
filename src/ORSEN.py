from src.dataprocessor import Annotator
from src.models import World
from src.models.elements import Attribute
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

    def is_engaged(self, response):
        if response.lower() in IS_END:
            return False
        return True

    def get_response(self, response):
        Logger.log_dialogue_model(response)

        """"
        Check for trigger phrases 
        """""
        triggered_move = self.dialogue_planner.check_trigger_phrases(response)
        if triggered_move is None:
            """"
            Executes text understanding part. This includes the extraction of important information in the text input 
            (using previous sentences as context). This also including breaking the sentences into different event entities.  
            """""
            ORSEN.perform_text_understanding(self, response)

            """" 
            Executing Dialogue Manager 
            """""
            Logger.log_dialogue_model("Entering ORSEN.get_response()")
            result = ORSEN.perform_dialogue_manager(self, response)

        else:
            result = ORSEN.perform_dialogue_manager(self, triggered_move)

        self.dialogue_planner.reset_state()

        return result


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

    def perform_dialogue_manager(self, move_to_execute=""):
        # curr_event = None
        curr_event = self.world.curr_event
        self.dialogue_planner.set_event(curr_event)

        if move_to_execute == "":
            move_to_execute = self.dialogue_planner.perform_dialogue_planner()
        else:
            self.dialogue_planner.perform_dialogue_planner(move_to_execute)


        # choose dialogue move

        # # self.dialogue_planner.perform_dialogue_planner()
        # move_to_execute = 'specific'  # TODO Delete this after finishing the testing of this particular dialogue move.
        # self.dialogue_planner.test_perform_dialogue_planner(move_to_execute) # TODO: Delete after testing
        # move_to_execute = self.dialogue_planner.chosen_dialogue_move
        available_templates = self.dialogue_planner.chosen_dialogue_template

        
        # send current event to ContentDetermination
        self.content_determination.set_state(move_to_execute, curr_event, available_templates)
        response = self.content_determination.perform_content_determination()

        return response


    def repeat_story(self):
        response = ""
        for event in self.world.event_chains:
            to_insert = event.subject.name + " "
            if event.get_type() == EVENT_ACTION:
                to_insert = to_insert + str(event.verb)
            elif event.get_type() == EVENT_CREATION:
                to_insert = event.subject.name
            elif event.get_type() == EVENT_DESCRIPTION:
                # Iterate through attributes
                for X in event.attributes:
                    to_insert = to_insert + X.keyword + " " + str(X.description.lemma_)
            to_insert = to_insert + ". "
            response = response + to_insert
        return response


