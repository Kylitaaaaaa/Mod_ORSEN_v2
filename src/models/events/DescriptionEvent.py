from . import Event
from .constants import  EVENT_DESCRIPTION

class DescriptionEvent(Event):

    attributes = [] #Attribute object

    def __init__(self, sequence_number, subject, attributes):
        super().__init__(sequence_number, EVENT_DESCRIPTION, subject)

        self.attributes = attributes

    def get_attributes(self):
        return self.attributes