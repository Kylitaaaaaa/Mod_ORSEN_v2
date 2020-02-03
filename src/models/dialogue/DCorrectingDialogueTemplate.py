from . import DialogueTemplate
from src.constants import *
import copy


class DCorrectingDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_D_CORRECTING, template, relation, blanks, nodes,
                                  dependent_nodes);

    def get_template_to_use(self):
        # check if it has usable templates
        #        return []
        pass

    def fill_blanks(self, curr_emotion_event):
        response = copy.deepcopy(self.template)

        for i in range(len(self.nodes)):
            to_insert = ""
            curr_index = response.index(self.nodes[i])
            if self.blanks[i] == 'Character':
                to_insert = self.check_subject(curr_emotion_event.event.get_characters_involved()[0].name)

            response[curr_index] = to_insert
        return response


