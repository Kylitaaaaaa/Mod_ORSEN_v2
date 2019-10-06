from . import Concept

class GlobalConcept(Concept):

    pass

    @staticmethod
    def convert_local_to_global(local_concept):
        global_concept = GlobalConcept(id=-1, first=str(local_concept.first), rel=str(local_concept.relation), second=str(local_concept.second))
        return global_concept