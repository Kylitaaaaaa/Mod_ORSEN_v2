from src.models import World
from src.textunderstanding import InputDecoder
from src.constants import *
from . import Logger
from src.textunderstanding.InputDecoder import InputDecoder

class ORSEN:

    def __init___(self):
        super().__init__()
        self.turn_count = 1
        self.prereqs = []
        self.prereqs_pointer = [0, 0]
        self.world = World()

    def add_prereq(self, prereq):
        self.prereqs.append(prereq)

    def is_done_with_prereqs(self):
        return True

    def execute_text_understanding(self, input):
        result = InputDecoder.annotate_input(input)
        print("Printing result")
        print(result)

    def talk(self):
        if self.is_done_with_prereqs() == False:
            pass
            # TODO implement the modularization of pre-required dialogues
            # WHAT I'M THINKING IS GAWIN NATIN NA PARANG CLASS UGN MGA SHIT NA NILALAGAY BEFORE THE ACTUAL STORYTELLING THING
            # prereq_dialogue = self.prereqs[0]
            # prereq_dialogue.talk(prereq_dialogue[0])

        if self.is_story_done:
            pass
        else:
            result = None

    def is_end_story(self, response):
        if response == 'the end':
            return True
        return False

    def get_response(self, response):
        print("Response is: ", response)
        result = InputDecoder.get_instance().coref_resolve(response)
        print("returned response is: ", response)

        # if self.endstory:
        #     if (not self.endstorygen):
        #         if response.lower() in IS_AFFIRM:
        #             pass
        #         else:
        #             pass
        #     elif self.endstorygen:
        #         if response.lower() in IS_AFFIRM:
        #             pass
        #         else:
        #             pass
        # elif response.lower() in IS_END:
        #     pass
        # else:
        #     pass












