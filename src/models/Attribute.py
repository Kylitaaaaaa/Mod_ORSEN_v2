class Attribute():

    relation = ""
    description = ""
    is_negated = False

    def __init__(self, relation, description, is_negated):
        self.relation = relation
        self.description = description
        self.is_negated = is_negated
