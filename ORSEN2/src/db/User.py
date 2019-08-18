class User():

    id = -1
    name = ""
    code = ""

    def __init__(self, id, name, code):
        self.id         = id
        self.name       = name
        self.code       = code

    def __str__(self):
        return str(self.id) + " " + self.name