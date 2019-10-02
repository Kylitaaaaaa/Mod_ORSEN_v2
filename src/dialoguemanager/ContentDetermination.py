import numpy as np
from src.models.dialogue.constants import *

from src.dbo.dialogue.DBODialogueTemplate import DBODialogueTemplate


class ContentDetermination:
    move_to_execute = ""

    def __init__(self, move_to_execute):
        super().__init__()
        self.move_to_execute = move_to_execute

    def perform_content_determination(self):
        print("trying to get: ", self.move_to_execute)
        self.get_templates()
        pass

    def get_templates(self):
        dialogue_template = DBODialogueTemplate('templates')
        # dialogue_template.get_templates_of_type()

        template_list = dialogue_template.get_templates_of_type(self.move_to_execute)
        print("Here are the templates for ", self.move_to_execute)
        for X in template_list:
            # print(X.dialogue_type())
            print(X)
        print("Done Printing")