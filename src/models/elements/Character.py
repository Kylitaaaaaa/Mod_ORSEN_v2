from . import Object

class Character(Object):
    gender = ""

    def __init__(self, id="", name="", type="", attribute=[], in_setting="", mention_count=0, gender=""):
        super().__init__(id, name, type, attribute, in_setting, mention_count)

        self.gender = gender

    @staticmethod
    def create_character(self, sentence, token, id="", attribute=[], in_setting="", mention_count=0, gender=""):

        char_type = ""
        for ent in sentence.ents:
            if ent.start <= token.i < ent.end:
                char_type = ent.label_

        new_character = Character(id = id,
                                  name = token.text,
                                  type = char_type,
                                  attribute = attribute,
                                  in_setting= in_setting,
                                  mention_count = mention_count,
                                  gender = gender
                                  )


    @staticmethod
    def convert_from_object(object):
        new_char = Character(id = object.id,
                             name = object.name,
                             type = object.type,
                             in_setting = object.in_setting,
                             mention_count = object.mention_count,
                             attribute = object.attributes)
        return new_char

