from src.models.dialogue import DialogueTemplate
from src.constants import DIALOGUE_TYPE_SUGGESTING
from src.Logger import Logger

import copy


class SuggestingDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_SUGGESTING, template, relation, blanks, nodes, dependent_nodes);

    def fill_blanks(self, fill):
        response = copy.deepcopy(self.template)

        for i in range(len(self.dependent_nodes)):
            to_insert = ""
            Logger.log_dialogue_model_basic("Current Blank: " + self.blanks[i])

            print(self.relation[i])

            if self.dependent_nodes[i] is not None:
                curr_index = response.index(self.dependent_nodes[i])
                if self.blanks[i] == 'Object' or self.blanks[i] == 'Character':
                    to_insert = self.relations_blanks[0][i].name
                    Logger.log_dialogue_model_basic(str(self.relations_blanks[0][i].name))
                elif self.blanks[i] == 'IsA':
                    to_insert = self.relations_blanks[0][i].first
                    Logger.log_dialogue_model_basic(str(self.relations_blanks[0][i].first))

                # <2 UsedFor 3>
                elif int(self.relation[i][0]) < int(self.relation[i][2]):
                    to_insert = self.relations_blanks[0][i].second
                    Logger.log_dialogue_model_basic(str(self.relations_blanks[0][i].second))

                # <3 CreatedBy 2>
                else:
                    to_insert = self.relations_blanks[0][i].first
                    Logger.log_dialogue_model_basic(str(self.relations_blanks[0][i].first))
                

                response[curr_index] = to_insert

        return response

    def get_template_to_use(self):
        # check if it has usable templates
        return []
