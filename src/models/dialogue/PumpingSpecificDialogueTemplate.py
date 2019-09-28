from . import DialogueTemplate
from src.constants import DIALOGUE_TYPE_PUMPING_SPECIFIC


class PromptDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_PUMPING_SPECIFIC, template, relation, blanks, nodes, dependent_nodes);

    def fill_blank(self, fill):
        # TODO fix fill_blank implementation

        for i in range(len(self.template)):
            for j in range(len(self.nodes)):
                if self.template[i] == self.node[j]:
                    self.template[i] = fill
                    break

    def is_usable(self, to_check=[]):
        # TODO fix fill_blank implementation
        pass
