from . import Event
from src.constants import EVENT_CREATION

class CreationEvent(Event):

    def __init__(self, sequence_number, subject):
        super().__init__(sequence_number, EVENT_CREATION, subject)

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