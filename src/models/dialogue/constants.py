from . import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate


#BASIC ORSEN
DIALOGUE_TYPE_FEEDBACK = "FEEDBACK"
DIALOGUE_TYPE_HINTING = "HINTING"
DIALOGUE_TYPE_PROMPT = "PROMPT"
DIALOGUE_TYPE_PUMPING_GENERAL = "PUMPING_GENERAL"
DIALOGUE_TYPE_PUMPING_SPECIFIC = "PUMPING_SPECIFIC"

#JUVEYANCE
DIALOGUE_TYPE_FOLLOW_UP_CONFIRM = "FOLLOW_UP_CONFIRM"
DIALOGUE_TYPE_FOLLOW_UP_ASK = "FOLLOW_UP_ASK"
DIALOGUE_TYPE_FOLLOW_UP_UNKNOWN = "FOLLOW_UP_???"
DIALOGUE_TYPE_SUGGESTING = "SUGGESTING"

DIALOGUE_TYPE_INPUT_MISHEARD = "INPUT_MISHEARD"
DIALOGUE_TYPE_UNKNOWN = "UNKNOWN"

#list of usable dialogue moves
DIALOGUE_LIST = [FeedbackDialogueTemplate(),
                 HintingDialogueTemplate(),
                 PromptDialogueTemplate(),
                 PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate()]
