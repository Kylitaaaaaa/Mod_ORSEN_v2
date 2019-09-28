from . import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate

#list of usable dialogue moves
DIALOGUE_LIST = [FeedbackDialogueTemplate(),
                 HintingDialogueTemplate(),
                 PromptDialogueTemplate(),
                 PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate()]
