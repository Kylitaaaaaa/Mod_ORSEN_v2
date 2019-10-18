import random

import numpy as np
import time

from EDEN.constants import EMOTION_TYPE_POSITIVE
from src import Logger, DIALOGUE_TYPE_FEEDBACK, DIALOGUE_TYPE_PUMPING_GENERAL, DIALOGUE_TYPE_HINTING, DEFAULT_SEED, \
    DIALOGUE_TYPE_SUGGESTING, DIALOGUE_TYPE_FOLLOW_UP, IS_AFFIRM, IS_DONT_LIKE, IS_WRONG, \
    DIALOGUE_TYPE_FOLLOW_UP_DONT_LIKE, DIALOGUE_TYPE_FOLLOW_UP_WRONG, IS_DENY, DIALOGUE_TYPE_SUGGESTING_AFFIRM
from src.models.dialogue import DialogueHistoryTemplate
from src.models.dialogue.constants import *
from src.dbo.dialogue.DBODialogueTemplate import *

FALLBACK_DIALOGUE_MOVE = 1  # GENERAL DIALOGUE TEMPLATE
MAX_WAITING_TIME = 7000  # 7 SECONDS


class DialoguePlanner:

    def __init__(self):
        super().__init__()
        self.frequency_count = np.zeros(len(DIALOGUE_LIST))
        self.is_usable = [False] * len(DIALOGUE_LIST)
        self.move_index = -1

        self.dialogue_history = []
        self.usable_templates = []

        self.curr_event = None

        self.dialogue_template = DBODialogueTemplate('templates')

        self.chosen_move_index = -1
        self.chosen_dialogue_move = None
        self.chosen_dialogue_template = []

        self.seed_time = time.time()
        self.num_action_events = 0
        # TODO seed(Handle triggered
        np.random.seed(DEFAULT_SEED)

    def set_state(self, curr_event, num_action_events):
        self.curr_event = curr_event
        self.num_action_events = num_action_events

    def reset_state(self):
        self.chosen_dialogue_move = None
        self.chosen_dialogue_template = []
        self.chosen_move_index = -1
        self.move_index = -1
        # self.curr_event = None
        self.num_action_events = 0

        self.is_usable = []
        self.is_usable = [False] * len(DIALOGUE_LIST)

    def perform_dialogue_planner(self, dialogue_move=""):
        if dialogue_move == "":
            self.setup_templates_is_usable()

            Logger.log_dialogue_model_basic("Breakdown of values used:")
            Logger.log_dialogue_model_basic_example(DIALOGUE_LIST)
            Logger.log_dialogue_model_basic_example(self.is_usable)
            Logger.log_dialogue_model_basic_example(self.frequency_count)

            self.chosen_move_index = self.choose_dialogue()
            Logger.log_dialogue_model_basic("Chosen dialogue index: " + str(self.chosen_move_index))

            self.chosen_dialogue_move = DIALOGUE_LIST[self.chosen_move_index].get_type()
            self.chosen_dialogue_template = self.usable_templates[self.chosen_move_index]

            # self.dialogue_history.append(DialogueHistoryTemplate(dialogue_type=self.chosen_dialogue_move))
            # print("HERE'S THE DIALOGUE HISTORY: ", len(self.dialogue_history))
            # print(self.dialogue_history)
            # self.print_dialogue_list()

        else:
            self.chosen_dialogue_move = dialogue_move
            self.chosen_dialogue_template = self.get_usable_templates(dialogue_move)

        self.dialogue_history.append(DialogueHistoryTemplate(dialogue_type=self.chosen_dialogue_move))
        print("HERE'S THE DIALOGUE HISTORY: ", len(self.dialogue_history))
        print(self.dialogue_history)
        self.print_dialogue_list()

        return self.chosen_dialogue_move



    def setup_templates_is_usable(self):
        self.init_set_dialogue_moves_usable()

        # fetch all usable dialogue templates
        for i in range(len(DIALOGUE_LIST)):
            #check if dialogue move is initially valid
            to_check = DIALOGUE_LIST[i]
            Logger.log_dialogue_model_basic(to_check)
            if self.is_usable[i]:
                # check if dialogue has templates
                self.usable_templates.append(self.get_usable_templates(DIALOGUE_LIST[i].get_type()))

            else:
                self.usable_templates.append([])
            # gets number of occurences
            self.frequency_count[i] = self.get_num_usage(DIALOGUE_LIST[i].get_type())

        # recheck dialogue moves given templates
        for i in range(len(DIALOGUE_LIST)):
            self.is_usable[i] = self.is_dialogue_usable(DIALOGUE_LIST[i].get_type(), self.usable_templates[i])


    def init_set_dialogue_moves_usable(self):
        # check which dialogue moves are usable
        set_to_true = []

        if self.num_action_events <= 3:
            set_to_true.append(DIALOGUE_TYPE_FEEDBACK)
            set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)

        elif self.get_num_usage(DIALOGUE_TYPE_FEEDBACK) == 3 or self.get_num_usage(DIALOGUE_TYPE_PUMPING_GENERAL) == 3:
            set_to_true.append(DIALOGUE_TYPE_PUMPING_SPECIFIC)
            set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)

        else:
            set_to_true = [True for i in range(len(DIALOGUE_LIST))]
        self.set_dialogue_list_true(set_to_true)

    def set_dialogue_list_true(self, set_to_true):
        for i in range(len(set_to_true)):
            for j in range(len(DIALOGUE_LIST)):
                if DIALOGUE_LIST[j].get_type() == set_to_true[i]:
                    self.is_usable[j] = True

        self.print_dialogue_list()

    def is_dialogue_usable(self, dialogue_type, curr_usable_templates):
        if len(curr_usable_templates) == 0:
            return False

        # can be repeated 3 times only
        if len(self.dialogue_history) >= 3:
            len_dialogue = len(self.dialogue_history)
            if self.dialogue_history[len_dialogue - 3] == dialogue_type and \
                    self.dialogue_history[len_dialogue - 2] == dialogue_type and \
                    self.dialogue_history[len_dialogue - 1] == dialogue_type:
                return False
        return True

    def  get_usable_templates(self, move_to_execute):
        usable_template_list = []

        template_list = self.dialogue_template.get_templates_of_type(move_to_execute)

        # check which template is usable
        for X in template_list:
            print("Checking:", X)
            if X.is_usable(self.curr_event, self.get_num_usage(X.get_type())):
                usable_template_list.append(X)

        return usable_template_list

    def get_num_usage(self, dialogue_type):
        # returns number of times it has been used
        count = 0
        for X in self.dialogue_history:
            if X.dialogue_type == dialogue_type:
                count = count + 1
        return count

    def select_dialogue_from_weights(self, weights_to_use):
        # weights_to_use = self.frequency_count

        probability = np.repeat(1 / len(weights_to_use), len(weights_to_use))
        if np.count_nonzero(weights_to_use) > 0:
            max_value = np.max(weights_to_use)
            max_value_list = np.repeat(max_value, len(weights_to_use))

            weights_to_use - np.asarray(weights_to_use)

            numerator = max_value_list - weights_to_use
            print(numerator)

            probability = numerator / max_value_list
            print(probability)

        candidates = np.argwhere(probability == np.amax(probability))
        candidates = candidates.flatten().tolist()
        print(candidates)

        # np.random.seed(int(self.seed_time))
        choice = np.random.choice(candidates)

        return choice

    def choose_dialogue(self):

        moves_to_eval = self.get_valid_moves_index()
        weights_to_eval = self.get_weights_from_index(moves_to_eval)

        dialogue_move_index = self.select_dialogue_from_weights(weights_to_eval)

        return moves_to_eval[dialogue_move_index]

    def get_weights_from_index(self, indexes):
        weights = []
        for i in indexes:
            weights.append(self.frequency_count[i])
        return weights

    def get_valid_moves_index(self):
        valid_moves = []
        for i in range(len(self.is_usable)):
            if self.is_usable[i]:
                valid_moves.append(i)
        return valid_moves

    ###checks only dialogue that does not need to go through text understanding
    def check_trigger_phrases(self, response, event_chain, curr_event):
        if response in IS_END:
            return DIALOGUE_TYPE_E_END
        if response in PUMPING_TRIGGER:
            if len(event_chain) > 0:
                return DIALOGUE_TYPE_PUMPING_SPECIFIC
            return DIALOGUE_TYPE_PROMPT
        elif response in PROMPT_TRIGGER:
            return DIALOGUE_TYPE_PROMPT


        return self.check_based_prev_move(response, curr_event)



    def check_based_prev_move(self, response, curr_event):
        last_move = self.get_last_dialogue_move()
        if last_move is not None:
            print("LAST MOVE IS: ", last_move.dialogue_type)
            ###START EDEN
            #check if last move is eden

            if last_move.dialogue_type == DIALOGUE_TYPE_E_LABEL:
                if response in IS_AFFIRM:
                    return DIALOGUE_TYPE_C_PUMPING
                else:
                    return DIALOGUE_TYPE_E_PUMPING
            elif last_move.dialogue_type == DIALOGUE_TYPE_E_PUMPING:
                self.curr_event.emotion = response

                return DIALOGUE_TYPE_C_PUMPING
            elif last_move.dialogue_type == DIALOGUE_TYPE_C_PUMPING:
                #check if emotion is + or -
                if curr_event.emotion is not None:
                    print("EMOTION TYPE OF ", curr_event.emotion)
                    print(" IS: ", curr_event.get_emotion_type())
                    if curr_event.get_emotion_type() == EMOTION_TYPE_POSITIVE:
                        return DIALOGUE_TYPE_D_PRAISE
                        # return DIALOGUE_TYPE_EVALUATION
                    else:
                        return DIALOGUE_TYPE_D_CORRECTING
            elif last_move.dialogue_type == DIALOGUE_TYPE_D_CORRECTING:
                if response in IS_AFFIRM:
                    return DIALOGUE_TYPE_EVALUATION
                else:
                    return DIALOGUE_TYPE_D_PUMPING
            elif last_move.dialogue_type == DIALOGUE_TYPE_D_PUMPING:
                return DIALOGUE_TYPE_EVALUATION
            elif last_move.dialogue_type == DIALOGUE_TYPE_EVALUATION:
                return DIALOGUE_TYPE_RECOLLECTION

            ###END EDEN

            # check if prev move is suggestion
            if last_move.dialogue_type == DIALOGUE_TYPE_SUGGESTING:
                if response in IS_AFFIRM:
                    return DIALOGUE_TYPE_SUGGESTING_AFFIRM
                elif response in IS_DENY:
                    return DIALOGUE_TYPE_FOLLOW_UP
            #check if prev move is follow up
            elif last_move.dialogue_type == DIALOGUE_TYPE_FOLLOW_UP:
                if response in IS_DONT_LIKE:
                    return DIALOGUE_TYPE_FOLLOW_UP_DONT_LIKE
                if response in IS_WRONG:
                    return DIALOGUE_TYPE_FOLLOW_UP_WRONG

        else:
            print("NO PREVIOUS DIALOGUE")
        return None


    # ###checks only dialogue that does not need to go through text understanding
    # def check_trigger_phrases(self, response, event_chain):
    #     response = response.lower()
    #
    #     #get latest dialogue move
    #     last_move = self.get_last_dialogue_move()
    #
    #     if last_move is not None:
    #         print("LAST MOVE IS: ", last_move.dialogue_type)
    #         ###START EDEN
    #         #check if last move is eden
    #         if last_move.dialogue_type == DIALOGUE_TYPE_E_LABEL:
    #             if response in IS_AFFIRM:
    #                 return DIALOGUE_TYPE_C_PUMPING
    #             else:
    #                 return DIALOGUE_TYPE_E_PUMPING
    #             # elif last_move.dialogue_type == DIALOGUE_TYPE_E_PUMPING:
    #             #     return DIALOGUE_TYPE_C_PUMPING
    #             # elif last_move.dialogue_type == DIALOGUE_TYPE_C_PUMPING:
    #             #     #check if emotion is + or -
    #             #     if curr_emotion.get_emotion_type == EMOTION_TYPE_POSITIVE:
    #             #         return DIALOGUE_TYPE_D_PRAISE
    #             #     else:
    #             #         return DIALOGUE_TYPE_D_CORRECTING
    #         elif last_move.dialogue_type == DIALOGUE_TYPE_D_CORRECTING:
    #             if response in IS_AFFIRM:
    #                 return DIALOGUE_TYPE_EVALUATION
    #             else:
    #                 return DIALOGUE_TYPE_D_PUMPING
    #             # elif last_move.dialogue_type == DIALOGUE_TYPE_D_PUMPING:
    #             #     return DIALOGUE_TYPE_EVALUATION
    #             # elif last_move.dialogue_type == DIALOGUE_TYPE_EVALUATION:
    #             #     return DIALOGUE_TYPE_RECOLLECTION
    #
    #         ###END EDEN
    #
    #         # check if prev move is suggestion
    #         if last_move.dialogue_type == DIALOGUE_TYPE_SUGGESTING:
    #             if response in IS_AFFIRM:
    #                 return DIALOGUE_TYPE_SUGGESTING_AFFIRM
    #             elif response in IS_DENY:
    #                 return DIALOGUE_TYPE_FOLLOW_UP
    #         #check if prev move is follow up
    #         elif last_move.dialogue_type == DIALOGUE_TYPE_FOLLOW_UP:
    #             if response in IS_DONT_LIKE:
    #                 return DIALOGUE_TYPE_FOLLOW_UP_DONT_LIKE
    #             if response in IS_WRONG:
    #                 return DIALOGUE_TYPE_FOLLOW_UP_WRONG
    #
    #     else:
    #         print("NO PREVIOUS DIALOGUE")
    #     if response in PUMPING_TRIGGER:
    #         if len(event_chain) > 0:
    #             return DIALOGUE_TYPE_PUMPING_SPECIFIC
    #         return DIALOGUE_TYPE_PROMPT
    #     elif response in PROMPT_TRIGGER:
    #         return DIALOGUE_TYPE_PROMPT
    #     return None


    def set_template_details_history(self, chosen_template):
        print("CUR LEN DIALOGUE HISTORY: ", len(self.dialogue_history))
        self.dialogue_history[len(self.dialogue_history) - 1].set_template_details(chosen_template)

    def print_dialogue_list(self):
        print("\n\nCHOSEN DIALOGUE MOVE: ", self.chosen_dialogue_move)

        print("move", "\t", "is_usable")
        for i in range(len(DIALOGUE_LIST)):
            print(DIALOGUE_LIST[i], "\t", self.is_usable[i])

    def get_last_dialogue_move(self):
        if len(self.dialogue_history) ==0:
            return None
        return self.dialogue_history[len(self.dialogue_history)-1]

    def is_move_eden(self, type):
        for X in EDEN_DIALOGUE_LIST:
            if X.dialogue_type == type:
                return True
        return False

    def get_next_eden_move(self, curr_emotion):
        # get latest dialogue move
        last_move = self.get_last_dialogue_move()
        if last_move is not None and self.is_move_eden(last_move):
            if last_move.dialogue_type == DIALOGUE_TYPE_E_PUMPING:
                return DIALOGUE_TYPE_C_PUMPING
            elif last_move.dialogue_type == DIALOGUE_TYPE_C_PUMPING:
                #check if emotion is + or -
                if curr_emotion.get_emotion_type() == EMOTION_TYPE_POSITIVE:
                    return DIALOGUE_TYPE_D_PRAISE
                else:
                    return DIALOGUE_TYPE_D_CORRECTING
            elif last_move.dialogue_type == DIALOGUE_TYPE_D_PUMPING:
                return DIALOGUE_TYPE_EVALUATION
            elif last_move.dialogue_type == DIALOGUE_TYPE_EVALUATION:
                return DIALOGUE_TYPE_RECOLLECTION
        return DIALOGUE_TYPE_E_LABEL