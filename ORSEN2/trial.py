from src.dialoguemanager import Follow_Up, DBO_Follow_Up
from src.db.concepts import DBO_Concept, DBO_Local_Concept
from numpy import random

def get_string_template(template2):
    final_response = ""
    for j in range(len(template2)):
        final_response += template2[j]
    return final_response

template = "_character_ used _A_ to _B_" #for replacing
assertionsList= []
assertionsList.append("character CapableOf B")
assertionsList.append("A UsedFor B")
print(template)

searchConcept = []
searchConcept.append("first")
searchConcept.append("second")

replace = ["character", "A", "B"]
position = [1, 3, 5]

template2 = template.split("_")
#print(template2)

#DICTIONARY
dict = {}
dict[template2[1]] = "Irene"
dict[template2[3]] = "mic"
dict[template2[5]] = "sing"

#print(dict[template2[1]])
tempChar = ""

template2[1] = "Mary"
conceptList= []

for i in range(len(assertionsList)):
    tempList = assertionsList[i].split(" ")
    first1 = tempList[0]
    relation1 = tempList[1]
    second1 = tempList[2]

    if tempChar != "":
        second1 = tempChar

    if searchConcept[i] == "first":
        usable_concepts = DBO_Concept.get_concept_like(relation1, first=first1)

    else:
        usable_concepts = DBO_Concept.get_concept(second1, relation1)
    
        while len(usable_concepts) == 0:
            usable_concepts = DBO_Concept.get_concept_like(relation1, first=first1)
            concept_index = random.randint(0,len(usable_concepts))
            concept = usable_concepts[concept_index]
            conceptList[0] = concept
    
    if len(usable_concepts) != 0:
        concept_index = random.randint(0,len(usable_concepts))
        concept = usable_concepts[concept_index]
        tempChar = concept.second
        conceptList.append(concept)
    
    if i == len(assertionsList)-1:
        template2[3] = concept.first
        template2[5] = concept.second

print("Assertion 0: ", conceptList[0])
print("Assertion 1: ", conceptList[1])
p = get_string_template(template2)
print(p)