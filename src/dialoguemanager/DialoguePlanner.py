import numpy as np
import time

from src import Logger
from src.models.dialogue.constants import *
from src.dbo.dialogue.DBODialogueTemplate import DBODialogueTemplate, PUMPING_TRIGGER, PROMPT_TRIGGER, \
    DIALOGUE_TYPE_PUMPING_SPECIFIC, DIALOGUE_TYPE_PROMPT, IS_END, THE_END

FALLBACK_DIALOGUE_MOVE = 2 # GENERAL DIALOGUE TEMPLATE
MAX_WAITING_TIME = 7000 # 7 SECONDS
class DialoguePlanner:


    def __init__(self):
        super().__init__()
        self.frequency_count = np.zeros(len(DIALOGUE_LIST))
        self.is_usable = []
        self.move_index = -1

        self.dialogue_history = []
        self.usable_templates = []

        self.curr_event = None

        self.dialogue_template = DBODialogueTemplate('templates')

        self.chosen_move_index = -1
        self.chosen_dialogue_move = None
        self.chosen_dialogue_template = []

        self.seed_time = time.time()
    #TODO Handle triggered

    def reset_state(self):
        self.chosen_dialogue_move = None
        self.chosen_dialogue_template = []
        self.chosen_move_index = -1
        self.move_index = -1
        self.is_usable = []
        self.curr_event = None

    def perform_dialogue_planner(self, dialogue_move = ""):
        if dialogue_move == "":
            for i in range(len(DIALOGUE_LIST)):
                if DIALOGUE_LIST[i].get_type() == DIALOGUE_TYPE_PROMPT:
                    print("IT'S A PROMPT")
                    self.usable_templates.append([])
                    self.is_usable.append(False)
                else:
                    print("IT'S NOT A PROMPT")
                    to_check = DIALOGUE_LIST[i]
                    Logger.log_dialogue_model_basic(to_check)

                    # feedback[d1, d4, d5]
                    # general[d7, d9, 10]
                    # pumping[d11, d12, d15]
                    # list.append() --> [[],[],[]]]

                    # check if dialogue has templates
                    curr_usable_templates = self.get_usable_templates(DIALOGUE_LIST[i].get_type())
                    self.usable_templates.append(curr_usable_templates)


                    # check if dialogue can be repeated (Only up to 3 times)
                    self.is_usable.append(self.is_dialogue_usable(DIALOGUE_LIST[i].get_type(), curr_usable_templates))

                # gets number of occurences
                self.frequency_count[i] = self.get_num_usage(DIALOGUE_LIST[i].get_type())

            Logger.log_dialogue_model_basic("Breakdown of values used:")
            Logger.log_dialogue_model_basic_example(DIALOGUE_LIST)
            Logger.log_dialogue_model_basic_example(self.is_usable)
            Logger.log_dialogue_model_basic_example(self.frequency_count)

            self.chosen_move_index = self.choose_dialogue()
            Logger.log_dialogue_model_basic("Chosed dialogue index: " + str(self.chosen_move_index))

            self.chosen_dialogue_move = DIALOGUE_LIST[self.chosen_move_index].get_type()
            self.chosen_dialogue_template = self.usable_templates[self.chosen_move_index]

            # add chosen dialogue move to dialogue history TODO call DialogueTemplateBuilder
            self.dialogue_history.append(self.chosen_dialogue_move)
            print("\n\nCHOSEN DIALOGUE MOVE: ", self.chosen_dialogue_move)

            print("move", "\t", "num_temp", "\t", "is_usable", "\t", "weight")
            for i in range(len(DIALOGUE_LIST)):
                print(DIALOGUE_LIST[i], "\t", len(self.usable_templates[i]), "\t", self.is_usable[i], "\t", self.frequency_count[i])



        else:
            self.chosen_dialogue_move = dialogue_move
            self.chosen_dialogue_template = self.get_usable_templates(dialogue_move)

        return self.chosen_dialogue_move

    # def test_perform_dialogue_planner(self, dialogue_move):
    #     self.chosen_dialogue_move = dialogue_move
    #     self.chosen_dialogue_template = self.get_usable_templates(dialogue_move)
    #
    #     return self.chosen_dialogue_move

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

        # dialogue_template.get_templates_of_type()

        template_list = self.dialogue_template.get_templates_of_type(move_to_execute)

        # check which template is usable
        for X in template_list:
            if X.is_usable(self.curr_event):
                usable_template_list.append(X)

        return usable_template_list

    def get_num_usage(self, dialogue_type):
        #returns number of times it has been used
        return self.dialogue_history.count(dialogue_type)


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

    # def get_weights(self):
    #
    #     usable = np.ones(len(DIALOGUE_LIST))
    #
    #     totals = usable * self.frequency_count
    #     Logger.log_information_extraction_basic_example(totals)
    #
    #     print("totals: ", sum(totals))
    #     percentages = totals / sum(totals)
    #     if np.isfinite(percentages).all():
    #         percentages = []
    #         for i in range(len(DIALOGUE_LIST)):
    #             percentages.append(1/len(DIALOGUE_LIST))
    #
    #     # if only one highest candidate, only get its index
    #     # otherwise, randomize between the list of highest candidates
    #     self.move_index = np.argmax(percentages)
    #     if self.move_index > 1:
    #         self.move_index = np.random.choice(self.move_index)
    #
    #     # increases weight of everything except the one that will be used. It wouldn't make much sense to increase the weight of the most recently used, thus being the reason why it retains the current value it has.
    #     self.frequency_count = self.frequency_count + 1
    #     self.frequency_count[self.move_index] = self.frequency_count[self.move_index] - 1
    #     # print("Here are the weights")
    #     # for X in self.weights:
    #     #     print(X)
    #
    #     #returning chosen index
    #     return self.move_index

    def choose_dialogue(self):
        dialogue_move_index = -1

        timeout = time.time() + MAX_WAITING_TIME
        ctr = 0
        while ctr < 5 and time.time() <= timeout:

            # if ctr == 5 or time.time() > timeout:
            #     curr_index = FALLBACK_DIALOGUE_MOVE
            #     break

            dialogue_move_index = self.select_dialogue_from_weights()
            if dialogue_move_index > -1:
                if self.is_usable[dialogue_move_index]:
                    break

            ctr = ctr + 1

        if dialogue_move_index == -1:
            print("USING THE FALLBACK: ", DIALOGUE_LIST[FALLBACK_DIALOGUE_MOVE].get_type())
            dialogue_move_index = FALLBACK_DIALOGUE_MOVE

        return dialogue_move_index

    def set_event(self, curr_event):
        self.curr_event = curr_event

    def check_trigger_phrases(self, response, event_chain):
        response = response.lower()
        if response in PUMPING_TRIGGER:
            if len(event_chain) > 0:
                print("TRIGGERED PUMP")
                return DIALOGUE_TYPE_PUMPING_SPECIFIC
            print("TRIGGERED PROMPT")
            return DIALOGUE_TYPE_PROMPT
        elif response in PROMPT_TRIGGER:
            print("TRIGGERED PROMPT")
            return DIALOGUE_TYPE_PROMPT
        print("TRIGGERED NOTHING")
        return None




