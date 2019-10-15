from . import *
from src.knowledgeacquisition.followup import SuggestingDialogueTemplate

# from src.models.dialogue import FeedbackDialogueTemplate, HintingDialogueTemplate, PromptDialogueTemplate, PumpingGeneralDialogueTemplate, PumpingSpecificDialogueTemplate


#list of all dialogue moves
"""ORSEN"""
# DIALOGUE_LIST = [FeedbackDialogueTemplate(),
#                  PromptDialogueTemplate(),
#                  PumpingGeneralDialogueTemplate(),
#                  PumpingSpecificDialogueTemplate()]

"""ORSEN 2"""
# DIALOGUE_LIST = [FeedbackDialogueTemplate(),
#                  PumpingGeneralDialogueTemplate(),
#                  PumpingSpecificDialogueTemplate(),
#                  HintingDialogueTemplate(),
#                  SuggestingDialogueTemplate()]

"""EDEN"""
DIALOGUE_LIST = [PumpingGeneralDialogueTemplate()]

EDEN_DIALOGUE_LIST = [CPumpingDialogueTemplate(),
                      DCorrectingDialogueTemplate(),
                      DPraiseDialogueTemplate(),
                      DPumpingDialogueTemplate(),
                      ELabelDialogueTemplate(),
                      EvaluationDialogueTemplate(),
                      RecollectionDialogueTemplate(),
                      EEndDialogueTemplate()]