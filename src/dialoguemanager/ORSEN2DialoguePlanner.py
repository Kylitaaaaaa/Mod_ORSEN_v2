from EDEN.constants import *
from src import *
from src.dialoguemanager import DialoguePlanner

class ORSEN2DialoguePlanner(DialoguePlanner):

    def __init__(self):
        super().__init__()
        self.response = ""

    ###checks only dialogue that does not need to go through text understanding
    # def check_trigger_phrases(self, response, event_chain):
    def check_trigger_phrases(self, event_chain):
        if self.response in IS_END:
            return DIALOGUE_TYPE_E_END
        if self.response in PUMPING_TRIGGER:
            if len(event_chain) > 0:
                return DIALOGUE_TYPE_PUMPING_SPECIFIC
            return DIALOGUE_TYPE_PROMPT
        elif self.response in PROMPT_TRIGGER:
            return DIALOGUE_TYPE_PROMPT

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
