import abc
from abc import ABC


class DialogueTemplate(ABC):
   __metaclass__ = abc.ABCMeta

   def __init__(self, id = -1, dialogue_type = '', template = [], relation = [], blanks = [], nodes = [], dependent_nodes = []):
      self.id = id
      self.dialogue_type = dialogue_type
      self.template = template
      self.relation = relation
      self.blanks = blanks
      self.nodes = nodes
      self.dependent_nodes = dependent_nodes

   def fill_blanks(self, details=[]):
      pass

   def get_string_response(self):
      return "".join(self.template)

   def __str__(self):
      str = "(%s) %s" % (self.dialogue_type, self.get_string_response())
      return str

   def get_type(self):
      return self.dialogue_type