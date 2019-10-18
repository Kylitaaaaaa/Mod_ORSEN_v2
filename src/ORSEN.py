from src.dataprocessor import Annotator
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

        self.dialogue_planner = DialoguePlanner()
        self.content_determination = ContentDetermination()
        self.initialize_story_prerequisites()

        ###EDEN
        self.occ_manager = OCCManager()
        self.is_end = False

    def initialize_story_prerequisites(self):
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

    def get_response(self, response, triggered_move = None):
        print("TRIGGERED MOVE:  ", triggered_move)
        Logger.log_dialogue_model(response)
        Logger.log_dialogue_model("Entering ORSEN.get_response()")

        """"
        Check for trigger phrases 
        """""

        if triggered_move is not None:
            result = ORSEN.perform_dialogue_manager(self, triggered_move)
        else:
            if self.world.\
                    curr_emotion_event is None:
                triggered_move = self.dialogue_planner.check_trigger_phrases(response, self.world.event_chains, self.world.curr_event)
            else:
                triggered_move = self.dialogue_planner.check_trigger_phrases(response, self.world.event_chains,
                                                                             self.world.curr_emotion_event)

            if triggered_move is None:
                print("NO MOVE TRIGGERED")
                #if not pump
                """"
                Executes text understanding part. This includes the extraction of important information in the text input 
                (using previous sentences as context). This also including breaking the sentences into different event entities.  
                """""
                ORSEN.perform_text_understanding(self, response)

                curr_emotion_event = self.get_emotion(response)
                result = None
                if curr_emotion_event is not None:
                    self.world.add_emotion_event(curr_emotion_event)
                    result = ORSEN.perform_dialogue_manager(self, DIALOGUE_TYPE_E_LABEL)

                if result is None:
                    """" 
                    Executing Dialogue Manager 
                    """""
                    result = ORSEN.perform_dialogue_manager(self)

            else:
                print("TRIGGERED MOVE IS: ", triggered_move)
                """EDEN"""
                if triggered_move in [DIALOGUE_TYPE_C_PUMPING, DIALOGUE_TYPE_D_PRAISE, DIALOGUE_TYPE_D_CORRECTING, DIALOGUE_TYPE_EVALUATION, DIALOGUE_TYPE_RECOLLECTION]:
                    ORSEN.perform_text_understanding(self, response)
                    result = ORSEN.perform_dialogue_manager(self, triggered_move)
                    if triggered_move == DIALOGUE_TYPE_D_PRAISE:
                        print("TRIGGERED D-PRAISE")
                        temp_eval = ORSEN.perform_dialogue_manager(self, DIALOGUE_TYPE_EVALUATION)
                        print("HERE'S TEMPORARY EVALUATION TEMPLATE")
                        print(temp_eval)
                        result = result + temp_eval
                        print(result)
                        print("DONE PRINTING TRIGERRED D-PRAISE + EVAL")
                    elif triggered_move == DIALOGUE_TYPE_RECOLLECTION:
                        temp_end = ORSEN.perform_dialogue_manager(self, DIALOGUE_TYPE_E_END)
                        result = result + temp_end
                        self.is_end = True
                else:
                    result = ORSEN.perform_dialogue_manager(self, triggered_move)



                # """ORSEN 2"""
                # elif triggered_move == DIALOGUE_TYPE_SUGGESTING_AFFIRM:
                #     #add score then general pumping
                #     last_dialogue = self.dialogue_planner.get_last_dialogue_move()
                #     if last_dialogue is not None:
                #         for X in last_dialogue.word_relation:
                #             self.extractor.add_relation_to_concepts_if_not_existing(X)
                #     triggered_move = DIALOGUE_TYPE_PUMPING_GENERAL
                #     pass
                # elif triggered_move == DIALOGUE_TYPE_FOLLOW_UP:
                #     # Why dont u like it or is it wrong -- called from database
                #     pass
                # elif triggered_move == DIALOGUE_TYPE_FOLLOW_UP_DONT_LIKE:
                #     triggered_move = DIALOGUE_TYPE_PUMPING_GENERAL
                # elif triggered_move == DIALOGUE_TYPE_FOLLOW_UP_WRONG:
                #     #deduct score then general pumping
                #     last_dialogue = self.dialogue_planner.get_last_dialogue_move()
                #     if last_dialogue is not None:
                #         for X in last_dialogue.word_relation:
                #             self.extractor.remove_relation_to_concepts_if_not_valid(X)
                #     triggered_move = DIALOGUE_TYPE_PUMPING_GENERAL
                # elif triggered_move == DIALOGUE_TYPE_PUMPING_SPECIFIC:
                #     self.world.curr_event = self.world.event_chains[len(self.world.event_chains)-1]

                #if prompt
                # result = ORSEN.perform_dialogue_manager(self, triggered_move)

        self.dialogue_planner.reset_state()

        return result


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
        self.world.last_fetched = current_event_list

        for i in range(len(current_setting_list)):
            self.world.add_setting(setting)

    def perform_dialogue_manager(self, move_to_execute=""):
        print("**********CURR EMOTION EVENT")
        print(self.world.curr_emotion_event)
        print("AT DIALOGUE MANAGER 1: ", move_to_execute)
        # curr_event = None
        if self.world.curr_emotion_event is not None:
            curr_event = self.world.curr_emotion_event
        else:
            curr_event = self.world.curr_event

        self.dialogue_planner.set_state(curr_event, self.world.get_num_action_events())

        # move_to_execute == DIALOGUE_TYPE_HINTING #TODO remove if done
        if move_to_execute == "":
            move_to_execute = self.dialogue_planner.perform_dialogue_planner()
        else:
            print("AT DIALOGUE MANAGER 2: ", move_to_execute)
            self.dialogue_planner.perform_dialogue_planner(move_to_execute)

        available_templates = self.dialogue_planner.chosen_dialogue_template

        # send current event to ContentDetermination
        self.content_determination.set_state(move_to_execute, curr_event, available_templates)
        response, chosen_template = self.content_determination.perform_content_determination()

        #setting template details
        print("CHOSEN TEMPLATE: ", type(chosen_template))
        print(chosen_template)

        if move_to_execute == DIALOGUE_TYPE_RECOLLECTION:
            print("EVENTS before: ")
            print(self.world.curr_emotion_event)

            emotion_story = self.repeat_emotion_story()
            if emotion_story == "":
                response = ""
            else:
                response = response + \
                           "\n" + emotion_story

                print("EVENTS after: ")
                print(self.world.curr_emotion_event)
            # self.world.curr_emotion_event = None

        self.dialogue_planner.set_template_details_history(chosen_template)


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

    def repeat_emotion_story(self):
        if self.world.curr_emotion_event is None:
            return ""

        # self.world.curr_emotion_event.sequence_number
        response = ""
        print("SEQUENCE NUMBER: ", self.world.curr_emotion_event.sequence_number)
        print("WORLD EVENTS: ", len(self.world.event_chains))
        for i in range (self.world.curr_emotion_event.sequence_number-1, len(self.world.event_chains)):
        # for event in self.world.event_chains:
            event = self.world.event_chains[i]
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


    def get_emotion(self, response):
        Logger.log_occ_values("CHECKING: " + response)
        #returns only the first emotion detected
        emotions_found = []
        for i in range(0, len(self.world.last_fetched)):
            curr_event = self.world.last_fetched[i]
            if curr_event.type == EVENT_ACTION:
                temp_emotion = self.occ_manager.get_occ_emotion(curr_event, response)
                emotions_found.append(temp_emotion)
            else:
                Logger.log_occ_values("NO EMOTION FOUND")

        # for i in range(0, len(emotions_found)):
        #     emotion = emotions_found[i]
        #     Logger.log_occ_values("EVALUATING: " )
        #     if emotion is None:
        #         Logger.log_occ_values("NO EMOTION FOUND")
        #     else:
        #         emotion.print_occ_values()

        #remove none
        emotions_found = list(filter(None, emotions_found))
        if len(emotions_found) != 0:
            Logger.log_occ_values("FINAL EMOTION FOR RESPONSE: " + emotions_found[len(emotions_found)-1].emotion)
            return emotions_found[len(emotions_found)-1]

        Logger.log_occ_values("NO EMOTION FOUND FOR RESPONSE")
        return None

    def is_end_story(self, response):
        if self.is_end:
            print("IS END IS TRUE")
            return True
        if response.lower() in IS_END:
            print("RESPONSE FOR IS END IS TRUE")
            return True
        return False
