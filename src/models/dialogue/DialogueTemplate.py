import abc
from abc import ABC, abstractmethod


class DialogueTemplate(ABC):
    __metaclass__ = abc.ABCMeta

    def __init__(self, id=-1, dialogue_type='', template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
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

    def is_usable(self, curr_event):
        print('CHECKING IS USABLE: ', len(curr_event))
        # Requires a relation
        if self.relation[0][0] == 'None':
            return True
        else:
            if len(curr_event) == 0:
                return False
            else:
                # check relations one by one
                for i in range(len(self.relation)):
                    print("i: ", self.relation[i])
                return True

        return True

    @staticmethod
    @abstractmethod
    def get_template_to_use(self):
        # check if it has usable templates
        return []
