from . import DBOConcept
from src.objects.concept import LocalConcept

class DBOConceptGlobalImpl(DBOConcept):
    def __init__(self):
        DBOConcept.__init__(self, "concepts", LocalConcept)
        print("Done")
