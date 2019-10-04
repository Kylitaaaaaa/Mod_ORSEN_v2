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