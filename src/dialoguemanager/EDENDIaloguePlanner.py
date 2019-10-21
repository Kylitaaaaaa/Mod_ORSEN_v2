from EDEN.OCC import OCCManager
from EDEN.constants import *
from src import *
from src.dialoguemanager import DialoguePlanner
from src.models.dialogue.constants import DIALOGUE_LIST, DialogueHistoryTemplate, EDEN_DIALOGUE_LIST

class EDENDialoguePlanner(DialoguePlanner):

    def __init__(self):
        super().__init__()
        self.occ_manager = OCCManager()
        self.ongoing_c_pumping = False

    def perform_dialogue_planner(self, dialogue_move=""):
        #still no triggered phrase
        if dialogue_move == "":
            print("I DONT HAVE A DIALOGUE")
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
            print("PUTANGINA Chosen dialogue index: " + DIALOGUE_LIST[self.chosen_move_index].get_type())
            self.chosen_dialogue_move = DIALOGUE_LIST[self.chosen_move_index].get_type()

            # choose dialogue template to be used
            self.chosen_dialogue_template = self.usable_templates[self.chosen_move_index]

        else:
            print("I HAVE A DIALOGUE: ", dialogue_move)
            # self.setup_templates_is_usable(dialogue_move)
            self.chosen_dialogue_move = dialogue_move
            self.chosen_dialogue_template = self.get_usable_templates(dialogue_move)

        #add chosen dialogue move to history
        self.dialogue_history.append(DialogueHistoryTemplate(dialogue_type=self.chosen_dialogue_move))
        print("FINAL DIALOGUE LIST: ", self.chosen_dialogue_move)
        self.print_dialogue_list()
        return self.chosen_dialogue_move

    def check_auto_response(self):
        next_move = ""
        next_move = self.check_trigger_phrases()
        if next_move == "":
            next_move = self.check_affirm_deny()
        print("NEXT MOVE SHOULD BE: ", next_move)
        return next_move

    ###checks only dialogue that does not need to go through text understanding
    def check_trigger_phrases(self, event_chain =[]):
        if self.response in IS_END:
            return DIALOGUE_TYPE_E_END
        return ""

    def check_affirm_deny(self):
        # check if last dialogue move has yes or no:
        print("CHECKING AFFIRM DENY")
        last_move = self.get_last_dialogue_move()
        second_to_last_move = self.get_second_to_last_dialogue_move
        if last_move is not None:
            if last_move.dialogue_type == DIALOGUE_TYPE_E_LABEL:
                if self.response in IS_AFFIRM:
                    self.ongoing_c_pumping = True
                    return DIALOGUE_TYPE_C_PUMPING
                else:
                    return DIALOGUE_TYPE_E_PUMPING
            elif last_move.dialogue_type == DIALOGUE_TYPE_D_CORRECTING:
                if self.response in IS_AFFIRM:
                    return DIALOGUE_TYPE_EVALUATION
                else:
                    return DIALOGUE_TYPE_D_PUMPING
            elif self.ongoing_c_pumping and self.response.lower() in IS_DONE_EXPLAINING:
                self.ongoing_c_pumping = False
                print("DONE EXPLANING")
                print(self.curr_event.emotion)
                if self.curr_event.emotion is not None:
                    # check if emotion should be disciplined
                    if self.curr_event.emotion in DISCIPLINARY_EMOTIONS:
                        return DIALOGUE_TYPE_D_CORRECTING
                    else:
                        # check if emotion is + or -
                        if self.curr_event.emotion in POSITIVE_EMOTIONS:
                            return DIALOGUE_TYPE_D_PRAISE
                        else:
                            return DIALOGUE_TYPE_EVALUATION
        return ""

    def check_based_prev_move(self, curr_event=None, curr_emotion_event=None):
        last_move = self.get_last_dialogue_move()

        if last_move is not None:
            print("LAST MOVE IS: ", last_move.dialogue_type)
            if self.ongoing_c_pumping:
                print("currently ongoing c pumping: ", self.response.lower())
                print(IS_DONE_EXPLAINING)

                if curr_event is not None and curr_emotion_event is not None and curr_event.type == EVENT_EMOTION and curr_event.emotion == curr_emotion_event.emotion:
                    print("triggering e emphasis")
                    return DIALOGUE_TYPE_E_EMPHASIS
                # elif self.response.lower() in IS_DONE_EXPLAINING:
                #     self.ongoing_c_pumping = False
                #     print("DONE EXPLANING")
                #     print(self.curr_event.emotion)
                #     if self.curr_event.emotion is not None:
                #         # check if emotion should be disciplined
                #         if self.curr_event.emotion in DISCIPLINARY_EMOTIONS:
                #             return DIALOGUE_TYPE_D_CORRECTING
                #         else:
                #             # check if emotion is + or -
                #             if self.curr_event.emotion in POSITIVE_EMOTIONS:
                #                 return DIALOGUE_TYPE_D_PRAISE
                #             else:
                #                 return DIALOGUE_TYPE_EVALUATION
                else:
                    return DIALOGUE_TYPE_PUMPING_GENERAL
            ###START EDEN
            #check if last move is eden
            elif last_move.dialogue_type == DIALOGUE_TYPE_E_PUMPING:
                print("SETTING CURR_EVENT_EMOTION TO: ", self.response.upper())
                self.curr_event.emotion = self.response.upper()
                self.ongoing_c_pumping = True
                return DIALOGUE_TYPE_C_PUMPING
            # elif self.ongoing_c_pumping and (self.response.lower() in IS_DONE_EXPLAINING):
            #     self.ongoing_c_pumping = False
            #     if self.curr_event.emotion is not None:
            #         #check if emotion should be disciplined
            #         if self.curr_event.emotion in DISCIPLINARY_EMOTIONS:
            #             return DIALOGUE_TYPE_D_CORRECTING
            #         else:
            #             # check if emotion is + or -
            #             if self.curr_event.emotion in POSITIVE_EMOTIONS:
            #                 return DIALOGUE_TYPE_D_PRAISE
            #             else:
            #                 return DIALOGUE_TYPE_EVALUATION
            # elif self.ongoing_c_pumping and not (self.response.lower() in IS_DONE_EXPLAINING):
            # # elif last_move.dialogue_type == DIALOGUE_TYPE_C_PUMPING or last_move.dialogue_type == DIALOGUE_TYPE_PUMPING_GENERAL and \
            # #         (not self.ongoing_c_pumping and self.response.lower() in IS_DONE_EXPLAINING):
            #     #check if emotion is repeating -- return emphasis
            #     return DIALOGUE_TYPE_PUMPING_GENERAL


            elif last_move.dialogue_type == DIALOGUE_TYPE_D_PUMPING:
                return DIALOGUE_TYPE_EVALUATION
            elif last_move.dialogue_type == DIALOGUE_TYPE_EVALUATION:
                return DIALOGUE_TYPE_RECOLLECTION

        else:
            print("NO PREVIOUS DIALOGUE")
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
            print("CHECKING EVENT t: ", self.curr_event.type)

            move_to_execute = self.check_based_prev_move()
            print("MOVE SELECTED: ", move_to_execute)

            if move_to_execute != "":
                print("MOVES 1")
                set_to_true.append(move_to_execute)
            else:
                print("MOVES 2")
                print("self.curr_event.type: ", self.curr_event.type)
                print("EVENT_EMOTION: ", EVENT_EMOTION)
                if self.curr_event.type == EVENT_EMOTION:
                    print("Turned elabel to true")
                    set_to_true.append(DIALOGUE_TYPE_E_LABEL)
                else:
                    print("MOVES 3")
                    set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)
        else:
            set_to_true.append(preselected_move)

        print("SETTING STUFF TO TRUE")
        print(set_to_true)
        self.set_dialogue_list_true(set_to_true)

    def get_latest_event(self, last_fetched):
        Logger.log_occ_values("CHECKING: " + self.response)
        # returns only the first emotion detected
        emotions_found = []
        for i in range(0, len(last_fetched)):
            curr_event = last_fetched[i]
            # check if description later
            if curr_event.type == EVENT_ACTION:
                # reset occ values
                self.occ_manager.set_values()
                # get emotion list (str)
                temp_emotion = self.occ_manager.get_occ_emotion(curr_event, self.response)
                if temp_emotion is not None and len(temp_emotion) > 0:
                    for X in temp_emotion:
                        if X.emotion not in emotions_found:
                            emotions_found.append(X)
        #emotion found
        if len(emotions_found) > 0:
            # self.world.add_emotion_event(emotions_found)
            #return latest emotion
            listToStr = ' '.join([str(curr_emotion.emotion) for curr_emotion in emotions_found])
            print("EMOTIONS FOUND 2: " + listToStr)
            Logger.log_occ_values("EMOTIONS FOUND 2: " + listToStr)

            return emotions_found[len(emotions_found)-1]

        #no emotion found
        else:
            if len(last_fetched) > 0:
                return last_fetched[len(last_fetched)-1]
            return None
        # return []

    def is_repeat_story(self, move_to_execute):
        if move_to_execute == DIALOGUE_TYPE_RECOLLECTION:
            return True
        return False

    def finalize_dialogue_move(self, curr_dialogue_move):
        if curr_dialogue_move == DIALOGUE_TYPE_D_PRAISE:
            return DIALOGUE_TYPE_EVALUATION
        elif curr_dialogue_move == DIALOGUE_TYPE_RECOLLECTION:
            return DIALOGUE_TYPE_PUMPING_GENERAL
        # if curr_dialogue_move == DIALOGUE_TYPE_E_END:
        #     return DIALOGUE_TYPE_RECOLLECTION
        return ""

