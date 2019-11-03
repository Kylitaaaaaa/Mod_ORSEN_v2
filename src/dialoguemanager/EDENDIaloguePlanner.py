from EDEN.OCC import OCCManager
from EDEN.constants import *
from src import *
from src.dbo.dialogue import DBODialogueTemplate
from src.dialoguemanager import DialoguePlanner
from src.models.dialogue.constants import DIALOGUE_LIST, DialogueHistoryTemplate, EDEN_DIALOGUE_LIST
import time
import numpy as np

class EDENDialoguePlanner(DialoguePlanner):

    def __init__(self):
        super().__init__()
        self.occ_manager = OCCManager()
        self.ongoing_c_pumping = False

    def reset_new_world(self):
        self.chosen_dialogue_move = None
        self.chosen_dialogue_template = []
        self.chosen_move_index = -1
        self.curr_event = None
        self.dialogue_history = []
        self.dialogue_template = DBODialogueTemplate('templates')
        self.frequency_count = np.zeros(len(DIALOGUE_LIST))
        self.is_usable = [False] * len(DIALOGUE_LIST)
        self.move_index = -1
        self.num_action_events = 0
        #occ manager
        self.ongoing_c_pumping = False
        self.response = ""
        self.seed_time = time.time()
        self.usable_templates = []
        np.random.seed(DEFAULT_SEED)
        self.occ_manager.reset_occ()

    def perform_dialogue_planner(self, dialogue_move=""):
        #still no triggered phrase
        if dialogue_move == "":
            self.setup_templates_is_usable()

            Logger.log_dialogue_model_basic("Breakdown of values used:")
            Logger.log_dialogue_model_basic_example(DIALOGUE_LIST)
            Logger.log_dialogue_model_basic_example(self.is_usable)
            Logger.log_dialogue_model_basic_example(self.frequency_count)

            print("Breakdown of values used:")
            self.print_dialogue_list()

            #choose dialogue based on dialogue history
            self.chosen_move_index = self.choose_dialogue()
            Logger.log_dialogue_model_basic("Chosen dialogue index: " + str(self.chosen_move_index))
            self.chosen_dialogue_move = DIALOGUE_LIST[self.chosen_move_index].get_type()

            # choose dialogue template to be used
            self.chosen_dialogue_template = self.usable_templates[self.chosen_move_index]

        else:
            # self.setup_templates_is_usable(dialogue_move)
            self.chosen_dialogue_move = dialogue_move
            self.chosen_dialogue_template = self.get_usable_templates(dialogue_move)

        #add chosen dialogue move to history
        self.dialogue_history.append(DialogueHistoryTemplate(dialogue_type=self.chosen_dialogue_move))
        print("FINAL DIALOGUE LIST: ", self.chosen_dialogue_move)
        self.print_dialogue_list()

        Logger.log_conversation("CHOSEN DIALOGUE MOVE: " + self.chosen_dialogue_move)

        return self.chosen_dialogue_move

    def check_auto_response(self, destructive = True, emotion_event = None):
        next_move = self.check_trigger_phrases()
        if next_move != "":
            return next_move
        else:
            next_move = self.check_affirm_deny(destructive, emotion_event)
        return next_move

    # def choose_dialogue(self):
    #     for i in range(len(DIALOGUE_LIST)):
    #         if DIALOGUE_LIST[i].get_type() == DIALOGUE_TYPE_PUMPING_GENERAL:
    #             return i

    ###checks only dialogue that does not need to go through text understanding
    def check_trigger_phrases(self, event_chain =[]):
        # if self.response in IS_END:
        if self.response in IS_END and not self.ongoing_c_pumping:
            return DIALOGUE_TYPE_E_END
        return ""

    def check_affirm_deny(self, destructive = True, emotion_event = None):
        # check if last dialogue move has yes or no:
        last_move = self.get_last_dialogue_move()
        next_move = ""
        if last_move is not None:
            if last_move.dialogue_type == DIALOGUE_TYPE_E_LABEL:
                if self.response in IS_AFFIRM:
                    self.ongoing_c_pumping = True
                    next_move = DIALOGUE_TYPE_C_PUMPING
                else:
                    next_move = DIALOGUE_TYPE_E_PUMPING
            elif last_move.dialogue_type == DIALOGUE_TYPE_D_CORRECTING:
                if self.response in IS_AFFIRM:
                    next_move = DIALOGUE_TYPE_EVALUATION
                else:
                    next_move = DIALOGUE_TYPE_D_PUMPING
            elif last_move.dialogue_type == DIALOGUE_TYPE_E_PUMPING and self.response.lower() in IS_DONE_EXPLAINING:
                if destructive:
                    self.ongoing_c_pumping = False
                # return DIALOGUE_TYPE_PUMPING_GENERAL
                return DIALOGUE_TYPE_E_FOLLOWUP
            # elif self.ongoing_c_pumping and self.response.lower() in IS_DONE_EXPLAINING:
            elif self.ongoing_c_pumping and self.response.lower() in IS_END:
                if destructive:
                    self.ongoing_c_pumping = False
                if emotion_event is not None:
                # if self.curr_event.emotion is not None:
                    # check if emotion should be disciplined
                    # if self.curr_event.emotion in DISCIPLINARY_EMOTIONS:
                    if emotion_event.emotion in DISCIPLINARY_EMOTIONS:
                        next_move = DIALOGUE_TYPE_D_CORRECTING
                    else:
                        # check if emotion is + or -
                        # if self.curr_event.emotion in POSITIVE_EMOTIONS:
                        if emotion_event.emotion in POSITIVE_EMOTIONS:
                            next_move = DIALOGUE_TYPE_D_PRAISE
                        else:
                            next_move = DIALOGUE_TYPE_EVALUATION
            if next_move !="" and destructive:
                self.curr_event = emotion_event
        return next_move

    def check_based_prev_move(self, destructive = True):
        last_move = self.get_last_dialogue_move()

        if last_move is not None:
            print("LAST MOVE IS: ", last_move.dialogue_type)
            if self.ongoing_c_pumping:
                print("currently ongoing c pumping: ", self.response.lower())
            ###START EDEN
            #check if last move is eden
            elif last_move.dialogue_type == DIALOGUE_TYPE_E_PUMPING:
                if destructive:
                    print("SETTING CURR_EVENT_EMOTION TO: ", self.response.upper())
                    Logger.log_occ_values("UPDATING EMOTION TO: " +  self.response.upper())


                    retrieved_emotion = self.occ_manager.get_emotion_by_synonym(self.response.lower())
                    if retrieved_emotion != "":
                        self.curr_event.emotion = retrieved_emotion
                    else:
                        self.curr_event.emotion = self.response.upper()

                    self.ongoing_c_pumping = True
                return DIALOGUE_TYPE_C_PUMPING
            elif last_move.dialogue_type == DIALOGUE_TYPE_D_PUMPING:
                return DIALOGUE_TYPE_EVALUATION
            elif last_move.dialogue_type == DIALOGUE_TYPE_EVALUATION:
                return DIALOGUE_TYPE_RECOLLECTION
            elif last_move.dialogue_type == DIALOGUE_TYPE_E_FOLLOWUP:
                return DIALOGUE_TYPE_PUMPING_GENERAL

        else:
            print("NO PREVIOUS DIALOGUE")
        return ""

    def check_based_curr_event(self, detected_event=None, curr_event=None):
        if self.ongoing_c_pumping:
            if detected_event is not None and curr_event is not None:
                if detected_event.type == EVENT_EMOTION and detected_event.emotion == curr_event.emotion:
                    return DIALOGUE_TYPE_E_EMPHASIS
                # else:
                #     return DIALOGUE_TYPE_PUMPING_GENERAL
        return ""


    #emotion coaching model
    def is_model_ongoing(self):
        last_move = self.get_last_dialogue_move()
        if last_move is not None:
            if last_move.dialogue_type != EDEN_LAST_MODEL_MOVE\
                    and last_move.dialogue_type != DIALOGUE_TYPE_PUMPING_GENERAL \
                    and not self.ongoing_c_pumping:
                return True
        return False

    def init_set_dialogue_moves_usable(self, preselected_move=""):
        # check which dialogue moves are usable
        set_to_true = []
        if preselected_move =="":
            move_to_execute = self.check_based_prev_move()
            if move_to_execute != "":
                set_to_true.append(move_to_execute)
            else:
                if self.curr_event is not None and self.curr_event.type == EVENT_EMOTION:
                    set_to_true.append(DIALOGUE_TYPE_E_LABEL)
                else:
                    if len(self.get_usable_templates(DIALOGUE_TYPE_PUMPING_SPECIFIC)) > 0:
                        set_to_true.append(DIALOGUE_TYPE_PUMPING_SPECIFIC)
                    set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)
        else:
            set_to_true.append(preselected_move)
        self.set_dialogue_list_true(set_to_true)

    def get_latest_event(self, last_fetched):
        # returns only the first emotion detected
        emotions_found = []
        for i in range(0, len(last_fetched)):
            curr_event = last_fetched[i]

            # reset occ values
            self.occ_manager.set_values()
            # get emotion list (str)
            temp_emotion = self.occ_manager.get_occ_emotion(curr_event, self.response)
            if temp_emotion is not None and len(temp_emotion) > 0:
                for X in temp_emotion:
                    if not self.is_emotion_exist(X.emotion, emotions_found):
                        emotions_found.append(X)


            # # check if description later
            # if curr_event.type == EVENT_ACTION:
            #     # reset occ values
            #     self.occ_manager.set_values()
            #     # get emotion list (str)
            #     temp_emotion = self.occ_manager.get_occ_emotion(curr_event, self.response)
            #     if temp_emotion is not None and len(temp_emotion) > 0:
            #         for X in temp_emotion:
            #             if not self.is_emotion_exist(X.emotion, emotions_found):
            #                 emotions_found.append(X)
        #emotion found
        if len(emotions_found) > 0:
            # self.world.add_emotion_event(emotions_found)
            #return latest emotion
            listToStr = ' '.join([str(curr_emotion.emotion) for curr_emotion in emotions_found])
            Logger.log_occ_values("SIMPLIFIED EMOTIONS: " + listToStr)

            final_emotion = self.occ_manager.get_final_emotion(emotions_found)

            # Logger.log_occ_values("CHOSEN EMOTION: " + emotions_found[len(emotions_found)-1].emotion)
            Logger.log_occ_values("CHOSEN EMOTION: " + final_emotion.emotion)

            # return emotions_found[len(emotions_found)-1]
            return final_emotion

        #no emotion found
        else:
            if len(last_fetched) > 0:
                return last_fetched[len(last_fetched)-1]
        return None
        # return []

    def is_emotion_exist(self, emotion_to_check, emotion_list):
        if len(emotion_list) > 0:
            for curr_emotion in emotion_list:
                if curr_emotion.emotion == emotion_to_check:
                    return True
        return False

    def is_repeat_story(self, move_to_execute):
        if move_to_execute == DIALOGUE_TYPE_RECOLLECTION:
            return True
        return False

    def finalize_dialogue_move(self, curr_dialogue_move):
        if curr_dialogue_move == DIALOGUE_TYPE_D_PRAISE:
            return DIALOGUE_TYPE_EVALUATION
        elif curr_dialogue_move == DIALOGUE_TYPE_RECOLLECTION:
            return DIALOGUE_TYPE_E_END
        return ""

    def get_welcome_message_type(self):
        return DIALOGUE_TYPE_EDEN_WELCOME
