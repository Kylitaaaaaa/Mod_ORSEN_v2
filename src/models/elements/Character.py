from src import IS_A
from src.models.elements import Object, Attribute
from src.models.pickles.PickleObject import PickleObject


class Character(Object):

    def __init__(self, id="", name="", type=[], attribute=[], in_setting=[], mention_count=0, gender=""):
        super().__init__(id, name, type, attribute, in_setting, mention_count)

        self.gender = gender

    def infer_gender(self, sentence, token):
        pass

    def add_in_setting(self, setting):
        self.in_setting.append(setting)
        
    @staticmethod
    def create_character(sentence, token, id="", attribute=[], in_setting=[], mention_count=0, gender=""):
        entity = Object.get_object_entity_via_token(token, sentence.ents)
        print("The entity I found is: ", entity)
        entity_text = str(token)
        entity_types = []

        if entity is not None:
            entity_text = entity.text
            entity_type = Attribute(relation=IS_A, description=entity.label_, is_negated=False)
            entity_types.append(entity_type)

        if type(attribute) == Attribute:
            attribute = [attribute]

        for a in attribute:
            if a.relation == IS_A:
                entity_types.append(a)

        new_character = Character(id = entity_text,
                                  name = entity_text,
                                  type = entity_types,
                                  attribute = attribute,
                                  in_setting= in_setting,
                                  mention_count = mention_count,
                                  gender = gender)
        return new_character

    @staticmethod
    def create_from_object(object):
        new_char = Character(id = object.id,
                             name = object.name,
                             type = object.type,
                             in_setting = object.in_setting,
                             mention_count = object.mention_count,
                             attribute = object.attributes)
        return new_char


    def get_pickled_character(self):
        pickled_character = PickleObject()
        pickled_character.id = str(self.id)
        pickled_character.name = str(self.name)

        pickled_character.type = []
        for X in self.type:
            pickled_character.type.append(X.get_pickled_atribute())

        pickled_character.in_setting = []
        for X in self.in_setting:
            pickled_character.in_setting.append(X.get_pickled_setting())

        pickled_character.mention_count = self.mention_count
        pickled_character.gender = self.gender
        pickled_character.pickled_char_obj = 'Character'

        return pickled_character
