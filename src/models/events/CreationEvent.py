from . import Event

class CreationEvent(Event):

    attributes = [] #Attribute object

    def __init__(self, sequence_number, type, subject, attributes):
        super().__init__(sequence_number, type, subject)

        self.attributes = attributes

    def get_attributes(self):
        return self.attributes