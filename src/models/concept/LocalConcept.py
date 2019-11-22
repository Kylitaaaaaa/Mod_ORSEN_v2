from . import Concept

class LocalConcept(Concept):

    user_id = -1
    score = 0
    valid = 1

    def __init__(self, id, user_id, first, rel, second, score, valid):
        super().__init__(id, first, rel, second)

        self.user_id = user_id
        self.score = score
        self.valid = valid

    @staticmethod
    def create_local_concept_from_relation(relation, user):
        local_concept = LocalConcept(id=-1,
                                     first=str(relation.first_token),
                                     rel=str(relation.relation),
                                     second=str(relation.second_token),
                                     user_id=str(user.id),
                                     score=0,
                                     valid=True)

        return local_concept