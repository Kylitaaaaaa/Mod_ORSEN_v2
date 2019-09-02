from . import Event
from .constants import EVENT_CREATION

class CreationEvent(Event):

    attributes = [] #Attribute object

    def __init__(self, sequence_number, subject, attributes):
        super().__init__(sequence_number, EVENT_CREATION, subject)

        self.attributes = attributes

    def get_attributes(self):
        return self.attributes