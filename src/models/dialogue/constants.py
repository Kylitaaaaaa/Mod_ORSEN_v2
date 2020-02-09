from . import *
from src.constants import *
from src.knowledgeacquisition.followup import SuggestingDialogueTemplate

# from src.models.dialogue import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate


#list of all dialogue moves
"""ORSEN1"""
ORSEN1_DIALOGUE_LIST = [FeedbackDialogueTemplate(),
                 PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate(),
                 HintingDialogueTemplate()]

"""ORSEN 2"""
ORSEN2_DIALOGUE_LIST = [FeedbackDialogueTemplate(),
                 PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate(),
                 HintingDialogueTemplate(),
                 SuggestingDialogueTemplate()]

"""EDEN"""
# DIALOGUE_LIST = [PumpingGeneralDialogueTemplate(),
#                  CPumpingDialogueTemplate(),
#                  DCorrectingDialogueTemplate(),
#                  DPraiseDialogueTemplate(),
#                  EEmphasisDialogueTemplate(),
#                  DPumpingDialogueTemplate(),
#                  ELabelDialogueTemplate(),
#                  EvaluationDialogueTemplate(),
#                  RecollectionDialogueTemplate(),
#                  EEndDialogueTemplate()
#                  ]

DIALOGUE_LIST = [PumpingGeneralDialogueTemplate(),
                 PumpingSpecificDialogueTemplate()
#                  # CPumpingDialogueTemplate(),
#                  # DCorrectingDialogueTemplate(),
#                  # DPraiseDialogueTemplate(),
#                  # EEmphasisDialogueTemplate(),
#                  # DPumpingDialogueTemplate(),
#                  # ELabelDialogueTemplate(),
#                  # EvaluationDialogueTemplate(),
#                  # RecollectionDialogueTemplate(),
#                  # EEndDialogueTemplate()
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

if CURR_ORSEN_VERSION == ORSEN1:
    DIALOGUE_LIST = ORSEN1_DIALOGUE_LIST
elif CURR_ORSEN_VERSION == ORSEN2:
    DIALOGUE_LIST = ORSEN2_DIALOGUE_LIST
elif CURR_ORSEN_VERSION == EDEN:
    DIALOGUE_LIST = DIALOGUE_LIST