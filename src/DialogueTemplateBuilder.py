from src.knowledgeacquisition.followup import *
from src.models.dialogue import *
from src.constants import *
from src.models.dialogue.EFollowupDialogueTemplate import EFollowupDialogueTemplate


class DialogueTemplateBuilder:

   @staticmethod
   def build(id = -1, dialogue_type = "", template_string = "", relation_string = "", blank_string = "", nodes_string = "", dependent_nodes_string = ""):

      templates = str(template_string).split("_")

      relations_split = str(relation_string).split(",")
      relations = [r.strip().split(" ") for r in relations_split]

      blanks = str(blank_string).split(",")
      nodes = str(nodes_string).split(",")
      dependent_nodes = str(dependent_nodes_string).split(",")



      if dialogue_type == DIALOGUE_TYPE_PROMPT:
         return PromptDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_PUMPING_GENERAL:
         return PumpingGeneralDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)

      elif dialogue_type == DIALOGUE_TYPE_FEEDBACK:
         return FeedbackDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)

      elif dialogue_type == DIALOGUE_TYPE_HINTING:
         return HintingDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)

      elif dialogue_type == DIALOGUE_TYPE_SUGGESTING:
         return SuggestingDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)

      elif dialogue_type == DIALOGUE_TYPE_PUMPING_SPECIFIC:
         return PumpingSpecificDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
    
      elif dialogue_type == DIALOGUE_TYPE_FOLLOW_UP:
         return FollowUpDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
    
      #TODO: Add the suggestion_affirm here
        
      elif dialogue_type == DIALOGUE_TYPE_KNOWLEDGE_ACQUISITION_PUMPING:
         return KnowledgeAcquisitionPumpingDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)


      elif dialogue_type == DIALOGUE_TYPE_INPUT_MISHEARD:
         return InputMisheardDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)


      elif dialogue_type == DIALOGUE_TYPE_C_PUMPING:
         return CPumpingDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_D_CORRECTING:
         return DCorrectingDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_D_PRAISE:
         return DPraiseDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_D_PUMPING:
         return DPumpingDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_E_LABEL:
         return ELabelDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_E_PUMPING:
         return EPumpingDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_EVALUATION:
         return EvaluationDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_RECOLLECTION:
         return RecollectionDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_E_END:
         return EEndDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_E_EMPHASIS:
         return EEmphasisDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
      elif dialogue_type == DIALOGUE_TYPE_E_FOLLOWUP:
         return EFollowupDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)

      ##WELCOME MESSAGE
      elif dialogue_type == DIALOGUE_TYPE_EDEN_WELCOME:
         return EDENWelcomeDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)
        
      elif dialogue_type == DIALOGUE_TYPE_ORSEN_WELCOME:
         return ORSENWelcomeDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)

      else:
         return UnknownDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)