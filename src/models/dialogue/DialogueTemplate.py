import abc
from abc import ABC, abstractmethod

from src.models.dialogue.constants import *
# from src.models.dialogue import PromptDialogueTemplate, PumpingGeneralDialogueTemplate, InputMisheardDialogueTemplate, UnknownDialogueTemplate
from src.models.dialogue import UnknownDialogueTemplate

class DialogueTemplate(ABC):
   __metaclass__ = abc.ABCMeta

   def __init__(self, id = -1, dialogue_type = '', template = [], relation = [], blanks = [], nodes = [], dependent_nodes = []):
      super().__init__()

      self.id = id
      self.dialogue_type = dialogue_type
      self.template = template
      self.relation = relation
      self.blanks = blanks
      self.nodes = nodes
      self.dependent_nodes = dependent_nodes

   @staticmethod
   def build(id = -1, dialogue_type = "", template_string = "", relation_string = "", blank_string = "", nodes_string = "", dependent_nodes_string = ""):

      templates = str(template_string).split("_")

      relations_split = str(relation_string).split(",")
      relations = [r.strip().split(" ") for r in relations_split]

      blanks = str(blank_string).split(",")
      nodes = str(nodes_string).split(",")
      dependent_nodes = str(dependent_nodes_string).split(",")

      # if dialogue_type == DIALOGUE_TYPE_PROMPT:
      #    return PromptDialogueTemplate(id, dialogue_type, templates, relations, blanks, nodes, dependent_nodes)
      # elif dialogue_type == DIALOGUE_TYPE_PUMPING_GENERAL:
      #    return PumpingGeneralDialogueTemplate(id, dialogue_type, templates, relations, blanks, nodes, dependent_nodes)
      # elif dialogue_type == DIALOGUE_TYPE_INPUT_MISHEARD:
      #    return InputMisheardDialogueTemplate(id, dialogue_type, templates, relations, blanks, nodes, dependent_nodes)
      # else:
      #    return UnknownDialogueTemplate(id, DIALOGUE_TYPE_UNKNOWN, templates, relations, blanks, nodes, dependent_nodes)
      return UnknownDialogueTemplate(id, templates, relations, blanks, nodes, dependent_nodes)

   def fill_blanks(self, details=[]):
      pass

   def get_string_response(self):
      return "".join(self.template)

   def __str__(self):
      str = "(%s) %s" % (self.dialogue_type, self.get_string_response())
      return str

   def get_type(self):
      return self.dialogue_type