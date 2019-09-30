from . import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate

# from src.models.dialogue import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate


#list of all dialogue moves
DIALOGUE_LIST = [FeedbackDialogueTemplate(),
                 HintingDialogueTemplate(),
                 PromptDialogueTemplate(),
                 PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate()]
