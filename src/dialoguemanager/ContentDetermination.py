import numpy as np
from src.models.dialogue.constants import *

from src.dbo.dialogue.DBODialogueTemplate import DBODialogueTemplate
import random


class ContentDetermination:

    def __init__(self):
        super().__init__()
        self.move_to_execute = ""
        self.curr_event = []

    def set_state(self, move_to_execute, curr_event, usable_template_list):
        self.move_to_execute = move_to_execute
        self.curr_event = curr_event
        self.usable_template_list = usable_template_list

    def reset_state(self):
        self.move_to_execute = ""
        self.curr_event = []
        self.usable_template_list = []

    def perform_content_determination(self):
        print("FETCHING: ", self.move_to_execute)

        #choose template
        chosen_template = self.choose_template()
        print("CHOSEN TEMPLATE IS: ", chosen_template)

        #fill template to use
        if len(chosen_template.template) == 1:
            response = chosen_template.template[0]
        else:
            response = chosen_template.fill_blanks(self.curr_event)

        if type(response) is not type("dump"):
            str_response = ' '.join(response)
            # TODO replace multiple occurences of spaces with only one space.
        else:
            str_response = response
        print("RESPONSE IS: ", str_response)

        self.reset_state()
        return str_response

    # def get_usable_templates(self):
    #     usable_template_list = []
    #     dialogue_template = DBODialogueTemplate('templates')
    #     # dialogue_template.get_templates_of_type()
    #
    #     template_list = dialogue_template.get_templates_of_type(self.move_to_execute)
    #
    #     # check which template is usable
    #     for X in template_list:
    #         print("==============================")
    #         print("TEMPLATE: ", X)
    #         print("==============================")
    #         print("Relation: ", X.relation)
    #         print("Template: ", X.template)
    #         print("Relations: ", X.relation)
    #         print("Blanks: ", X.blanks)
    #         print("Nodes: ", X.nodes)
    #         print("Dependent Nodes: ", X.dependent_nodes)
    #         result = X.is_usable(self.curr_event)
    #         print("Is it usable? ", result)
    #         if X.is_usable(self.curr_event):
    #             usable_template_list.append(X)
    #         print("\n")
    #
    #     return usable_template_list

    def choose_template(self):
        return random.choice(self.usable_template_list)



