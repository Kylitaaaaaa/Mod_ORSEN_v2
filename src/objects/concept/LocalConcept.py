from . import Concept

class LocalConcept(Concept):

    user_id = -1
    score = 0
    valid = 1

    def __init__(self, id, first, rel, second, user_id, score, valid):
        super().__init__(id, first, rel, second)

        self.user_id = user_id
        self.score = score
        self.valid = valid

    def __str__(self):
        return str(self.id) + " " + self.first + " " + self.relation + " " + self.second + " " + str(self.score) + " " + str(self.valid)