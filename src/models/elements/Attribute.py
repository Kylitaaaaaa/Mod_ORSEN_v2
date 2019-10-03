class Attribute:

    relation = ""
    description = ""
    is_negated = False

    def __init__(self, relation, description, is_negated):
        self.relation = relation
        self.description = description
        self.is_negated = is_negated

    @staticmethod
    def create_from_relation(relation):
        new_attribute = None
        if relation.is_flipped == False:
            new_attribute = Attribute(relation.relation, relation.second_token, relation.is_negated)

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