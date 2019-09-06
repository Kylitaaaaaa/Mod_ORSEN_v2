from . import Event
from .constants import EVENT_CREATION

class CreationEvent(Event):

    attributes = [] #Attribute object

    def __init__(self, sequence_number, subject, attributes):
        super().__init__(sequence_number, EVENT_CREATION, subject)

        self.attributes = attributes

    def get_attributes(self):
        return self.attributes

    def __str__(self):
        subject_string = "\tSubject = [ "
        for object in self.subject:
            subject_string += object + ","
        subject_string += " ]\n"

        string = "EVENT #" + str(self.sequence_no) + " - "

        string += "CREATION\n"
        string += subject_string
        string += "\tattributes = [ "
        for attr in self.attributes:
            string += attr + ","
        string += " ]\n"