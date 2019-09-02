from . import DialogueTemplate
from .constants import DIALOGUE_TYPE_PROMPT

class PromptDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_PROMPT, template, relation, blanks, nodes, dependent_nodes);

    def fill_blank(self, fill):
        for i in range(len(self.template)):
            for j in range(len(self.nodes)):
                if self.template[i] == self.node[j]:
                    self.template[i] = fill
                    break
