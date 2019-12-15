from . import *
from src.knowledgeacquisition.followup import SuggestingDialogueTemplate

# from src.models.dialogue import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate


#list of all dialogue moves
from ... import CURR_ORSEN_VERSION, ORSEN, ORSEN2, EDEN

"""ORSEN"""
ORSEN_RAND_DIALOGUE_LIST = [FeedbackDialogueTemplate(),
                 PromptDialogueTemplate(),
                 PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate(),
                 SuggestingDialogueTemplate()] ###Suggesting is same as hinting in ORSEN2 context

"""ORSEN 2"""
ORSEN2_RAND_DIALOGUE_LIST = [FeedbackDialogueTemplate(),
                 PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate(),
                 HintingDialogueTemplate(),
                 SuggestingDialogueTemplate()]

"""EDEN"""
EDEN_RAND_DIALOGUE_LIST = [PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate()
                 ]

EDEN_DIALOGUE_LIST = [CPumpingDialogueTemplate(),
                      DCorrectingDialogueTemplate(),
                      DPraiseDialogueTemplate(),
                      DPumpingDialogueTemplate(),
                      ELabelDialogueTemplate(),
                      EvaluationDialogueTemplate(),
                      RecollectionDialogueTemplate(),
                      EEndDialogueTemplate(),
                      EEmphasisDialogueTemplate()]

"""DEFAULT IS ORSEN"""
if CURR_ORSEN_VERSION == ORSEN:
    DIALOGUE_LIST = ORSEN_RAND_DIALOGUE_LIST
elif CURR_ORSEN_VERSION == ORSEN2:
    DIALOGUE_LIST = ORSEN2_RAND_DIALOGUE_LIST
elif CURR_ORSEN_VERSION == EDEN:
    DIALOGUE_LIST = EDEN_RAND_DIALOGUE_LIST
else:
    DIALOGUE_LIST = ORSEN_RAND_DIALOGUE_LIST



