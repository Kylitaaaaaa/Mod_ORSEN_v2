from . import DialogueTemplate
from src.constants import DIALOGUE_TYPE_FEEDBACK, EVENT_ACTION, EVENT_CREATION, EVENT_DESCRIPTION


class FeedbackDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_FEEDBACK, template, relation, blanks, nodes, dependent_nodes);


    def fill_blanks(self, event):
        print("EVENT ATTRIBUTES")
        print(event.attributes)
        

        print("subject name: ", event.subject.name)
        print("subject: ", event.subject)
        response = self.template
        for i in range (len(self.nodes)):
            to_insert = ""
            curr_index = response.index(self.nodes[i])
            if self.blanks[i] == 'Repeat':
                if event.get_type() == EVENT_ACTION:
                    to_insert = event.subject.name + " " + event.verb + " " +  event.direct_object.name + " " +  event.adverb + " " +  event.preposition + " " +  event.object_of_preposition
                elif event.get_type() == EVENT_CREATION:
                    to_insert = event.subject.name
                elif event.get_type() == EVENT_DESCRIPTION:
                    to_insert = event.subject.name + " is "
                    # for j in range (len(event.get_attributes())):
                    #     if j == len(event.get_attributes()) - 1:
                    #         to_insert = to_insert
                    #     else:
                    #         to_insert = to_insert + " and "

            response[curr_index] = to_insert

        return response

    def get_usable_templates(self):
        # check if it has usable templates
        return []

    def get_template_to_use(self):
        # check if it has usable templates
        return []

    # def is_usable(self, to_check=[]):
    #     pass
