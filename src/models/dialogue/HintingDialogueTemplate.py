from . import DialogueTemplate
from src.constants import DIALOGUE_TYPE_HINTING
import copy
from src.Logger import Logger


class HintingDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_HINTING, template, relation, blanks, nodes, dependent_nodes);

    def fill_blanks(self, fill):
        response = copy.deepcopy(self.template)

        print("inside fill_blank()")
        print("id", self.id)
        print("tp", self.template)
        print("rl", self.relation)
        print("dn", self.dependent_nodes)
    
        for i in range(len(self.dependent_nodes)):
            to_insert = ""
            Logger.log_dialogue_model_basic("Current Blank: " + self.blanks[i])

            if self.dependent_nodes[i] is not None:
                curr_index = response.index(self.dependent_nodes[i])
                if self.blanks[i] == 'Object' or self.blanks[i] == 'Character':
                    to_insert = self.relations_blanks[0][i].name
                    Logger.log_dialogue_model_basic(str(self.relations_blanks[0][i].name))
                elif self.blanks[i] == 'IsA':
                    to_insert = self.relations_blanks[0][i].first
                    Logger.log_dialogue_model_basic(str(self.relations_blanks[0][i].first))
                else:
                    to_insert = self.relations_blanks[0][i].second
                    Logger.log_dialogue_model_basic(str(self.relations_blanks[0][i].second))
                response[curr_index] = to_insert
            
            print("iteration", i, "of", range(len(self.dependent_nodes)))
            print("\t", response)

        return response

    def get_template_to_use(self):
        # check if it has usable templates
        return []
