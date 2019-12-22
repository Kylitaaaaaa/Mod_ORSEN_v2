from EDEN.constants import *
from src import *
from src.dialoguemanager import DialoguePlanner, ORSENDialoguePlanner


class ORSEN2DialoguePlanner(DialoguePlanner):

    def __init__(self):
        super().__init__()
        self.response = ""

    def init_set_dialogue_moves_usable(self, preselected_move=""):
        # check which dialogue moves are usable
        set_to_true = []
        if preselected_move =="":
            print(self.curr_world_num_events)

            #uncomment to test suggesting
            # if len(self.get_usable_templates(DIALOGUE_TYPE_SUGGESTING)) > 0:
            #     set_to_true.append(DIALOGUE_TYPE_SUGGESTING)

            if self.curr_world_num_events <=3:
                if len(self.get_usable_templates(DIALOGUE_TYPE_FEEDBACK)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_FEEDBACK)
                if len(self.get_usable_templates(DIALOGUE_TYPE_PUMPING_GENERAL)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)
                if len(self.get_usable_templates(DIALOGUE_TYPE_PUMPING_SPECIFIC)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_PUMPING_SPECIFIC)
            elif self.get_num_dialogue_history(DIALOGUE_TYPE_FEEDBACK) == 3:
                if len(self.get_usable_templates(DIALOGUE_TYPE_PUMPING_SPECIFIC)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_PUMPING_SPECIFIC)
            else:
                if len(self.get_usable_templates(DIALOGUE_TYPE_FEEDBACK)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_FEEDBACK)
                if len(self.get_usable_templates(DIALOGUE_TYPE_PUMPING_GENERAL)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)
                if len(self.get_usable_templates(DIALOGUE_TYPE_PUMPING_SPECIFIC)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_PUMPING_SPECIFIC)
                if len(self.get_usable_templates(DIALOGUE_TYPE_HINTING)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_HINTING)
                if len(self.get_usable_templates(DIALOGUE_TYPE_SUGGESTING)) > 0:
                    set_to_true.append(DIALOGUE_TYPE_SUGGESTING)
        else:
            set_to_true.append(preselected_move)
        self.set_dialogue_list_true(set_to_true)

    ###checks only dialogue that does not need to go through text understanding
    def check_trigger_phrases(self, event_chain =[]):
        if self.response in PROMPT_TRIGGER:
            return DIALOGUE_TYPE_PROMPT
        elif self.response in HINTING_TRIGGER:
            return DIALOGUE_TYPE_HINTING
        elif self.response in PUMPING_TRIGGER:
            return DIALOGUE_TYPE_PUMPING_SPECIFIC
        return ""

    def check_based_prev_move(self, destructive = True):
        last_move = self.get_last_dialogue_move()

        if last_move is not None:
            print("LAST MOVE IS: ", last_move.dialogue_type)

            # check if prev move is suggestion
            if last_move.dialogue_type == DIALOGUE_TYPE_SUGGESTING:
                if self.response in IS_AFFIRM:
                    # TODO: Add to story world
                    pass
                elif self.response in IS_DENY:
                    return DIALOGUE_TYPE_FOLLOW_UP
            # check if prev move is follow up
            elif last_move.dialogue_type == DIALOGUE_TYPE_FOLLOW_UP:
                if self.response in IS_DONT_LIKE:
                    # TODO: Point System
                    return DIALOGUE_TYPE_FOLLOW_UP_DONT_LIKE
                if self.response in IS_WRONG:
                    # TODO: Point System
                    return DIALOGUE_TYPE_FOLLOW_UP_WRONG

        else:
            print("NO PREVIOUS DIALOGUE")
        return ""

    # suggestion model
    def is_ongoing_done(self):
        pass


