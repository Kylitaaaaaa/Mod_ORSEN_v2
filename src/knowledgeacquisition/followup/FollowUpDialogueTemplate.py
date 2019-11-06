from abc import ABC

from src import DIALOGUE_TYPE_FOLLOW_UP
from src.models.dialogue import DialogueTemplate


class FollowUpDialogueTemplate(DialogueTemplate, ABC):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_FOLLOW_UP, template, relation, blanks, nodes, dependent_nodes);
    
    def get_template_to_use(self):
        # check if it has usable templates
        # return []
        pass

    def fill_blanks(self, fill):
        # TODO fix fill_blank implementation
        return self.template
        #pass
