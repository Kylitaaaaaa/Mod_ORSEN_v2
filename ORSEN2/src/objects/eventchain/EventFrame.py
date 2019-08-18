
FRAME_EVENT = 0
FRAME_DESCRIPTIVE = 1
FRAME_CREATION = 2

class EventFrame:

    event_type = -1
    # descriptive, action, etc.

    def __init__(self, seq_no=-1, event_type=-1):
        self.sequence_no        = seq_no
        self.event_type         = event_type

        self.subject = []
        if event_type == FRAME_EVENT:
            self.action = ""
            self.direct_object = []
            self.indirect_object = []
            self.preposition = ""
            self.obj_of_preposition = None
            self.adverb = ""
        elif event_type == FRAME_DESCRIPTIVE:
            self.attributes = []
        elif event_type == FRAME_CREATION:
            self.attributes = []

    def __str__(self):
        subject_string = "\tSubject = [ "
        for object in self.subject:
            subject_string += object + ","
        subject_string += " ]\n"

        string = "EVENT #" + str(self.sequence_no) + " - "
        if self.event_type == FRAME_EVENT:
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

        elif self.event_type == FRAME_DESCRIPTIVE:
            string += "DESCRIPTIVE\n"
            string += subject_string
            string += "\tattributes = [ "
            for attr in self.attributes:
                string += attr + ","
            string += " ]\n"

        elif self.event_type == FRAME_CREATION:
            string += "CREATION\n"
            string += subject_string
            string += "\tattributes = [ "
            for attr in self.attributes:
                string += attr + ","
            string += " ]\n"

        else:
            string += "UNKNOWN"
        return string

    def get_subject(self, index, world):
        chars = world.characters
        obj = world.objects

        if index > len(self.subject) - 1:
            return None

        if self.subject[index] in chars:
            return chars[self.subject[index]]

        if self.subject[index] in obj:
            return obj[self.subject[index]]

        return None

    def get_direct_object(self, index, world):
        chars = world.characters
        obj = world.objects

        if index > len(self.direct_object) - 1:
            return None

        if self.direct_object[index] in chars:
            return chars[self.direct_object[index]]

        if self.subject[index] in obj:
            return obj[self.direct_object[index]]

        return None

    def get_indirect_object(self, index, world):
        chars = world.characters
        obj = world.objects

        if index > len(self.indirect_object) - 1:
            return None

        if self.direct_object[index] in chars:
            return chars[self.indirect_object[index]]

        if self.subject[index] in obj:
            return obj[self.indirect_object[index]]

        return None


