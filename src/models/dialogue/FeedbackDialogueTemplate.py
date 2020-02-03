from src import DialogueTemplateBuilder
from . import DialogueTemplate
from src.constants import DIALOGUE_TYPE_FEEDBACK, EVENT_ACTION, EVENT_CREATION, EVENT_DESCRIPTION
import copy
from src.Logger import Logger


class FeedbackDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_FEEDBACK, template, relation, blanks, nodes, dependent_nodes);


    def fill_blanks(self, event):
        print(self.full_string())

        # response = self.template
        # response = DialogueTemplateBuilder.build(*self)
        response = copy.deepcopy(self.template)

        for i in range (len(self.nodes)):
            to_insert = ""
            curr_index = response.index(self.nodes[i])
            Logger.log_dialogue_model_basic("Current Blank: " + self.blanks[i])

            if self.blanks[i] == 'Repeat':
                to_insert = self.check_subject(event.subject.name) + " "
                # to_insert = event.subject.name + " "
                if event.get_type() == EVENT_ACTION:
                    to_insert = to_insert + str(event.verb)
                    Logger.log_dialogue_model_basic(str(to_insert + str(event.verb)))
                elif event.get_type() == EVENT_CREATION:
                    to_insert = event.subject.name
                    Logger.log_dialogue_model_basic(str(event.subject.name))
                elif event.get_type() == EVENT_DESCRIPTION:
                    #Iterate through attributes
                    for X in event.attributes:
                        to_insert = to_insert + X.keyword + " " + str(X.description.lemma_)
                        Logger.log_dialogue_model_basic(str(to_insert + X.keyword + " " + str(X.description.lemma_)))
            response[curr_index] = to_insert
        return response

    def get_usable_templates(self):
        # check if it has usable templates
        return []

    def get_template_to_use(self):
        # check if it has usable templates
        return []
