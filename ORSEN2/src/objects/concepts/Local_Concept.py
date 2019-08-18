class Local_Concept():

    id = -1
    userid = -1
    first = ""
    relation = ""
    second = ""
    score = 0
    valid = 1

    def __init__(self, id, userid, first, rel, second, score, valid):
        self.id         = id
        self.userid     = userid
        self.relation   = rel
        self.first      = first
        self.second     = second
        self.score      = score
        self.valid      = valid

    def __str__(self):
        return str(self.id) + " " + self.first +" "+ self.relation +" "+ self.second + " " + str(self.score) + " " + str(self.valid)