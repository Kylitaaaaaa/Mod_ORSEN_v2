from src.models.pickles.PickleObject import PickleObject
from . import Event
from src.constants import EVENT_CREATION

class CreationEvent(Event):

    def __init__(self, sequence_number, subject, attributes=[]):
        super().__init__(sequence_number, EVENT_CREATION, subject)

    def __str__(self):
        my_string = "" \
                    "============================\n" \
                    "= EVENT " + str(self.sequence_number) + "\t============\n" \
                    "============================\n" \
                    "Type: Creation Event\n" \
                    "Subject: " + str(self.subject) + "\n"

        return my_string.strip()

    def print_basic(self):
        my_string = "Created new entity: " + str(self.subject)

        return my_string

    # def __str__(self):
        # subject_string = "\tSubject = [ "
        # for object in self.subject:
        #     subject_string += object + ","
        # subject_string += " ]\n"
        #
        # string = "EVENT #" + str(self.sequence_no) + " - "
        #
        # string += "CREATION\n"
        # string += subject_string
        # string += "\tattributes = [ "
        # for attr in self.attributes:
        #     string += attr + ","
        # string += " ]\n"

    def get_pickled_event(self):
        pickled_event = PickleObject()

        pickled_event.attributes = []
        for X in self.attributes:
            pickled_event.attributes.append(X.get_pickled_atribute())

        pickled_event.type = self.type
        pickled_event.sequence_number = self.sequence_number
        pickled_event.subject = self.get_pickled_char_obj(self.subject)

        return pickled_event