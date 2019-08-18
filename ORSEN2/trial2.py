from src.dialoguemanager import Follow_Up, DBO_Follow_Up
from src.db.concepts import DBO_Concept, DBO_Local_Concept
from numpy import random
from sys import exit

def filler(curr_blank, used_concept_list, return_back):
    DATABASE_TYPE = DBO_Local_Concept
    dbtype = "L"

    print("Dictionary", dict_nodes)
    print("curr_blank: ", curr_blank)
    print("Used CL", used_concept_list)

    if curr_blank == len(assertion_list)+1:
        for x in range(len(blanks)):
            if blanks[x] in DATABASE_TYPE.RELATIONS:
                #only need the last one sa used concept list kasi yun naman yun ginamit
                temp = used_concept_list[x][-1].split(":")
                if temp[0] == "G":
                    global_used_concepts.append(temp[1])
                elif temp[0] == "L":
                    local_used_concepts.append(temp[1])
                    follow_up_relations.append([x, temp[1]])
        return "TEMPLATE COMPLETE"

    elif curr_blank == 0:
        used_concept_list[curr_blank].clear()
        return "Change move"
    
    if return_back == True:
        #exit(0)
        used_concept_list[curr_blank].clear()

        if dependent_node_split[curr_blank-1] != "None":
            dict_nodes[dependent_node_split[curr_blank-1]] = ""

        if dependent_node_split[curr_blank-1] == "None":
            return filler(curr_blank - 1, used_concept_list, True)

    blank_type = blanks[curr_blank-1]

    #subject.id if real code na
    if blank_type == "Character":
        to_replace = True
        #Maybe use indexing for replacing, marker - list the position

        charas = ["person"]

        charas = [x for x in charas if x not in used_concept_list[curr_blank-1]]
        charas = [x for x in charas if x not in dict_nodes.values()]

        if len(charas) > 0:
            choice_index = random.randint(0, len(charas))
            subject = charas[choice_index]

            #subject = "person"
            dict_nodes[num_nodes[curr_blank-1]] = subject
            used_concept_list[curr_blank-1].append(subject)

            return filler(curr_blank + 1, used_concept_list, False)
        else:
            return filler(curr_blank - 1, used_concept_list, True) #and remove index
            ### ADD REMOVER OF THE INDEX
        
    elif blank_type in DATABASE_TYPE.RELATIONS:
        usable_concepts = []
        bin_assertion_template = assertion_list[curr_blank-1]

        # This while loop is for the DATABASE_TYPE
        # Priority would be the Local then if no concept, change to global
        while len(usable_concepts) <= 0:
            result_nodes = node_decider(bin_assertion_template)
            print("dbtype:", dbtype)
            print(result_nodes)
            if result_nodes[0] == "NODE_START":
                usable_concepts = DATABASE_TYPE.get_concept_like(blank_type, first=result_nodes[1])
            elif result_nodes[0] == "NODE_END":
                usable_concepts = DATABASE_TYPE.get_concept_like(blank_type, second=result_nodes[1])
            elif result_nodes[0] == "NODE_BOTH":
                usable_concepts = DATABASE_TYPE.get_concept_like(blank_type, first=result_nodes[1], second=result_nodes[2])
            else:
                usable_concepts = []
            
            # START OF REMOVE USED CONCEPT
            assertionL = []
            assertionG = []
            #if len(used_concept_list) > 0: #Check this pa
            for x in used_concept_list[curr_blank-1]:
                temp = x.split(":")
                if temp[0] == "G":
                    assertionG.append(temp[1])
                else:
                    assertionL.append(temp[1])
            
            temp_index = []

            for remove_index in range(len(usable_concepts)):
                if dbtype == "G":
                    assertionG = assertionG + global_used_concepts
                    if str(usable_concepts[remove_index].id) in assertionG:
                        temp_index.append(remove_index)
                elif dbtype == "L":
                    assertionL = assertionL + local_used_concepts
                    if str(usable_concepts[remove_index].id) in assertionL:
                        temp_index.append(remove_index)

            temp_index.sort()
            temp_index.reverse()
            for x in temp_index:   
                del usable_concepts[x]
            # END OF REMOVE USED 

            # Switching of Database Type
            if len(usable_concepts) == 0 and dbtype == "G":
                break
  
            elif len(usable_concepts) == 0 and dbtype == "L":
                DATABASE_TYPE = DBO_Concept
                dbtype = "G"
            
        # 
        
        if len(usable_concepts) == 0:
           return filler(curr_blank - 1, used_concept_list, True)
           ### ADD REMOVER OF THE INDEX
        
        if len(usable_concepts) > 0:
            # Also check if the concept was already use here, use loops
            concept_index = random.randint(0,len(usable_concepts))
            concept = usable_concepts[concept_index]

            if result_nodes[0] == "NODE_START":
                dict_nodes[bin_assertion_template[2]] = concept.second   
            elif result_nodes[0] == "NODE_END":
                dict_nodes[bin_assertion_template[0]] = concept.first
            elif result_nodes[0] == "NODE_BOTH":
                dict_nodes[bin_assertion_template[0]] = concept.first
                dict_nodes[bin_assertion_template[2]] = concept.second

            used_concept_list[curr_blank-1].append(dbtype + ":" + str(concept.id))

            #START - AVOID USING THE SAME NODE IN ONE SENTENCE
            rev_dict = {} 
            for key, value in dict_nodes.items(): 
                rev_dict.setdefault(value, set()).add(key) 
      
            result = [key for key, values in rev_dict.items() 
                                        if len(values) > 1] 
            if len(result) > 0:
                if result[0] != "":
                    return filler(curr_blank, used_concept_list, False)
            
            #END - AVOID USING THE SAME NODE IN ONE SENTENCE

            print(concept.first)
            print(concept.relation)
            print(concept.second)

            return filler(curr_blank + 1, used_concept_list, False)

    elif blank_type == "Object":
        #object = ["ball", "gift", "cake"]
        object = ["cake"]

        object = [x for x in object if x not in used_concept_list[curr_blank-1]]
        object = [x for x in object if x not in dict_nodes.values()]

        if len(object) > 0:
            choice_index = random.randint(0, len(object))
            subject = object[choice_index]

            #dict_nodes[str(curr_blank)] = subject
            dict_nodes[num_nodes[curr_blank-1]] = subject
            used_concept_list[curr_blank-1].append(subject)

            return filler(curr_blank + 1, used_concept_list, False)
        
        else:
            return filler(curr_blank - 1, used_concept_list, True) #and remove index
            ### ADD REMOVER OF THE INDEX

    elif blank_type == "Repeat":
        dict_nodes[str(curr_blank)] = "FEE"
        return filler(curr_blank + 1, used_concept_list, False)

    return "hi"

