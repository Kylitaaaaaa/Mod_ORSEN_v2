from src.models.elements import Attribute
from src.models.pickles.PickleObject import PickleObject
from . import Event
from src.constants import EVENT_DESCRIPTION, IS_A


class DescriptionEvent(Event):

    attributes = [] #Attribute object

    def __init__(self, sequence_number, subject, attributes):
        super().__init__(sequence_number, EVENT_DESCRIPTION, subject)

        if type(attributes) == Attribute:
            attributes = [attributes]
        self.attributes = attributes

        for a in attributes:
            subject.attribute.append(a)
            if a.relation == IS_A:
                subject.type.append(a)

    def get_attributes(self):
        return self.attributes

    def print_basic(self):
        my_string = ""
        my_string = my_string + str(self.subject.name) + " [ "
        for a in self.attributes:
            my_string = my_string + str(a.relation) + ">" + str(a.description) + "(" + str(a.is_negated) + ") "
        my_string = my_string + "]"
        return my_string

    def __str__(self):
        my_string = "" \
                    "============================\n" \
                    "= EVENT " + str(self.sequence_number) + "\t============\n" \
                    "============================\n" \
                    "Type: Description Event\n" \
                    "Subject: " + str(self.subject) + "\n" + \
                    "Attributes: \n"

        if type(self.attributes) == Attribute:
            my_string = my_string + "\t" + str(self.attributes)
        else:
            for a in self.attributes:
                my_string = my_string + str(a)

        return my_string.strip()

    def __eq__(self, other):
        if self.subject == other.subject:
            if len(self.attributes) == len(other.attributes):
                for i in range(len(self.attributes)):
                   if self.attributes[i] != other.attributes[i]:
                       return False
                return True
        return False

    def get_pickled_event(self):
        pickled_event = PickleObject()
        pickled_event.type = self.type
        pickled_event.sequence_number = self.sequence_number
        pickled_event.subject = self.get_pickled_char_obj(self.subject)

        pickled_event.attributes = []
        for X in self.attributes:
            pickled_event.attributes.append(X.get_pickled_atribute())

        return pickled_event