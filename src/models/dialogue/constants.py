from . import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate
from src.knowledgeacquisition.followup import SuggestingDialogueTemplate

# from src.models.dialogue import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate


#list of all dialogue moves
# DIALOGUE_LIST = [FeedbackDialogueTemplate(),
#                  PromptDialogueTemplate(),
#                  PumpingGeneralDialogueTemplate(),
#                  PumpingSpecificDialogueTemplate()]

DIALOGUE_LIST = [FeedbackDialogueTemplate(),
                 PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate(),
                 HintingDialogueTemplate(),
                 SuggestingDialogueTemplate()]
