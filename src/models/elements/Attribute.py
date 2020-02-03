from src.models.pickles.PickleObject import PickleObject
import spacy

class Attribute:

    relation = ""
    description = ""
    is_negated = False

    def __init__(self, relation, description, is_negated, keyword=""):
        self.relation = relation
        self.description = description
        self.is_negated = is_negated
        self.keyword = keyword

    @staticmethod
    def create_from_relation(relation):
        new_attribute = None
        if relation.is_flipped == False:
            keyword = ""
            if relation.keyword_type == 1:
                keyword = relation.keyword
            else:
                # keyword = hardcode ka ng somethign dito based sa value niya sa database.
                if relation.keyword == "aux":
                    keyword = "can"
                elif relation.keyword == "agent":
                    keyword = "by"
                elif relation.keyword == "auxpass":
                    keyword = "was"
                elif relation.keyword == "det":
                    keyword = "can be"
                elif relation.keyword == "ROOT":
                    keyword = "has"


            new_attribute = Attribute(relation.relation, relation.second_token, relation.is_negated, keyword)

        return new_attribute

    @staticmethod
    def create_relation(relation, description, is_negated):
        return Attribute(relation, description, is_negated)

    def __str__(self):
        my_string = "%s --> %s" % (self.relation, self.description)
        if self.is_negated:
            my_string = my_string + " (negated)"
        return my_string

    def __eq__(self, other):
        if self.relation == other.relation:
            if self.description == other.desciption:
                if self.is_negated == other.is_negated:
                    return True

    def get_pickled_atribute(self):
        pickled_attribute = PickleObject()
        pickled_attribute.relation = str(self.relation)
        pickled_attribute.description = str(self.description)
        pickled_attribute.is_negated = self.is_negated
        pickled_attribute.keyword = str(self.keyword)

        return pickled_attribute