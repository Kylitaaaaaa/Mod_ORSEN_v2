from src.knowledgeacquisition.followup import FollowUpDialogueTemplate
from src.constants import DIALOGUE_TYPE_FOLLOW_UP


class FollowUpAskDialogueTemplate(FollowUpDialogueTemplate):

    def __init__(self, id=-1, template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        FollowUpDialogueTemplate.__init__(self, id, DIALOGUE_TYPE_FOLLOW_UP, template, relation, blanks, nodes, dependent_nodes);

    def fill_blank(self, fill):
        # TODO fix fill_blank implementation

        pass
