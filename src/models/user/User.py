class User:

    def __init__(self, id, name, code, heuristics=[]):
        self.id = id
        self.name = name
        self.code = code
        self.heuristics = heuristics

    def __str__(self):
        return str(self.id) + " " + self.name