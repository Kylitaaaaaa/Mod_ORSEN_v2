from EDEN.OCC import OCCManager
from EDEN.constants import *
from src import *
from src.dbo.dialogue import DBODialogueTemplate
from src.dialoguemanager import DialoguePlanner
from src.models.dialogue.constants import DIALOGUE_LIST, DialogueHistoryTemplate, EDEN_DIALOGUE_LIST
import time
import numpy as np

class ORSENDialoguePlanner(DialoguePlanner):

    def __init__(self):
        super().__init__()

    def init_set_dialogue_moves_usable(self, preselected_move=""):
        # check which dialogue moves are usable
        set_to_true = []
        if preselected_move =="":
            if len(self.get_usable_templates(DIALOGUE_TYPE_PUMPING_GENERAL)) > 0:
                set_to_true.append(DIALOGUE_TYPE_PUMPING_GENERAL)
            if len(self.get_usable_templates(DIALOGUE_TYPE_PUMPING_SPECIFIC)) > 0:
                set_to_true.append(DIALOGUE_TYPE_PUMPING_SPECIFIC)
            if len(self.get_usable_templates(DIALOGUE_TYPE_FEEDBACK)) > 0:
                set_to_true.append(DIALOGUE_TYPE_FEEDBACK)
        else:
            set_to_true.append(preselected_move)
        self.set_dialogue_list_true(set_to_true)

    def finalize_dialogue_move(self, curr_dialogue_move):
        if curr_dialogue_move == DIALOGUE_TYPE_RECOLLECTION:
            return DIALOGUE_TYPE_E_END
        return ""

    def check_auto_response(self, destructive = True, emotion_event = None):
        next_move = self.check_trigger_phrases()
        return next_move

    def check_trigger_phrases(self, event_chain =[]):
        if self.response in PROMPT_TRIGGER:
            return DIALOGUE_TYPE_PROMPT
        elif self.response in PUMPING_TRIGGER:
            return DIALOGUE_TYPE_PUMPING_SPECIFIC
        elif self.response in HINTING_TRIGGER:
            return DIALOGUE_TYPE_HINTING
        return ""


