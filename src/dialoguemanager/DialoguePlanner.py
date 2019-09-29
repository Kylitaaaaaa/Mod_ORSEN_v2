import numpy as np
from src.models.dialogue.constants import *

class DialoguePlanner:

    def __init__(self):
        super().__init__()
        self.weights = np.zeros(len(DIALOGUE_LIST))


    def choose_dialogue(self, to_check=[]):
        usable = np.zeros(len(DIALOGUE_LIST))
        for i in range(len(usable)):
            usable = DIALOGUE_LIST[i].is_usable(to_check) * 1

        totals = usable * self.weights
        percentages = totals / sum(totals)

        move_index = np.argmax(percentages)
        if move_index > 1:
            move_index = np.random.choice(move_index)

        self.weights = self.weights + 1
        self.weights[move_index] = self.weights[move_index] - 1
        print("Here are the dialogues")
        for X in self.weights:
            print(X)

        return None

    def perform_dialogue_planner(self):
        print("hello at perform dialogue planner")

        pass


