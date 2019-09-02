from . import Event

class ActionEvent(Event):

    verb = ""
    direct_object = None #Object/Character object
    adverb = ""
    preposition = ""
    object_of_preposition = ""

    def __init__(self, sequence_number, type, subject, attributes):
        super().__init__(sequence_number, type, subject)

        self.attributes = attributes

    def get_verb(self):
        return self.verb

    def get_direct_object(self):
        return self.direct_object

    def get_adverb(self):
        return self.adverb

    def get_preposition(self):
        return self.preposition

    def get_object_of_preposition(self):
        return self.object_of_preposition