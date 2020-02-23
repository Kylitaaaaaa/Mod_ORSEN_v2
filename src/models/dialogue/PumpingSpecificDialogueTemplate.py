from . import DialogueTemplate
from src.Logger import Logger
from src.constants import DIALOGUE_TYPE_PUMPING_SPECIFIC, EVENT_ACTION, EVENT_CREATION, EVENT_DESCRIPTION


class PumpingSpecificDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_PUMPING_SPECIFIC, template, relation, blanks, nodes, dependent_nodes);

    def fill_blanks(self, event):

        response = self.template
        for i in range (len(self.nodes)):
            to_insert = ""
            curr_index = response.index(self.nodes[i])
            Logger.log_dialogue_model_basic("Current Blank: " + self.blanks[i])
            
            if self.blanks[i] == 'Character':
                to_insert = self.check_subject(event.get_characters_involved()[0].name)
                # if event.get_characters_involved()[0].name.lower() == 'i':
                #     to_insert = 'you'
                # else:
                #     to_insert = event.get_characters_involved()[0].name
            elif self.blanks[i] == 'Object' or self.blanks[i] == 'Item':
                to_insert = event.get_objects_involved()[0].name
                Logger.log_dialogue_model_basic(str(event.get_objects_involved()[0].name))
            elif self.blanks[i] == 'Event':
                to_insert = self.check_subject(event.subject.name) + " " + str(event.verb.lemma_)
                # to_insert = event.subject.name + " " + str(event.verb.lemma_)
            elif self.blanks[i] == 'Repeat':
                to_insert = self.check_subject(event.subject.name) + " "
                # to_insert = event.subject.name + " "
                if event.get_type() == EVENT_ACTION:
                    to_insert = to_insert + str(event.verb)
                elif event.get_type() == EVENT_CREATION:
                    to_insert = event.subject.name
                elif event.get_type() == EVENT_DESCRIPTION:
                    #Iterate through attributes
                    for X in event.attributes:
                        to_insert = to_insert + X.keyword + " " + str(X.description.lemma_)
           
            response[curr_index] = to_insert

        return response

    def get_template_to_use(self):
        # check if it has usable templates
        return []
