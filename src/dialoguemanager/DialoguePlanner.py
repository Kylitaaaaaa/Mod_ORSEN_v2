import numpy as np
import time

from src import Logger, DIALOGUE_TYPE_FEEDBACK, DIALOGUE_TYPE_PUMPING_GENERAL
from src.models.dialogue import DialogueHistoryTemplate
from src.models.dialogue.constants import *
from src.dbo.dialogue.DBODialogueTemplate import DBODialogueTemplate, PUMPING_TRIGGER, PROMPT_TRIGGER, \
    DIALOGUE_TYPE_PUMPING_SPECIFIC, DIALOGUE_TYPE_PROMPT

FALLBACK_DIALOGUE_MOVE = 2 # GENERAL DIALOGUE TEMPLATE
MAX_WAITING_TIME = 7000 # 7 SECONDS
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
        self.num_action_events =0
        #TODO Handle triggered


    def set_state(self, curr_event, num_action_events):
        self.curr_event = curr_event
        self.num_action_events =num_action_events

    def reset_state(self):
        self.chosen_dialogue_move = None
        self.chosen_dialogue_template = []
        self.chosen_move_index = -1
        self.move_index = -1
        self.is_usable = []
        self.curr_event = None
        self.num_action_events = 0

    def perform_dialogue_planner(self, dialogue_move = ""):
        if dialogue_move == "":
            self.setup_templates_is_usable()




            # for i in range(len(DIALOGUE_LIST)):
                # if DIALOGUE_LIST[i].get_type() == DIALOGUE_TYPE_PROMPT:
                #     print("IT'S A PROMPT")
                #     self.usable_templates.append([])
                #     self.is_usable.append(False)
                # else:
                #     print("IT'S NOT A PROMPT")
                #     to_check = DIALOGUE_LIST[i]
                #     Logger.log_dialogue_model_basic(to_check)
                #
                #     # check if dialogue has templates
                #     curr_usable_templates = self.get_usable_templates(DIALOGUE_LIST[i].get_type())
                #     self.usable_templates.append(curr_usable_templates)


            #check if should randomize weights
            # if self.is_randomizable():
            #     #if yes do this
            #         # check if dialogue can be repeated (Only up to 3 times)
            #         self.is_usable.append(self.is_dialogue_usable(DIALOGUE_LIST[i].get_type(), curr_usable_templates))
            # else:
            #     pass
            #     #manually set is_usable
            #
            #     # gets number of occurences
            #     self.frequency_count[i] = self.get_num_usage(DIALOGUE_LIST[i].get_type())

            Logger.log_dialogue_model_basic("Breakdown of values used:")
            Logger.log_dialogue_model_basic_example(DIALOGUE_LIST)
            Logger.log_dialogue_model_basic_example(self.is_usable)
            Logger.log_dialogue_model_basic_example(self.frequency_count)

            self.chosen_move_index = self.choose_dialogue()
            Logger.log_dialogue_model_basic("Chosed dialogue index: " + str(self.chosen_move_index))

            self.chosen_dialogue_move = DIALOGUE_LIST[self.chosen_move_index].get_type()
            self.chosen_dialogue_template = self.usable_templates[self.chosen_move_index]

            # add chosen dialogue move to dialogue history TODO call DialogueTemplateBuilder
            self.dialogue_history.append(DialogueHistoryTemplate(dialogue_type = self.chosen_dialogue_move))
            print("\n\nCHOSEN DIALOGUE MOVE: ", self.chosen_dialogue_move)

            print("move", "\t", "num_temp", "\t", "is_usable", "\t", "weight")
            for i in range(len(DIALOGUE_LIST)):
                print(DIALOGUE_LIST[i], "\t", len(self.usable_templates[i]), "\t", self.is_usable[i], "\t", self.frequency_count[i])

        else:
            self.chosen_dialogue_move = dialogue_move
            self.chosen_dialogue_template = self.get_usable_templates(dialogue_move)

        return self.chosen_dialogue_move


    def setup_templates_is_usable(self):
        if self.num_action_events <= 3:
            self.is_usable[DIALOGUE_LIST.index(DIALOGUE_TYPE_FEEDBACK)] = True
            self.is_usable[DIALOGUE_LIST.index(DIALOGUE_TYPE_PUMPING_GENERAL)] = True
        elif self.get_num_usage(DIALOGUE_TYPE_FEEDBACK) == 3 or self.get_num_usage(DIALOGUE_TYPE_PUMPING_GENERAL) == 3:
            self.is_usable[DIALOGUE_LIST.index(DIALOGUE_TYPE_PUMPING_SPECIFIC)] = True

        for i in range(len(DIALOGUE_LIST)):
            to_check = DIALOGUE_LIST[i]
            Logger.log_dialogue_model_basic(to_check)

            # check if dialogue has templates
            self.usable_templates.append(self.get_usable_templates(DIALOGUE_LIST[i].get_type()))

            # check if dialogue can be repeated (Only up to 3 times)
            self.is_usable.append(self.is_dialogue_usable(DIALOGUE_LIST[i].get_type(), self.usable_templates[i]))

            # gets number of occurences
            self.frequency_count[i] = self.get_num_usage(DIALOGUE_LIST[i].get_type())

        #TODO check suggestion

    def is_dialogue_usable(self, dialogue_type, curr_usable_templates):
        if len(curr_usable_templates) == 0:
            return False

        #can be repeated 3 times only
        if len(self.dialogue_history) >= 3:
            len_dialogue = len(self.dialogue_history)
            if self.dialogue_history[len_dialogue-3] == dialogue_type and \
                    self.dialogue_history[len_dialogue-2] == dialogue_type and \
                    self.dialogue_history[len_dialogue-1] == dialogue_type:
                return False
        return True

    def get_usable_templates(self, move_to_execute):
        usable_template_list = []

        template_list = self.dialogue_template.get_templates_of_type(move_to_execute)

        # check which template is usable
        for X in template_list:
            if X.is_usable(self.curr_event, self.get_num_usage(X.get_type())):
                usable_template_list.append(X)

        return usable_template_list

    def get_num_usage(self, dialogue_type):
        #returns number of times it has been used
        count = 0
        for X in self.dialogue_history:
            if X.dialogue_type == dialogue_type:
                count = count + 1
        return count

    def select_dialogue_from_weights(self):
        weights_to_use = self.frequency_count

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

        np.random.seed(int(self.seed_time))
        choice = np.random.choice(candidates)

        return choice

    def choose_dialogue(self):
        dialogue_move_index = -1

        timeout = time.time() + MAX_WAITING_TIME
        ctr = 0
        while ctr < 5 and time.time() <= timeout:

            dialogue_move_index = self.select_dialogue_from_weights()
            if dialogue_move_index > -1:
                if self.is_usable[dialogue_move_index]:
                    break

            ctr = ctr + 1

        if dialogue_move_index == -1:
            print("USING THE FALLBACK: ", DIALOGUE_LIST[FALLBACK_DIALOGUE_MOVE].get_type())
            dialogue_move_index = FALLBACK_DIALOGUE_MOVE

        return dialogue_move_index



    def check_trigger_phrases(self, response, event_chain):
        response = response.lower()
        if response in PUMPING_TRIGGER:
            if len(event_chain) > 0:
                return DIALOGUE_TYPE_PUMPING_SPECIFIC
            return DIALOGUE_TYPE_PROMPT
        elif response in PROMPT_TRIGGER:
            return DIALOGUE_TYPE_PROMPT
        return None




