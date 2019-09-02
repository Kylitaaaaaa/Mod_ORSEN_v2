from src.models.dialogue import DialogueTemplate
from src.models.dialogue.constants import DIALOGUE_TYPE_FOLLOW_UP_UNKNOWN


class FollowUpDialogueTemplate():

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_FOLLOW_UP_UNKNOWN, template, relation, blanks, nodes, dependent_nodes);

    def fill_blank(self, fill):
        # TODO fix fill_blank implementation

        pass
