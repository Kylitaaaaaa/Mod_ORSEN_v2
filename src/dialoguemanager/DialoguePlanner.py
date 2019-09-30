import numpy as np
from src.models.dialogue.constants import *


class DialoguePlanner:
    dialogue_history = []

    def __init__(self):
        super().__init__()
        self.weights = np.zeros(len(DIALOGUE_LIST))
        self.is_usable = np.zeros(len(DIALOGUE_LIST))
        self.move_index = -1

    #TODO Handle triggered


    def perform_dialogue_planner(self):
        print("Dialogue_list: ", len(DIALOGUE_LIST))
        for i in range(len(DIALOGUE_LIST)):
            # check if dialogue can be repeated (Only up to 3 times)
            self.is_usable[i] = self.is_dialogue_usable(DIALOGUE_LIST[i].get_type())

            # gets number of occurences
            self.weights[i] = self.get_num_usage(DIALOGUE_LIST[i].get_type())

        self.get_weights()

        print("I choose: ", self.choose_dialogue())

        # add chosen dialogue move to dialogue history TODO call DialogueTemplateBuilder
        # curr_dialogue_move = None
        # self.dialogue_history.append(curr_dialogue_move)

        pass

    def is_dialogue_usable(self, dialogue_type):
        #can be repeated 3 times only
        if len(self.dialogue_history) >= 3:
            len_dialogue = len(self.dialogue_history)
            if self.dialogue_history[len_dialogue-2] == dialogue_type and \
                    self.dialogue_history[len_dialogue-1] == dialogue_type and \
                    self.dialogue_history[len_dialogue] == dialogue_type:
                return 0
        return 1

    def get_num_usage(self, dialogue_type):
        #returns number of times it has been used
        return self.dialogue_history.count(dialogue_type)

    def get_weights(self):
        usable = np.ones(len(DIALOGUE_LIST))


        totals = usable * self.weights
        print("totals: ", sum(totals))
        percentages = totals / sum(totals)
        if np.isfinite(percentages).all():
            percentages = []
            for i in range(len(DIALOGUE_LIST)):
                percentages.append(1/len(DIALOGUE_LIST))

        # if only one highest candidate, only get its index
        # otherwise, randomize between the list of highest candidates
        self.move_index = np.argmax(percentages)
        if self.move_index > 1:
            self.move_index = np.random.choice(self.move_index)

        # increases weight of everything except the one that will be used. It wouldn't make much sense to increase the weight of the most recently used, thus being the reason why it retains the current value it has.
        self.weights = self.weights + 1
        self.weights[self.move_index] = self.weights[self.move_index] - 1
        print("Here are the weights")
        for X in self.weights:
            print(X)

    def choose_dialogue(self):
        # num_to_pick = 1
        # draw = np.random.choice(DIALOGUE_LIST, num_to_pick, p=self.weights)
        # return draw
        return self.move_index




