from . import DialogueTemplate
from src.constants import DIALOGUE_TYPE_PROMPT

from src.dbo.concept import *
import copy
from src.Logger import Logger



class PromptDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_PROMPT, template, relation, blanks, nodes, dependent_nodes);

    def fill_blanks(self, fill):
        dBOConceptGlobalImpl = DBOConceptGlobalImpl()

        rand_concept = dBOConceptGlobalImpl.get_random_concept()

        response = copy.deepcopy(self.template)
        for i in range (len(self.nodes)):
            to_insert = rand_concept.first
            Logger.log_dialogue_model_basic(str(to_insert))
            curr_index = response.index(self.nodes[i])
            response[curr_index] = to_insert

        return response

    def get_template_to_use(self):
        # check if it has usable templates
        return []
