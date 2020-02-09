from EDEN.constants import *
from src import *
from src.dialoguemanager import DialoguePlanner
import numpy as np
import time
from src.models.dialogue import DialogueHistoryTemplate
from src.models.dialogue.constants import *
from src.dbo.dialogue.DBODialogueTemplate import *

class ORSEN2DialoguePlanner(DialoguePlanner):

    def __init__(self):
        super().__init__()
        self.response = ""
        
    def reset_new_world(self):
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
        self.response = ""
    
    def init_set_dialogue_moves_usable(self):
        # check which dialogue moves are usable
        set_to_true = []

        # set_to_true.append(DIALOGUE_TYPE_HINTING)
        # set_to_true.append(DIALOGUE_TYPE_SUGGESTING)

        if self.num_action_events <= 3:
            set_to_true.append(DIALOGUE_TYPE_FEEDBACK)
            set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)

        elif self.get_num_usage(DIALOGUE_TYPE_FEEDBACK) + self.get_num_usage(DIALOGUE_TYPE_PUMPING_GENERAL) == 3:
            set_to_true.append(DIALOGUE_TYPE_PUMPING_SPECIFIC)
            set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)

        else:
            set_to_true = ['feedback', 'general', 'specific', 'hinting', 'suggesting']

        self.set_dialogue_list_true(set_to_true)

    ###checks only dialogue that does not need to go through text understanding
    def check_trigger_phrases(self, response, event_chain):
        response = response.lower()

        #get latest dialogue move
        last_move = self.get_last_dialogue_move()
        if last_move is not None:
            print("Last Move Dialogue Type: ", last_move.dialogue_type)

        if last_move is not None:
            # check if prev move is suggestion
            if last_move.dialogue_type == DIALOGUE_TYPE_SUGGESTING:
                if response in IS_AFFIRM:
                    return DIALOGUE_TYPE_SUGGESTING_AFFIRM
                elif response in IS_DENY:
                    return DIALOGUE_TYPE_FOLLOW_UP
            #check if prev move is follow up
            elif last_move.dialogue_type == DIALOGUE_TYPE_FOLLOW_UP:
                print("LAST MOVE IS FOLLOW UP")
                if response in IS_DONT_LIKE:
                    print("DON'T LIKE")
                    return DIALOGUE_TYPE_KNOWLEDGE_ACQUISITION_PUMPING
                    # return DIALOGUE_TYPE_FOLLOW_UP_DONT_LIKE
                elif response in IS_WRONG:
                    print("DEDUCT")
                    return DIALOGUE_TYPE_FOLLOW_UP_WRONG
            elif last_move.dialogue_type == DIALOGUE_TYPE_KNOWLEDGE_ACQUISITION_PUMPING:
                return DIALOGUE_TYPE_SUGGESTING_AFFIRM       

        if self.response in IS_END:
            return DIALOGUE_TYPE_E_END
        elif response in PUMPING_TRIGGER:
            if len(event_chain) > 0:
                return DIALOGUE_TYPE_PUMPING_SPECIFIC
            return DIALOGUE_TYPE_PROMPT
        elif response in PROMPT_TRIGGER:
            return DIALOGUE_TYPE_PROMPT
        elif response in HINTING_TRIGGER:
            if len(event_chain) > 0:
                return DIALOGUE_TYPE_HINTING
            return DIALOGUE_TYPE_PUMPING_GENERAL
        elif response in SUGGESTING_TRIGGER:
            if len(event_chain) > 0:
                return DIALOGUE_TYPE_SUGGESTING
            return DIALOGUE_TYPE_PUMPING_GENERAL
        return None

    def check_based_prev_move(self):
        last_move = self.get_last_dialogue_move()

        if last_move is not None:
            print("LAST MOVE IS: ", last_move.dialogue_type)
            ###START EDEN
            #check if last move is eden

            # check if prev move is suggestion
            if last_move.dialogue_type == DIALOGUE_TYPE_SUGGESTING:
                if self.response in IS_AFFIRM:
                    return DIALOGUE_TYPE_SUGGESTING_AFFIRM
                elif self.response in IS_DENY:
                    return DIALOGUE_TYPE_FOLLOW_UP
            # check if prev move is follow up
            elif last_move.dialogue_type == DIALOGUE_TYPE_FOLLOW_UP:
                if self.response in IS_DONT_LIKE:
                    return DIALOGUE_TYPE_FOLLOW_UP_DONT_LIKE
                if self.response in IS_WRONG:
                    return DIALOGUE_TYPE_FOLLOW_UP_WRONG

        else:
            print("NO PREVIOUS DIALOGUE")
        return ""

    # suggestion model
    def is_ongoing_done(self):
        pass

    def get_welcome_message_type(self):
        return DIALOGUE_TYPE_ORSEN_WELCOME
