from . import Object

class Character(Object):
    gender = ""

    def __init__(self, name, type, attribute, in_setting, mentioned, gender):
        super().__init__(name, type, attribute, in_setting, mentioned)

        self.gender = gender