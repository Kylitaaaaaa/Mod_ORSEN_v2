import requests
from src.db.concepts.DBO_Concept import DBO_Concept
from src.objects.concepts.Concept import Concept

# obj = requests.get('http://api.conceptnet.io/c/en/fitting?rel=/r/RelatedTo&limit=1000').json()
# print(obj.keys())
# print(len(obj['edges']))
# print(obj['edges'][2])

res = DBO_Concept.getConceptForWord("cat")
for a in res:
    print(a)

conc = Concept(-1, "horse", Concept.RELATION_ISA, "animal")
resu = DBO_Concept.addConcept(conc)
print(resu)