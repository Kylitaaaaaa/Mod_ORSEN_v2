from src.models.elements import Character, Object
from src.models.pickles.PickleObject import PickleObject
from . import Event
from src.constants import EVENT_ACTION

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

    # def get_verb(self):
    #     return self.verb
    #
    # def get_direct_object(self):
    #     return self.direct_object
    #
    # def get_adverb(self):
    #     return self.adverb
    #
    # def get_preposition(self):
    #     return self.preposition
    #
    # def get_object_of_preposition(self):
    #     return self.object_of_preposition

    def get_characters_involved(self):
        characters = []

        if type(self.subject) == Character:
            characters.append(self.subject)
        if type(self.direct_object) == Character:
            characters.append(self.direct_object)
        if type(self.object_of_preposition) == Character:
            characters.append(self.object_of_preposition)

        return characters

    def get_objects_involved(self):
        objects = []

        if type(self.subject) == Object:
            objects.append(self.subject)
        if type(self.direct_object) == Object:
            objects.append(self.direct_object)
        if type(self.object_of_preposition) == Object:
            objects.append(self.object_of_preposition)

        return objects

    def print_basic(self):
        my_string = ""
        my_string = my_string + str(self.subject.name) + ", "
        my_string = my_string + str(self.verb)

        if self.direct_object is not None:
            if str(self.direct_object.name).strip() is not "":
                my_string = my_string + ", " + str(self.direct_object.name)

        if self.adverb is not None:
            if str(self.adverb).strip() is not "":
                my_string = my_string + ", " + str(self.adverb)

        if self.preposition is not None:
            if str(self.preposition).strip() is not "":
                my_string = my_string + ", " + str(self.preposition)

        if self.object_of_preposition is not None:
            if str(self.object_of_preposition).strip() is not "":
                my_string = my_string + ", " + str(self.object_of_preposition)

        return my_string

    def __str__(self):
        my_string = "" \
                    "============================\n" \
                    "= EVENT " + str(self.sequence_number) + "\t============\n" \
                    "============================\n" \
                    "Type: Action Event\n" \
                    "Subject: " + str(self.subject) + "\n" + \
                    "Action : " + str(self.verb) + "\n" + \
                    "D.O.   : " + str(self.direct_object) + "\n" + \
                    "Adverb : " + str(self.adverb) + "\n" + \
                    "Prep   : " + str(self.preposition) + "\n" + \
                    "ObjPrep: " + str(self.object_of_preposition) + "\n"

        return my_string.strip()


# def __str__(self):
        # subject_string = "\tSubject = [ "
        # for object in self.subject:
        #     subject_string += object + ","
        # subject_string += " ]\n"
        #
        # string = "EVENT #" + str(self.sequence_no) + " - "
        #
        # string += "ACTION EVENT\n"
        # string += subject_string
        # string += "\tD.O. = [ "
        # for object in self.direct_object:
        #     string += object + ","
        # string += " ]\n"
        # string += "\tI.O. = [ "
        # for object in self.indirect_object:
        #     string += object + ","
        # string += " ]\n"
        # if self.action != "":
        #     string += "\tVERB = " + self.action + "\n"
        # if self.preposition != "":
        #     string += "\tPREP = " + self.preposition + "\n"
        # if self.obj_of_preposition is not None:
        #     string += "\tOBJ PREP = " + self.obj_of_preposition + "\n"
        # if self.adverb != "":
        #     string += "\tADVERB = " + self.adverb + "\n"

    def print_event(self):
        print("Subject: ", self.subject)
        print("Verb: ", self.verb)
        print("Direct Object: ", self.direct_object)
        print("Adverb: ", self.adverb)
        print("Preposition: ", self.preposition)
        print("Object of Preposition: ", self.object_of_preposition)

    def get_characters_involved(self):
        characters = []

        if type(self.subject) == Character:
            characters.append(self.subject)
        if type(self.direct_object) == Character:
            characters.append(self.direct_object)
        if type(self.object_of_preposition) == Character:
            characters.append(self.object_of_preposition)

        return characters

    def get_objects_involved(self):
        objects = []

        if type(self.subject) == Object:
            objects.append(self.subject)
        if type(self.direct_object) == Object:
            objects.append(self.direct_object)
        if type(self.object_of_preposition) == Object:
            objects.append(self.object_of_preposition)

        return objects

    def get_pickled_event(self):
        pickled_event = PickleObject()
        pickled_event.sequence_number = self.sequence_number
        pickled_event.type = self.type

        pickled_event.subject = self.get_pickled_char_obj(self.subject)
        pickled_event.direct_object = self.get_pickled_char_obj(self.direct_object)
        pickled_event.object_of_preposition = self.get_pickled_char_obj(self.object_of_preposition)

        pickled_event.verb = str(self.verb)
        pickled_event.adverb = str(self.adverb)
        pickled_event.preposition = str(self.preposition)

        return pickled_event