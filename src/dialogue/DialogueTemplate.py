import abc
from abc import ABC, abstractmethod

class DialogueTemplate(ABC):

   def __init__(self, id = -1, dialogue_type = [], template = [], relation = [], blanks = [], nodes = [], dependent_nodes = []):

      self.id = id
      self.dialogue_type = dialogue_type
      self.template = template
      self.relation = relation
      self.blanks = blanks
      self.nodes = nodes
      self.dependent_nodes = dependent_nodes

      # TODO implement this

   @staticmethod
   def build(id = -1, dialogue_type = "", template_string = "", relation_string = "", blank_string = "", nodes_string = "", dependent_nodes_string = ""):

      templates = str(template_string).split("_")
      relations_split = str(relation_string).split(",")

      relations = [r.strip().split(" ") for r in relations_split]

      blanks = str(blank_string).split(",")
      nodes = str(nodes_string).split(",")
      dependent_nodes = str(dependent_nodes_string).split(",")

      return DialogueTemplate(id, dialogue_type, templates, relations, blanks, nodes, dependent_nodes)

   def get_string_response(self):
      return "".join(self.template)

   def __str__(self):
      str = "(%s) %s" % (self.dialogue_type, self.get_string_response())
      return str