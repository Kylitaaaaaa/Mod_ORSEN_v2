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




