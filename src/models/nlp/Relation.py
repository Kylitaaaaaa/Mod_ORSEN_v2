class Relation():
    id = ""
    relation = ""
    first = ""
    keywords = ""
    second = ""
    third = ""
    keyword_type = ""
    is_flipped = ""

    def __init__(self, id, rel, first, keywords, second, third = "", keyword_type = "", is_flipped = ""):
        self.id         = id
        self.relation   = rel
        self.first      = first
        self.keywords   = keywords
        self.second     = second
        self.third      = third
        self.keyword_type = keyword_type
        self.is_flipped = is_flipped

    def __str__(self):
        return self.relation + " ( " + self.first +", " + self.second + " )  " + self.keywords + self.is_flipped