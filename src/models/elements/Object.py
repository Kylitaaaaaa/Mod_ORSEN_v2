from src import IS_A
from . import Attribute


class Object:

    def __init__(self, id="", name="", type=[], attribute=[], in_setting="", mention_count=0):
        self.id = id
        self.name = name
        self.type = type
        self.attribute = attribute
        self.in_setting = in_setting
        self.mention_count = mention_count

    def __str__(self):
        my_string = "(" + self.id + ")" + self.name + "\n" 
        for a in self.attribute:
            my_string = my_string + str(a) + "\n"
        
        for t in self.type:
            my_string = my_string + str(t) + "\n"
        
        my_string = my_string + "mentioned: " + str(self.mention_count)
                    
        return my_string.strip()

    @staticmethod
    def get_object_entity_via_token(token, sentence):
        entities = sentence.ents

        for ent in entities:
            print(token.text, "vs", ent)
            print("Ent range:", ent.start, "to", ent.end)
            if type(ent) == type(token):
                print("Entity range:", token.start, "to", token.end)
                if ent.start <= token.start and ent.end >= token.end:
                    return ent
            elif type(ent[0]) == type(token):
                print("Token index:", token.i)
                if ent.start <= token.i < ent.end:
                    return ent
            print()
        return None

    @staticmethod
    def create_object(sentence, token, id="", attribute=[], in_setting="", mention_count=0, gender=""):
        entity = Object.get_object_entity_via_token(token, sentence)

        entity_text = token.text
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


        new_object = Object(id = entity_text,
                            name = entity_text,
                            type = entity_types,
                            attribute = attribute,
                            in_setting= in_setting,
                            mention_count = mention_count)

        return new_object