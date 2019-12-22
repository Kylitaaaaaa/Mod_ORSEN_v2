from src.models.dialogue import DialogueTemplate
from src.constants import DIALOGUE_TYPE_SUGGESTING
import copy


class SuggestingDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_SUGGESTING, template, relation, blanks, nodes, dependent_nodes);

    def fill_blank(self, fill):
        response = copy.deepcopy(self.template)

        for i in range(len(self.dependent_nodes)):
            to_insert = ""
            if self.dependent_nodes[i] is not None:
                curr_index = response.index(self.dependent_nodes[i])
                if self.blanks[i] == 'Object' or 'Character':
                    to_insert = self.relations_blanks[i].name
                else:
                    to_insert = self.relations_blanks[i].first

                response[curr_index] = to_insert
        response.insert(0, "What if ")
        return response

    def get_template_to_use(self):
        # check if it has usable templates
        return []
