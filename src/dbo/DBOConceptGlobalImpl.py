from . import DBOConcept
from src.objects.concept import GlobalConcept

class DBOConceptGlobalImpl(DBOConcept):
    def __init__(self):
        DBOConcept.__init__(self, "concepts", GlobalConcept)
        print("Done")
