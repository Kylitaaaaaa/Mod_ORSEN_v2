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

    @staticmethod
    def create_unflipped_template(template):
        new_template = template
        if template.is_flipped == True:
            if template.third.strip() == "":
                new_template = ExtractionTemplate(id=template.id,
                                                  relation=template.relation,
                                                  first=template.second,
                                                  keyword=template.keyword,
                                                  second=template.first,
                                                  third=template.third,
                                                  keyword_type=template.keyword_type,
                                                  is_flipped='n')
            else:
                new_template = ExtractionTemplate(id=template.id,
                                                  relation=template.relation,
                                                  first=template.third,
                                                  keyword=template.keyword,
                                                  second=template.second,
                                                  third=template.first,
                                                  keyword_type=template.keyword_type,
                                                  is_flipped='n')
        return new_template
