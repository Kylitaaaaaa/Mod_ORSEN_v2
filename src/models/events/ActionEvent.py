from . import Event
from .constants import EVENT_ACTION

class ActionEvent(Event):

    verb = ""
    direct_object = None #Object/Character object
    adverb = ""
    preposition = ""
    object_of_preposition = ""

    def __init__(self, sequence_number, subject, verb, direct_object, adverb, preposition, object_of_preposition):
        super().__init__(sequence_number, EVENT_ACTION, subject)
        self.verb = verb
        self.direct_object = direct_object
        self.adverb = adverb
        self.preposition = preposition
        self.object_of_preposition = object_of_preposition

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

    def __str__(self):
        subject_string = "\tSubject = [ "
        for object in self.subject:
            subject_string += object + ","
        subject_string += " ]\n"

        string = "EVENT #" + str(self.sequence_no) + " - "

        string += "ACTION EVENT\n"
        string += subject_string
        string += "\tD.O. = [ "
        for object in self.direct_object:
            string += object + ","
        string += " ]\n"
        string += "\tI.O. = [ "
        for object in self.indirect_object:
            string += object + ","
        string += " ]\n"
        if self.action != "":
            string += "\tVERB = " + self.action + "\n"
        if self.preposition != "":
            string += "\tPREP = " + self.preposition + "\n"
        if self.obj_of_preposition is not None:
            string += "\tOBJ PREP = " + self.obj_of_preposition + "\n"
        if self.adverb != "":
            string += "\tADVERB = " + self.adverb + "\n"
