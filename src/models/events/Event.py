from src.models.elements import Character, Object


class Event():

    sequence_number = -1
    type = ""
    subject = None #Object/Character object

    def __init__(self, sequence_number, type, subject):
        self.sequence_number = sequence_number
        self.type = type
        self.subject = subject

    def get_sequence_number(self):
        return self.sequence_number

    def get_type(self):
        return self.type

    def get_subject(self):
        return self.subject

    def get_characters_involved(self):
        characters = []

        if type(self.subject) == Character:
            characters.append(self.subject)

        return characters

    def get_objects_involved(self):
        objects = []

        if type(self.subject) == Object:
            objects.append(self.subject)

        return objects

    def get_pickled_event(self):
        pass

    def get_pickled_char_obj(self, unpickled):
        if type(unpickled) == Object:
            return unpickled.get_pickled_object()
        elif type(unpickled) == Character:
            return unpickled.get_pickled_character()

