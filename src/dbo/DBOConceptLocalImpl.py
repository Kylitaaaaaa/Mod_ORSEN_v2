from . import DBOConcept
from src.objects.concept import LocalConcept

"""
    Global implementation of DBO Concept which uses the GlobalConcept object type.
"""
class DBOConceptGlobalImpl(DBOConcept):
    def __init__(self):
        DBOConcept.__init__(self, "concepts", LocalConcept)
        print("Done")
