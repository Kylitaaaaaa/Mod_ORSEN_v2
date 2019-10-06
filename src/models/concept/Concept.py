class   Concept():

    id = -1
    relation = ""
    first = ""
    second = ""

    def __init__(self, id, first, rel, second):
        self.id         = id
        self.first = first
        self.relation = rel
        self.second = second


    def one_line_print(self):
        my_string = "%s --(%s)--> %s" % (str(self.first), str(self.relation), str(self.second))
        return my_string

    def __str__(self):
        value = ""
        for att in dir(self):
            if "__" not in att:
                value = value + att + ": " + str(getattr(self, att)) + "\n"
        return value

        # print(self.__dir__())
        # return self.first + " " + self.relation + " " + self.second