def node_decider(bin_assertion_template):

    starting_node = bin_assertion_template[0]
    ending_node = bin_assertion_template[2]

    result_nodes = []
    if starting_node in dict_nodes.keys() and ending_node in dict_nodes.keys():
        if dict_nodes[starting_node] != "" and dict_nodes[ending_node] != "":
            result_nodes.extend(["NODE_BOTH", dict_nodes[starting_node], dict_nodes[ending_node]]) 
        elif dict_nodes[starting_node] != "":
            result_nodes.extend(["NODE_START", dict_nodes[starting_node]])
        elif dict_nodes[ending_node] != "":
            result_nodes.extend(["NODE_END", dict_nodes[ending_node]])
        else:
            #TODO? If not under object or character
            return "NODE_NEITHER" 

    if starting_node not in dict_nodes.keys():
        #this condition is not being used for now
        result_nodes.extend(["NODE_START", starting_node])
        
    elif ending_node not in dict_nodes.keys():
        result_nodes.extend(["NODE_END", ending_node])
    return result_nodes


id = 1

''' ???? IDK IF NEED PA CONSIDER ITO
not sure if change curr_blanks -> use dict_nodes[curr_blanks] or
assertion_list[x][0] -> dict_nodes[assertion_list[x][0]]

template = "_3_ _1_ the _2_"
relation = "3 Character, 3 CapableOf 1, 2 Object, 2 ReceivedAction 1"
blank = "Character,CapableOf,Object,ReceivedAction"
nodes = "3,1,2"
#dependent_node = "None,1,None,3"
dependent_node = "3,1,2,None"'''

'''
template = "_1_ _2_ the _3_"
relation = "1 Character, 1 CapableOf 2, 3 Object, 3 ReceivedAction 2"
blank = "Character,CapableOf,Object,ReceivedAction"
nodes = "1,2,3"
#dependent_node = "None,1,None,3"
dependent_node = "1,2,3,None"'''

'''
template = "_1_ skies"
relation = "1 IsA place"
blank = "IsA"
nodes = "1"
#dependent_node = "None,1,None,3"
dependent_node = "1"'''

'''
template = "_1_ wanted to _2_ during the _3_ _4_"
relation = "1 Character, 1 CapableOf 2, 4 IsA weather, 3 HasProperty 4"
blank = "Character,CapableOf,IsA,HasProperty"
nodes = "1,2,4,3"
dependent_node = "1,2,4,3"


template = "_3_ _4_"
relation = "4 IsA weather, 4 HasProperty 3"
blank = "IsA,HasProperty"
nodes = "4,3"
dependent_node = "4,3" '''

