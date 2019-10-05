from . import DialogueTemplate
from src.constants import DIALOGUE_TYPE_PUMPING_SPECIFIC


class PumpingSpecificDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_PUMPING_SPECIFIC, template, relation, blanks, nodes, dependent_nodes);

    def fill_blanks(self, event):

        print("subject name: ", event.subject.name)
        print("subject: ", event.subject)
        response = self.template
        for i in range (len(self.nodes)):
            to_insert = ""
            curr_index = response.index(self.nodes[i])
            if self.blanks[i] == 'Character':
                to_insert = event.get_characters_involved()[0].name
            elif self.blanks[i] == 'Object':
                to_insert = event.get_objects_involved()[0].name
            elif self.blanks[i] == 'Event':
                to_insert = event.subject.name + " " + str(event.verb.lemma_)
           
            response[curr_index] = to_insert

        return response

    def get_template_to_use(self):
        # check if it has usable templates
        return []
