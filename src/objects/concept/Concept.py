class Concept():

    id = -1
    relation = ""
    first = ""
    second = ""

    def __init__(self, id, first, rel, second):
        self.id         = id
        self.first = first
        self.relation = rel
        self.second = second


    def __str__(self):
        value = ""
        for att in dir(self):
            if "__" not in att:
                value = value + att + ": " + str(getattr(self, att)) + "\n"
        return value

        # print(self.__dir__())
        # return self.first + " " + self.relation + " " + self.second