'''
template = "Then on _1_, _2_ used_ _3_ for _4_."
relation = "1 IsA day, 2 Character, 3 Object, 3 UsedFor 4, 2 CapableOf 4"
blank = "IsA,Character,Object,UsedFor,CapableOf"
nodes = "1,2,3,4"
dependent_node = "1,2,3,4,None"'''

'''
template = "_1_ went to the _2_ to _3_"
relation = "1 Character, 1 AtLocation 2, 2 UsedFor 3"
blank = "Character,AtLocation,UsedFor"
nodes = "1,2,3"
dependent_node = "1,2,3" '''


'''
template = "_1_ skies"
relation = "1 IsA weather"
blank = "IsA"
nodes = "1"
#dependent_node = "None,1,None,3"
dependent_node = "1"'''
'''
template = "I see so _1_"
relation = "1 Repeat"
blank = "Repeat"
nodes = "1"
#dependent_node = "None,1,None,3"
dependent_node = "1"'''

'''
template = "_1_ _2_ and _1_ _3_"
relation = "1 Character, 1 CapableOf 2, 1 CapableOf 3"
blank = "Character,CapableOf,CapableOf"
nodes = "1,2,3"
#dependent_node = "None,1,None,3"
dependent_node = "1,2,None" '''


template = "_1_ made a _2_ _3_ by _4_"
relation = "1 Character, 3 Object, 3 HasProperty 2, 3 CreatedBy 4, 1 CapableOf 4"
blank = "Character,Object,HasProperty,CreatedBy,CapableOf"
nodes = "1,3,2,4"
dependent_node = "1,3,2,4,None" 

template_split = str(template).split("_")
relation_split = str(relation).split(",")
blanks = str(blank).split(",")
num_nodes = nodes.split(",")
dependent_node_split = dependent_node.split(",")


assertion_list = []
for i in range(len(relation_split)):
    x = relation_split[i].split(" ")
    x[:] = (value for value in x if value != "")
    assertion_list.append(x)

dict_nodes = {}
for i in num_nodes:
    dict_nodes[i] = ""

used_concept_list = [["" for x in range(0)] for y in range(len(dependent_node_split))]

global_used_concepts = []
local_used_concepts = []

follow_up_relations = []

curr_blank = 1
return_back = False

uwu = filler(curr_blank, used_concept_list, return_back)

if uwu == "TEMPLATE COMPLETE":
    keys = [ k for k in dict_nodes]
    for x in range(len(keys)):
        for y in range(len(template_split)):
            if template_split[y] == keys[x]:
                template_split[y] = dict_nodes.get(keys[x])
print(dict_nodes)
print(used_concept_list)
print(template_split)

print(uwu)


# FOR FOLLOW UP

print ("FR", follow_up_relations)
print (assertion_list)
print(dict_nodes)

blankers = "None,None,_3_ can be _2_,_3_ is created by _4_,_1_ can _4_"

blankers = str(blankers).split(",")

blankers_list = []
for i in range(len(blankers)):
    x = blankers[i].split("_")
    x[:] = (value for value in x if value != "")
    blankers_list.append(x)

print(blankers_list)

# Fill up blanks
final = []
final2 = []
start = 65

for x in range(len(follow_up_relations)):
    print("AS", len(follow_up_relations))
    print('blankers', len(blankers_list))
    temp = blankers_list[follow_up_relations[x][0]]
    print(x, temp)
    if (len(temp) == 2):
        final.append([chr(start) + ". ", dict_nodes[temp[0]], temp[1]])
    else:
        final.append([chr(start) + ". ", dict_nodes[temp[0]], temp[1], dict_nodes[temp[2]]])
    final2.append([chr(start), follow_up_relations[x][1]])

    start = start + 1

final_rep = ""
for x in range(len(final)):
    for y in range (len(final[x])):
        final_rep += final[x][y]

    #if x != len(final)-1:
    final_rep += " ||| "
    
    if x == len(final)-1:
        final_rep += chr(start) + ". None of the Above"

print(final)
print(final2)
start = 65
print(final_rep)

'''
# Determine which relation
ans = input()

ans_list = ans.split(" ")
print(len(ans_list))

for x in range(len(final2)):
    for y in range(len(ans_list)):
        if final2[x][0] == ans_list[y]:
            print(final2[x][1]) #MINUS IT!
        else:
            print("Do Nothing")

#for x in range (len(final)):


print(follow_up_relations)

for x in range(len(follow_up_relations)):
    print(follow_up_relations[x][1])'''





