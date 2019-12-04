from src.knowledgeacquisition.followup import KnowledgeAcquisitionPumpingDialogueTemplate
from src.models.dialogue import DialogueTemplate
from src.constants import DIALOGUE_TYPE_KNOWLEDGE_ACQUISITION_PUMPING
from src.Logger import Logger

class KnowledgeAcquisitionPumpingDialogueTemplate(DialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        DialogueTemplate.__init__(self, id, DIALOGUE_TYPE_KNOWLEDGE_ACQUISITION_PUMPING, template, relation, blanks, nodes, dependent_nodes);

    def fill_blanks(self, dialogue_history):
        print("KA STUFF")
        # for x in range(len(dialogue_history)):
        #     print(dialogue_history[x].dialogue_type)

        response = self.template
        if len(dialogue_history) < 3:
            return None
        else:
            print(dialogue_history[len(dialogue_history)-3].dialogue_type)
            suggestion_blanks = dialogue_history[len(dialogue_history)-3].word_relation

        subject = ""

        for x in range(len(suggestion_blanks)):
            print(suggestion_blanks[x])
            if suggestion_blanks[x].second_token == "character":
                if self.blanks[0] == 'Character':
                    subject = suggestion_blanks[x].first_token
            elif suggestion_blanks[x].second_token == "object":
                if self.blanks[0] == 'Object':
                    subject = suggestion_blanks[x].first_token
        
        Logger.log_dialogue_model_basic("Subject: " + subject)

        response = [x.replace("1", subject) for x in response]

        return response

    def get_template_to_use(self):
        # check if it has usable templates
        return []
    