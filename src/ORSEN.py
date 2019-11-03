import time

from EDEN.constants import EVENT_EMOTION
from EDEN.models import Emotion
from src.dataprocessor import Annotator
from src.dialoguemanager import DialoguePlannerBuilder
from src.models import World
from src.models.elements import Attribute, Setting
from src.models.elements import Object, Character
from src.textunderstanding import InputDecoder, EizenExtractor
from src.constants import *
from . import Logger
from src.textunderstanding.InputDecoder import InputDecoder
from src.dialoguemanager import *
from src.models.events import *
from EDEN.OCC import OCCManager



class ORSEN:

    def __init__(self):
        super().__init__()

        self.annotator = Annotator()
        self.extractor = EizenExtractor()

        # self.dialogue_planner = DialoguePlanner()
        self.dialogue_planner = DialoguePlannerBuilder.build(CURR_ORSEN_VERSION)
        self.content_determination = ContentDetermination()
        self.initialize_story_prerequisites()

        ###EDEN
        self.occ_manager = OCCManager()
        self.is_end = False
        # self.world = None
        self.user_start_time = time.time()
        self.user_end_time = time.time()

    def initialize_story_prerequisites(self):
        # self.world = None
        self.world = World()
        self.turn_count = 1
        self.prereqs = []
        self.prereqs_pointer = [0, 0]
        # self.dialogue_planner.reset_state()
        self.dialogue_planner.dialogue_history = []


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

    def get_response(self, response="", move_to_execute = ""):
        self.user_end_time = time.time()

        Logger.log_conversation("USER LATENCY TIME (seconds): " + str(self.user_end_time - self.user_start_time))

        start_time = time.time()

        print("=====USER RESPONSE IS: " + response)
        if response != "":
            Logger.log_event_response_eval(response)

        orsen_reply = self.perform_dialogue_manager(response, preselected_move=move_to_execute)
        # try:
        #     orsen_reply = self.perform_dialogue_manager(response, preselected_move=move_to_execute)
        # except Exception as e:
        #     Logger.log_conversation("ERROR: " + str(e))
        #     orsen_reply = "I see. What else can you say about that?"

        Logger.log_conversation("ORSEN LATENCY TIME (seconds): " + str(time.time() - start_time))

        self.user_start_time = time.time()
        return orsen_reply


    def perform_text_understanding(self, response):


        story = response

        event_entities, sentence_references = self.extractor.parse_user_input(story, self.world)

        current_event_list = []
        current_sentence_list = []
        current_setting_list = []

        prev_sentence = "<START>"
        curr_sentence = ""

        for event_entity, sentence in zip(event_entities, sentence_references):
            if prev_sentence == "<START>":
                prev_sentence = ""
                curr_sentence = sentence.text
            else:
                prev_sentence = curr_sentence
                curr_sentence = sentence.text

            print("==============================")
            print("== !!EVENT FOUND!! ===========")
            print("==============================")
            print("ET     : %s" % event_entity)
            print("SR     : %s" % sentence)

            settings = []
            # print(prev_sentence + " vs " + curr_sentence)
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
                        print("NEW SETTING:", str(setting))
                        settings.append(setting)

            event = None

            event_type = event_entity[0]
            event_entity = event_entity[1:]

            if event_type == EVENT_CREATION:

                # Create an object corresponded by this event (NOT CHARACTER)
                new_char = Object.create_object(sentence=sentence, token=event_entity[SUBJECT])
                new_char.mention_count += 1

                for s in settings:
                    new_char.add_in_setting(s)

                # Create the creation event and add the new character to the world
                self.world.add_character(new_char)
                event = CreationEvent(len(self.world.event_chains), subject=new_char)
                Logger.log_event(EVENT_CREATION, event.print_basic())


            elif event_type == EVENT_DESCRIPTION:

                # Get the whole relation entity object passed from the extractor
                relation_entity = event_entity[0]
                print(relation_entity)

                # Convert the relation entity into an attribute entity. Attributes can be used to describe any given object/character
                attribute_entity = Attribute.create_from_relation(relation_entity)

                # Find the object/entity that will be described. Object may or may not be a character.
                # If not yet existing, create an instance of the object, and add it to the world.
                subject = self.world.get_character(relation_entity.first_token.text)
                if subject == None:
                    subject = self.world.get_object(relation_entity.first_token.text)
                    if subject == None:
                        subject = Object.create_object(sentence=sentence, token=relation_entity.first_token)
                        self.world.add_object(subject)

                subject.mention_count += 1

                for s in settings:
                    subject.add_in_setting(s)

                # Create the description event
                event = DescriptionEvent(len(self.world.event_chains), subject=subject, attributes=attribute_entity)
                Logger.log_event(EVENT_DESCRIPTION, event.print_basic())


            elif event_type == EVENT_ACTION:

                # Find the actor in the world characters.
                # If existing as an object, convert the object into a character.
                # If not existing anywhere, create it as a new CHARACTER (not an object)
                print("Actor entity is now:", event_entity[ACTOR].text)
                actor = self.world.get_character(event_entity[ACTOR].text)
                print("Actor entity after world.get_character():", str(actor))
                if actor == None:
                    actor = self.world.get_object(event_entity[ACTOR].text)
                    print("Actor entity after world.get_object():", str(actor))
                    if actor == None:
                        print("Actor entity not found. Creating one now via create_character():", str(actor))
                        actor = Character.create_character(sentence=sentence, token=event_entity[ACTOR])
                        self.world.add_character(actor)
                    else:
                        print("Actor entity object found. Remove from objects and add to characters", str(actor))
                        actor = Character.create_character(sentence=sentence, token=self.world.remove_object(actor))
                        self.world.add_character(actor)

                actor.mention_count += 1
                print(str(actor))

                for s in settings:
                    print("ADDING %S IN CHARACTER", str(s))
                    actor.add_in_setting(s)

                # Almost the same as the one above, except this is for the direct objects and not for the actors
                direct_object = None
                if event_entity[DIRECT_OBJECT] is not None:
                    direct_object = self.world.get_character(event_entity[DIRECT_OBJECT].text)
                    if direct_object == None:
                        direct_object = self.world.get_object(event_entity[DIRECT_OBJECT].text)
                        if direct_object == None:
                            direct_object = Object.create_object(sentence=sentence, token=event_entity[DIRECT_OBJECT])
                            self.world.add_object(direct_object)
                    direct_object.mention_count += 1

                    for s in settings:
                        direct_object.add_in_setting(s)

                print("Actor        :", actor)
                print("Direct object:", direct_object)

                event = ActionEvent(len(self.world.event_chains),
                                    subject=actor,
                                    verb=event_entity[ACTION],
                                    direct_object=direct_object,
                                    adverb=event_entity[ADVERB],
                                    preposition=event_entity[PREPOSITION],
                                    object_of_preposition=event_entity[OBJ_PREPOSITION])
                print("PRINTING THE BASIC VERSION OF THE EVENT:")
                print(event.print_basic())
                print("DONE PRINTING")
                Logger.log_event(EVENT_ACTION, event.print_basic())

            current_event_list.append(event)
            current_sentence_list.append(sentence)

            current_setting_list.extend(settings)
            # world.add_event(event, sentence)

        for i in range(len(current_event_list)):
            self.world.add_event(current_event_list[i], current_sentence_list[i])
        print(current_event_list)
        self.world.last_fetched = current_event_list

        for i in range(len(current_setting_list)):
            self.world.add_setting(setting)

    def perform_dialogue_manager(self, response, preselected_move=""):
        curr_event = None
        move_to_execute = ""

        #set response in dialogue planner
        self.dialogue_planner.response = response.lower()
        move_to_execute = ""

        # gets move to execute -- uses passed if not empty, asks dialogue planner to decide otherwise
        #usually used for testing
        if preselected_move != "":
            move_to_execute = preselected_move
            print("----------PRESELECTED: ", move_to_execute)

        elif self.dialogue_planner.check_auto_response(destructive = False, emotion_event = self.world.curr_emotion_event) != "":
            # check if trigger phrases, affirm, deny responses
            move_to_execute = self.dialogue_planner.check_auto_response(emotion_event = self.world.curr_emotion_event)
            print("----------AUTO: ", move_to_execute)

        # regardless if model is done or not, undergo text understanding
        elif self.dialogue_planner.check_based_prev_move(destructive = False) != "":
            self.perform_text_understanding(response)
            move_to_execute = self.dialogue_planner.check_based_prev_move()
            print("----------BASED ON PREV MOVE: ", move_to_execute)

        else:
            self.perform_text_understanding(response)

            print("LAST FETCHED IS: ", len(self.world.last_fetched))
            Logger.log_occ_values_basic(response)
            detected_event = self.dialogue_planner.get_latest_event(self.world.last_fetched)
            if detected_event is not None and detected_event.type == EVENT_EMOTION:
                print("ADDED EMOTION EVENT: ", detected_event.sequence_number)
                self.world.emotion_events.append(detected_event)

            new_move_from_old = self.dialogue_planner.\
                check_based_curr_event(detected_event, self.world.curr_emotion_event)
            print("----------EVENT: ", move_to_execute)

            if new_move_from_old == "":
                #no new move found
                if detected_event is not None and detected_event.type == EVENT_EMOTION and not self.dialogue_planner.ongoing_c_pumping:
                    self.world.curr_emotion_event = detected_event
                    self.dialogue_planner.curr_event = self.world.curr_emotion_event

                    move_to_execute = DIALOGUE_TYPE_E_LABEL
                else:
                    move_to_execute = ""
                    self.dialogue_planner.curr_event = self.world.curr_event

                print("----------NO MOVE SELECTED: ", move_to_execute)
            else:
                #for emphasis
                self.dialogue_planner.curr_event = self.world.curr_emotion_event

                move_to_execute = new_move_from_old

        self.dialogue_planner.perform_dialogue_planner(move_to_execute)
        #fetches templates of chosen dialogue move
        available_templates = self.dialogue_planner.chosen_dialogue_template

        # send current event to ContentDetermination
        self.content_determination.set_state(move_to_execute, self.dialogue_planner.curr_event, available_templates)
        response, chosen_template = self.content_determination.perform_content_determination()



        """FINALIZE MOVES"""

        #check if other dialogue moves should be appended
        #is it necessary to repeat the story
        if self.dialogue_planner.is_repeat_story(move_to_execute):
            emotion_story = self.content_determination.repeat_emotion_story(self.world.curr_emotion_event, self.world.event_chains)
            if emotion_story == "":
                response = ""
            else:
                response = response + \
                           "\n" + emotion_story

        if self.dialogue_planner.get_second_to_last_dialogue_move() is not None and \
                self.dialogue_planner.get_second_to_last_dialogue_move().dialogue_type == DIALOGUE_TYPE_E_FOLLOWUP:
            response = "Thank you for clarifying that. " + response
        #update event chain with new emotion
        if move_to_execute == DIALOGUE_TYPE_C_PUMPING:
            self.world.curr_emotion_event.emotion = self.dialogue_planner.curr_event.emotion
            self.world.emotion_events[len(self.world.emotion_events)-1] = self.world.curr_emotion_event

        #saves dialogue move to history
        self.dialogue_planner.set_template_details_history(chosen_template)

        followup_move = self.dialogue_planner.finalize_dialogue_move(move_to_execute)
        if followup_move != "":
            response = response + self.perform_dialogue_manager(response="", preselected_move=followup_move)

        self.dialogue_planner.reset_state()


        return response

    def is_end_story(self, response):
        # if self.is_end or \
        #         response.lower() in IS_END or \
        #         (self.dialogue_planner.get_last_dialogue_move() is not None and self.dialogue_planner.get_last_dialogue_move().dialogue_type == DIALOGUE_TYPE_E_END):
        #     return True

        if self.is_end or \
                (self.dialogue_planner.get_last_dialogue_move() is not None and self.dialogue_planner.get_last_dialogue_move().dialogue_type == DIALOGUE_TYPE_E_END):
            return True

        return False
