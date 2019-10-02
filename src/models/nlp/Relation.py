class Relation():

    def __init__(self, first = "", second = "", keyword = "", relation = "", third = "", keyword_type = "", is_flipped = "n", is_negated= "n"):
        self.first_token = first
        self.second_token = second
        self.keyword = keyword
        self.relation = relation
        self.third_token = third
        self.keyword_type = keyword_type
        self.is_flipped = False
        self.is_negated = False

        if is_flipped == 'y':
            self.is_flipped = True

        if is_negated == 'y':
            self.is_negated = True

    def __str__(self):
        my_string = "%s -> %s(%s) -> %s " % (self.first_token, self.relation, self.keyword, self.second_token)

        if self.third_token is not None:
            if self.third_token.strip() is not "":
                my_string = my_string \
                            + "\t(+ %s) " % (self.third_token)

        my_string = my_string \
                    + "\t(type %s, negated: %s, flipped: %s)" % (self.keyword_type, self.is_negated, self.is_flipped)

        return my_string