from . import DialogueTemplate
from .constants import DIALOGUE_TYPE_INPUT_MISHEARD


class InputMisheardDialogueTemplate(DialogueTemplate):
    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_INPUT_MISHEARD, template, relation, blanks, nodes, dependent_nodes);

    def fill_blanks(self, details=[]):
        # TODO fix fill_blank implementation

        pass