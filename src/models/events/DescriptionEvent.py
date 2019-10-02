from src.models import Attribute
from . import Event
from src.constants import  EVENT_DESCRIPTION

class DescriptionEvent(Event):

    attributes = [] #Attribute object

    def __init__(self, sequence_number, subject, attributes):
        super().__init__(sequence_number, EVENT_DESCRIPTION, subject)

        self.attributes = attributes

    def get_attributes(self):
        return self.attributes

    def __str__(self):
        my_string = "" \
                    "============================\n" \
                    "= EVENT " + str(self.sequence_number) + "\t================\n" \
                    "============================\n" \
                    "Subject: " + str(self.subject) + "\n" + \
                    "Attributes: \n"

        if type(self.attributes) == Attribute:
            my_string = my_string + "\t" + str(self.attributes)
        else:
            for a in self.attributes:
                my_string = my_string + str(a)

        return my_string.strip()
    # def __str__(self):
        # subject_string = "\tSubject = [ "
        # for object in self.subject:
        #     subject_string += object + ","
        # subject_string += " ]\n"
        #
        # string = "EVENT #" + str(self.sequence_no) + " - "
        #
        # string += "DESCRIPTIVE\n"
        # string += subject_string
        # string += "\tattributes = [ "
        # for attr in self.attributes:
        #     string += attr + ","
        # string += " ]\n"