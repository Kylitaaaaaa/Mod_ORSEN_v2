from . import DBOConcept
from src.objects.concept import GlobalConcept

"""
    Global implementation of DBO Concept which uses the GlobalConcept object type.
    As of now, I don't think there is anything unique to Global types, making this implementation a bit too empty.
"""
class DBOConceptGlobalImpl(DBOConcept):
    def __init__(self):
        DBOConcept.__init__(self, "concepts", GlobalConcept)
        print("Done")
