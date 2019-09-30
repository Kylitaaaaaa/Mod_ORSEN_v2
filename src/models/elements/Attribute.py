class Attribute:

    relation = ""
    name = ""
    isNegated = False

    def __init__(self, relation="", name="", isNegated = False):
        self.relation = relation
        self.name = name
        self.isNegated = isNegated
