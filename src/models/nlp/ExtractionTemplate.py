class ExtractionTemplate:

    def __init__(self, id="", relation="", first="", keyword="", second="", third="", keyword_type="", is_flipped=""):
        self.id = id
        self.relation = relation
        self.first = first
        self.keyword = keyword
        self.second = second
        self.third = third
        self.keyword_type = keyword_type
        self.is_flipped = False

        if is_flipped == 'y':
            self.is_flipped = True

    def __str__(self):
        my_string = "(%s) %s -> %s(%s) -> %s " % (self.id, self.first, self.relation, self.keyword, self.second)

        if self.third is not None:
            if self.third.strip() is not "":
                my_string = my_string \
                            + "\t(+ %s) " % (self.third)

        my_string = my_string \
                    + "\t(type %s, flipped: %s)" % (self.keyword_type, self.is_flipped)

        return my_string