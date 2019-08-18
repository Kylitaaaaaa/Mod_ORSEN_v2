from src.db.concepts import DBO_Concept, DBO_Local_Concept
from src.objects.concepts.Local_Concept import Local_Concept
from src.objects.concepts.Concept import Concept
from src.objects.eventchain.EventFrame import EventFrame, FRAME_DESCRIPTIVE, FRAME_EVENT, FRAME_CREATION
from src.objects.nlp.Sentence import Sentence
from src.objects.storyworld.Attribute import Attribute
from src.objects.storyworld.Character import Character
from src.objects.storyworld.Object import Object
from src.objects.storyworld.Setting import Setting
from src.inputprocessor import DBO_Relation, Relation
from neuralcoref import Coref
import _operator
import re


# ----- luisa


def reading(filename):
    with open(filename, 'r') as f:
        userinput = f.read()
    return userinput


# user input goes through spacy
# comment by Jilyan this function actually just copy pastes the output of spacy
# user input goes through spacy in run.py before this function is called. it is not done here 
def pos_ner_nc_processing(sentence, ie_fileWriter):
    new_sentence = Sentence()
    new_sentence.words = sentence

    for token in sentence:
        new_sentence.children.append([])
        new_sentence.text_token.append(token.text)
        new_sentence.head_text.append(token.head.text)
        new_sentence.lemma.append(token.lemma_)
        new_sentence.pos.append(token.pos_)
        new_sentence.tag.append(token.tag_)
        new_sentence.dep.append(token.dep_)

        new_sentence.finished_nodes.append(0)
        for child in token.children:
            new_sentence.children[len(new_sentence.children) - 1].append(child)

    for ent in sentence.ents:
        new_sentence.text_ent.append(ent.text)
        new_sentence.label.append(ent.label_)

    for chunk in sentence.noun_chunks:
        new_sentence.text_chunk.append(chunk.text)
        new_sentence.dep_root.append(chunk.root.dep_)
        new_sentence.dep_root_head.append(chunk.root.head.text)

    print("This is the output for pos_ner_nc_processing: ")
    print("input/new_sentence.words: " + str(new_sentence.words))
    print("children:	")
    print(new_sentence.children)
    print("text_token:	")
    print(new_sentence.text_token)
    print("lemma:		")
    print(new_sentence.lemma)
    print("head_text:	")
    print(new_sentence.head_text)
    print("dep:			")
    print(new_sentence.dep)
    print("pos:			")
    print(new_sentence.pos)
    print("tag:			")
    print(new_sentence.tag)
    print("text ents:   ")
    print(new_sentence.text_ent)
    print("ent label:   ")
    print(new_sentence.label)

    ie_fileWriter.write("This is the output for pos_ner_nc_processing: \n")
    ie_fileWriter.write("input/new_sentence.words: " + str(new_sentence.words) + "\n")
    ie_fileWriter.write("children:	\n")
    ie_fileWriter.write(str(new_sentence.children) + "\n")
    ie_fileWriter.write("text_token:\n")
    ie_fileWriter.write(str(new_sentence.text_token) + "\n")
    ie_fileWriter.write("lemma:		\n")
    ie_fileWriter.write(str(new_sentence.lemma) + "\n")
    ie_fileWriter.write("head_text:	\n")
    ie_fileWriter.write(str(new_sentence.head_text) + "\n")
    ie_fileWriter.write("dep:		\n")
    ie_fileWriter.write(str(new_sentence.dep) + "\n")
    ie_fileWriter.write("pos:		\n")
    ie_fileWriter.write(str(new_sentence.pos) + "\n")
    ie_fileWriter.write("tag:		\n")
    ie_fileWriter.write(str(new_sentence.tag) + "\n")
    ie_fileWriter.write("text ents: \n")
    ie_fileWriter.write(str(new_sentence.text_ent) + "\n")
    ie_fileWriter.write("ent label: \n")
    ie_fileWriter.write(str(new_sentence.label) + "\n\n")
    
    return new_sentence


# look for the index of a word (child) in sent(sentence)
def find_text_index(sent, child):
    num = -1 # I changed this from '0' to '-1' - jilyan
    child = str(child).lower()
    temp = child.split()
    for k in range(0, len(sent.text_token)):
        text_token = str(sent.text_token[k]).lower()
        if k < len(sent.finished_nodes) and len(temp) > 0:
            if (temp[-1] == text_token) and (sent.finished_nodes[k] == 0):
                num = k
                break
    return num


# checks if the list of entities extracted from spacy (sent) contains the word (ent)
def find_ent_index(sent, ent):
    # print("ENTER find_ent_index")
    ent = ent.lower()
    for k in range(0, len(sent.text_ent)):
        if ent in str(sent.text_ent[k]).lower():
            return k
            # break
    return None


# extracts story world details from parsed sentences
def details_extraction(sent, world, current_node, subj="", neg="", text=""):
    num = -1
    subject = subj
    current_index = -1
    dative = ""
    direct_object = ""
    for i in range(0, len(sent.dep)):
        if not text:
            if (sent.dep[i] == current_node) and (sent.finished_nodes[i] == 0):
                current_index = i
                sent.finished_nodes[i] = 1
                break
        else:
            if (sent.dep[i] == current_node) and (sent.finished_nodes[i] == 0) and (sent.text_token[i] == text):
                current_index = i
                sent.finished_nodes[i] = 1
                break

            if (current_node == "ROOT") and (sent.pos[i] in ["NOUN", "PROPN"]):
                add_objects(sent, sent.text_token[i], sent.dep[i], sent.lemma[i], world)

    if neg == "":
        is_negated = False
    else:
        is_negated = neg

    if current_index != -1:
        i = current_index
        for j in range(0, len(sent.children[i])):
            num = find_text_index(sent, str(sent.children[i][j]))
            if num != -1 and sent.finished_nodes[num] == 0 and \
                    sent.dep[num] in ["nsubj", "acomp", "attr", "nsubjpass", "dobj", "xcomp", "appos", "relcl",
                                      "npadvmod", "advmod", "pcomp"]:
                # nominal subject
                if sent.dep[num] == "nsubj":
                    subject = compound_extraction(sent, str(sent.children[i][j]))
                    add_objects(sent, str(subject), sent.dep[num], sent.lemma[i], world)
                    add_capability(sent, str(sent.text_token[i]), str(subject), world, current_index, i)

                # nominal subject (passive) or direct object
                elif sent.dep[num] == "nsubjpass" or sent.dep[num] == "dobj":
                    if not subject:
                        subject = compound_extraction(sent, str(sent.children[i][j]))

                    if dative and sent.dep[num] == "dobj":
                        subject = compound_extraction(sent, str(sent.children[i][j]))
                        add_objects(sent, str(subject), sent.dep[num],
                                    sent.lemma[i], world, dative)
                    else:
                        add_objects(sent, compound_extraction(sent, str(sent.children[i][j])), sent.dep[num],
                                    sent.lemma[i], world)

                    if sent.dep[num] == "dobj":
                        direct_object = sent.text_token[num]

                # adjectival complement
                elif sent.dep[num] == "acomp":
                    add_attributes(sent, str(sent.children[i][j]), str(subject), world, is_negated)
                    is_negated = False

                # attribute and appositional modifier
                elif sent.dep[num] == "attr":
                    if not add_settings(sent, num, subject, is_negated, world):
                        add_objects(sent, compound_extraction(sent, str(sent.children[i][j])), sent.dep[num],
                                    sent.lemma[i], world, subject, is_negated)
                        if not subject:
                            subject = sent.text_token[num]

                    is_negated = False

                # appositional modifier
                elif sent.dep[num] == "appos":
                    if not add_settings(sent, num, subject, is_negated, world):
                        add_objects(sent, compound_extraction(sent, str(sent.children[i][j])), sent.dep[num],
                                    sent.lemma[i], world, compound_extraction(sent, str(sent.head_text[num])))

                    is_negated = False

                # open clausal compliment
                elif sent.dep[num] in ["xcomp", "pcomp"]:
                    add_capability(sent, str(sent.lemma[num]), str(subject), world, num)
                    is_negated = False

                # relative clause modifier
                elif sent.dep[num] == "relcl":
                    add_capability(sent, str(sent.text_token[num]), str(sent.head_text[num]), world, num)

                # noun phrase as adverbial modifier
                elif num != -1 and sent.dep[num] in ["npadvmod", "advmod"]:
                    add_settings(sent, num, subject, is_negated, world)
                    sent.finished_nodes[num] = 1

                if sent.children[num] is not None:
                    for c in sent.children[num]:
                        dep_index = find_text_index(sent, str(c))
                        if sent.finished_nodes[dep_index] == 0:
                            details_extraction(sent, world, sent.dep[num], subject, is_negated)

                sent.finished_nodes[num] = 1

            # object predicate
            elif num != -1 and sent.dep[num] == "oprd":
                if direct_object:
                    add_attributes(sent, sent.text_token[num], direct_object, world)
                else:
                    add_attributes(sent, sent.text_token[num], subject, world)

            # negation
            elif num != -1 and sent.dep[num] == "neg":
                sent.finished_nodes[num] = 1
                is_negated = True

            # object of preposition
            elif num != -1 and sent.dep[num] == "pobj":
                if not add_settings(sent, num, subject, is_negated, world):
                    add_objects(sent, compound_extraction(sent, str(sent.children[i][j])), sent.dep[num], sent.lemma[i]
                                , world)
                details_extraction(sent, world, sent.dep[num], subject, is_negated)
                sent.finished_nodes[num] = 1

            # dative - the noun to which something is given
            elif num != -1 and sent.dep[num] == "dative":
                if str(sent.text_token[num]) == "to":
                    details_extraction(sent, world, sent.dep[num], subject, is_negated)
                    if sent.children[num]:
                        dative = compound_extraction(sent, sent.children[num][0])
                else:
                    dative = compound_extraction(sent, str(sent.children[i][j]))
                    add_objects(sent, str(dative), sent.dep[num], sent.lemma[i],world)

                sent.finished_nodes[num] = 1

            elif num != -1 and sent.dep[num] == "agent":
                for nc in range(0, len(sent.text_chunk)):
                    if sent.dep_root_head[nc] == sent.text_token[num]:
                        add_objects(sent, compound_extraction(sent, str(sent.text_chunk[nc])), sent.dep[num],
                                    sent.lemma[i], world)
                        add_capability(sent, str(sent.lemma[i]), str(sent.text_chunk[nc]), world, current_index)
                        sent.finished_nodes[num] == 1
                        break

            # adverbial clause modifier
            # clausal complement
            # conjunction
            # preposition
            # agent
            # adverbial modifier
            elif num != -1 \
                    and sent.dep[num] in ["advcl", "ccomp", "conj", "prep", "acl", "aux"]:
                details_extraction(sent, world, sent.dep[num], subject, is_negated)

            # compound
            elif num != -1 and sent.dep[num] == "compound":
                if sent.pos[num] == "VERB":
                    details_extraction(sent, world, sent.dep[num], subject, is_negated, str(sent.children[i][j]))
                elif sent.pos[num] in ["NOUN", "PROPN"]:
                    subject = compound_extraction(sent, str(sent.children[i][j]))
                    add_objects(sent, str(subject), sent.dep[num], sent.lemma[i], world)
                    add_capability(sent, str(sent.lemma[i]), str(subject), world, current_index)
                    sent.finished_nodes[num] = 1

            else:
                print("WARNING: Dependecy ", sent.dep[num], " not included in the list")
    else:
        print("ERROR: Cannot find current index or node ", current_node, " has been recorded")

# This is made by Jilyan
def compound_extraction(sent, subj):
    num = -1
    initial = subj
    print("~~~~~~~~~~~~~~~~~~~~")
    print(type(subj))
    print(subj)
    subj = subj.lower()
    temp = subj.split()
    # print("ENTER compound_extraction: ")

    # if there is no given word to check
    if not temp:
        return ""

    # find index of given word
    for k in range(len(sent.lemma)):
        if temp[-1] == sent.lemma[k].lower():
            num = k
            break
    
    # go to end of supposed compound word
    if num != -1:
        while sent.dep[num] == 'compound':
            num += 1
        
        # set last of compund word to string
        subj = sent.lemma[num]

        # insert remaining compound word in front of string
        for k in range(num - 1, -1, -1):
            if sent.dep[k] == "compound":
                subj = str(sent.lemma[k]).lower() + " " + subj
            else:
                break

    if initial not in subj:
        subj = initial

    return subj

def char_conj_extractions(sent, subj):
    # print("ENTERED char_conj_extractions")
    
    subj = str(subj).lower()
    list_of_conj = [subj]
    temp = str(subj).split()
    if not temp:
        return []

    subj = temp[-1]
    for k in range(0, len(sent.head_text)):
        head_text = str(sent.head_text[k]).lower()
        if head_text == subj and sent.dep[k] == "conj":
            subj = sent.text_token[k].lower()
            print("ADDED THIS", sent.text_token[k].lower())
            list_of_conj.append(compound_extraction(sent, subj))
            sent.finished_nodes[k] = 1
    return list_of_conj


def add_capability(sent, attr, subject, world, num, i=""):
    list_of_char = char_conj_extractions(sent, subject)

    if sent.dep[num - 1] == "neg":
        negation = True
    else:
        negation = False

    if sent.dep[num] == "relcl":
        first_attribute = Attribute(DBO_Concept.RECEIVES_ACTION, sent.lemma[num], negation)
    else:
        first_attribute = Attribute(DBO_Concept.CAPABLE_OF, sent.lemma[num], negation)

    list_of_capabilities = [first_attribute]
    head = attr.lower()

    for j in range(0, len(sent.words)):
        if sent.dep[j] in ['conj'] and (sent.head_text[j] == str(head)):
            if find_neg_attr(sent, j):
                new_attribute = Attribute(DBO_Concept.CAPABLE_OF, sent.text_token[j].lower(), True)
            else:
                new_attribute = Attribute(DBO_Concept.CAPABLE_OF, sent.text_token[j].lower(), False)
            list_of_capabilities.append(new_attribute)
            head = sent.text_token[j].lower()

    for cap in list_of_capabilities:
        if cap.name not in ["is", "was", "are", "be", "am", "are", "were", "been", "being"]:
            for c in list_of_char:
                c = str(c).lower()
                if c in world.characters:
                    new_attribute = check_duplicate_attribute(world.characters[c].attributes, cap)
                    if new_attribute is not None:
                        world.characters[c].attributes.append(new_attribute)
                elif c in world.objects:
                    new_attribute = check_duplicate_attribute(world.objects[c].attributes, cap)
                    if new_attribute is not None:
                        world.objects[c].attributes.append(new_attribute)


def add_objects(sent, child, dep, lemma, world, subject="", negated=""):
    list_of_char = char_conj_extractions(sent, child)
    for c in list_of_char:
        c = c.lower()
        if (c not in world.characters) and (c not in world.objects):
            if (DBO_Concept.get_concept_specified("character", DBO_Concept.CAPABLE_OF, lemma) or
                DBO_Concept.get_concept_specified("person", DBO_Concept.CAPABLE_OF, lemma) is not None) \
                    and dep in ["nsubj", "agent", "compound"]:
                new_character = Character()
                new_character.name = c
                new_character.id = c
                new_character.attributes = []
                new_character.type = []
                
                if get_entity_label(sent, c) == "PERSON":
                        new_character.type.append("person")
                        new_character.type.append("character")

                new_character.inSetting = {'LOC': None, 'DATE': None, 'TIME': None}
                if sent.location:
                    new_character.inSetting = sent.location
                world.add_character(new_character)
                world.characters[new_character.id].timesMentioned = 1
                print("ADDED", new_character.name)

            else:
                new_object = Object()
                new_object.name = c
                new_object.id = c
                new_object.attributes = []
                new_object.type = []
                new_object.inSetting = {'LOC': None, 'DATE': None, 'TIME': None}
                if sent.location:
                    new_object.inSetting = sent.location
                world.add_object(new_object)
                world.objects[new_object.id].timesMentioned = 1
                print("ADDED", new_object.name)

        elif c in world.objects:
            if DBO_Concept.get_concept_specified("character", DBO_Concept.CAPABLE_OF, lemma) is not None \
                    and dep == "nsubj":
                new_character = Character.convert_from_object(world.objects[c])
                world.add_character(new_character)
                world.characters[new_character.id].timesMentioned += 1
            else:
                world.objects[c].timesMentioned += 1

        elif c in world.settings:
            if DBO_Concept.get_concept_specified("character", DBO_Concept.CAPABLE_OF, lemma) is not None \
                    and dep == "nsubj":
                new_character = Character.convert_from_setting(world.settings[c])
                world.add_character(new_character)
                world.characters[new_character.id].timesMentioned += 1

        elif c in world.characters:
            world.characters[c].timesMentioned += 1

        # add amod and poss attribute
        char_index = find_text_index(sent, c)
        for ch in sent.children[char_index]:
            index = find_text_index(sent, ch)

            if sent.dep[index] in ["amod", "nummod"]:
                add_attributes(sent, sent.text_token[index], str(c), world)
                sent.finished_nodes[index] = 1

            elif sent.dep[index] in ["poss"]:
                if sent.text_token[index] in world.characters:
                    add_attributes(sent, c, sent.text_token[index], world, "", DBO_Concept.HAS_A)
                    char = world.characters[sent.text_token[index]]
                    char.timesMentioned += 1
                    sent.finished_nodes[index] = 1
                elif sent.text_token[index] in world.objects:
                    add_attributes(sent, c, sent.text_token[index], world, "", DBO_Concept.HAS_A)
                    obj = world.objects[sent.text_token[index]]
                    obj.timesMentioned += 1
                    sent.finished_nodes[index] = 1
                else:
                    add_objects(sent, compound_extraction(sent, str(sent.text_token[index])), sent.dep[index], lemma,
                                world)
                    add_attributes(sent, c, compound_extraction(sent, str(sent.text_token[index])), world, "",
                                   DBO_Concept.HAS_A)
    if dep in ["attr", "appos"]:
        add_attributes(sent, child, subject, world, negated, DBO_Concept.IS_A)
    if dep in ["dobj", "relcl"]:
        if subject:
            add_attributes(sent, child, subject, world, negated, DBO_Concept.HAS_A)


def check_duplicate_attribute(obj_attributes, attribute):
    for i in obj_attributes:
        if i.name == attribute.name:
            if i.isNegated is not attribute.isNegated:
                i.isNegated = attribute.isNegated
            return None
    return attribute


def find_neg_attr(sent, int):
    for i in range(0, len(sent.children[int])):
        j = find_text_index(sent, str(sent.children[int][i]))
        if sent.dep[j] == "neg":
            return True

    return False


def add_attributes(sent, child, subject, world, negation="", relation=""):
    if relation == "":
        relation = DBO_Concept.HAS_PROPERTY
    print("FIRST ATTR", child.lower)
    first_attribute = Attribute(relation, child.lower(), negation)
    list_of_attributes = [first_attribute]
    list_of_char = char_conj_extractions(sent, subject)
    head = child.lower()

    for i in range(0, len(sent.words)):
        if (sent.dep[i] == 'conj') and (sent.head_text[i] == str(head)):
            if find_neg_attr(sent, i):
                new_attribute = Attribute(relation, sent.text_token[i].lower(), True)

            else:
                new_attribute = Attribute(relation, sent.text_token[i].lower(), False)
            list_of_attributes.append(new_attribute)
            head = sent.text_token[i].lower()
            sent.finished_nodes[i] = 1

    for c in list_of_char:
        c = str(c).lower()
        if c in world.characters:
            for attr in list_of_attributes:
                char = world.characters[c]
                new_attribute = check_duplicate_attribute(char.attributes, attr)

                if new_attribute is not None:
                    char.attributes.append(new_attribute)

                    if relation == DBO_Concept.IS_A:
                        print("RELATION", relation)
                        if not attr.isNegated:
                            char.type.append(attr.name)

        elif c in world.objects:
            for attr in list_of_attributes:
                obj = world.objects[c]
                new_attribute = check_duplicate_attribute(obj.attributes, attr)
                if new_attribute is not None:
                    obj.attributes.append(new_attribute)

                    if relation == DBO_Concept.IS_A:
                        print("RELATION", relation)
                        if not attr.isNegated:
                            obj.type.append(attr.name)


def add_settings(sent, num, subject, negation, world):
    if sent.location:
        current_location = sent.location
    else:
        current_location = {'LOC': None, 'DATE': None, 'TIME': None}

    list_of_char = []
    is_setting = False
    if subject:
        list_of_char = char_conj_extractions(sent, subject)

    if not negation:
        ent_index = find_ent_index(sent, str(sent.text_token[num]))
        if ent_index is not None:
            label = sent.label[ent_index]
            ent_text = sent.text_ent[ent_index]
        else:
            label = ""
            ent_text = sent.text_token[num]
        ent_text = str(ent_text).lower()

        if ent_text not in world.settings:

            is_location = \
                label in ["LOC", "GPE"] or \
                DBO_Concept.get_concept_specified(str(sent.text_token[num]), DBO_Concept.IS_A, "place") or \
                DBO_Concept.get_concept_specified(str(sent.text_token[num]), DBO_Concept.IS_A, "location") or \
                DBO_Concept.get_concept_specified(str(sent.text_token[num]), DBO_Concept.IS_A, "site")

            is_date_time = \
                label in ["DATE", "TIME"] or \
                DBO_Concept.get_concept_specified(str(sent.text_token[num]), DBO_Concept.IS_A, "time period")

            if is_location or is_date_time:

                if is_location:
                    type_name = "LOC"
                else:
                    type_name = "TIME"

                is_setting = True
                new_setting = Setting()
                new_setting.id = ent_text
                new_setting.name = ent_text
                new_setting.type = type_name
                current_location[type_name] = ent_text
                world.add_setting(new_setting)

            sent.location = current_location

        else:
            is_setting = True

            if str(sent.text_token[num]).lower() in world.settings:
                if world.settings[str(sent.text_token[num]).lower()].type == "LOC":
                    current_location["LOC"] = ent_text
                elif world.settings[str(sent.text_token[num])].type == "TIME":
                    current_location["TIME"] = ent_text

        for c in list_of_char:
            if str(c) in world.characters and current_location:
                char = world.characters[str(c)]
                for key, value in current_location.items():
                    if value:
                        char.inSetting[key] = value
            elif str(c) in world.objects and current_location:
                obj = world.objects[str(c)]
                for key, value in current_location.items():
                    if value:
                        obj.inSetting[key] = value
    return is_setting


# ---------- rachel

CAT_STORY = 1
CAT_COMMAND = 2
CAT_ANSWER = 3


# ie_categorizing
def getCategory(sentence):
    # checks if entry has "orsen"
    sentence = sentence.lower()
    if 'orsen' in sentence or 'im stuck' == sentence or "i'm stuck" == sentence or 'your turn' == sentence or 'help me' == sentence or 'help me start' == sentence:
        return CAT_COMMAND
    elif 'yes' == sentence or 'no' == sentence or "don't like" in sentence or "dont like" in sentence or "wrong" in sentence:
        return CAT_ANSWER
    else:
        return CAT_STORY

def convert_indef_pron(sent):
    indef = ["everybody", "anybody", "somebody", "everyone", "someone", "anyone"]
    split = re.findall(r"[\w']+|[.,!?;]", sent)

    for index in range(0, len(split)):
        if split[index].lower() in indef:
            split[index] = "character"

    sent = " ".join(split)
    return sent

def coref_resolution(s, sent_curr, sent_bef, world, isFirst, ie_fileWriter):
    print("ENTERED coref_resolution")
    ie_fileWriter.write("Before Coref Resolution : ")
    ie_fileWriter.write(sent_curr + "\n")
    coref = Coref()

    num_prn = 0
    num_conj = 0
    num_pron = 0

    for x in range(0, len(s.pos)):
        if s.tag[x] == 'PRP' or s.tag[x] == 'PRP$':
            num_prn += 1
        if s.pos[x] == 'CCONJ':
            num_conj += 1
        if s.lemma[x] == '-PRON-':
            num_pron += 1

    for x in range(0, num_prn):
        if num_conj >= 1:
            sent = coref.continuous_coref(utterances=sent_curr)
            num_conj -= 1
        if isFirst is False:
            sent = coref.one_shot_coref(utterances=sent_curr, context=sent_bef)

        coref.get_mentions()

        rep = coref.get_most_representative()
        scores = coref.get_scores()
        propn_count = 0
        noun_count = 0

        print("rep")
        print(rep)

        for i in range(0, len(s.text_token)):
            if s.pos[i] == 'PROPN':
                propn_count += 1
            if s.tag[i] == 'NN':
                noun_count += 1

        if propn_count < 1:
            if noun_count < 1 and isFirst is True:
                return sent_curr

        if len(rep) > 0 and len(scores) > 0:
            for key, value in rep.items():
                if str(key).lower() == "his" or str(key).lower() == "hers" or str(key).lower() == "their" or str(key).lower() == "our" or str(key).lower() == "its":
                    sent_curr = re.findall(r"[\w']+|[.,!?;]", sent_curr)
                    for i in range(len(sent_curr)):
                        if sent_curr[i].lower() == str(key).lower():
                            sent_curr[i] = str(value) + "'s"

                    sent_curr = " ".join(sent_curr)
                else:
                    sent_curr = re.findall(r"[\w']+|[.,!?;]", sent_curr)
                    for i in range(len(sent_curr)):
                        if sent_curr[i].lower() == str(key).lower():
                            sent_curr[i] = str(value)

                    sent_curr = " ".join(sent_curr)

                if (str(value) not in world.characters) and (str(value) not in world.objects):
                    if (str(key).lower() == "he") or (str(key).lower() == "his") or (str(key).lower() == "him"):
                        new_character = Character()
                        new_character.name = str(value)
                        new_character.id = str(value)
                        new_character.gender = "M"
                        new_character.type = []
                        type = find_ent_index(s, str(value))
                        if type != None:
                            print(type)
                            new_character.type.append(type)
                        world.add_character(new_character)
                        world.characters[new_character.id].timesMentioned += 1

                    elif (str(key).lower() == "she") or (str(key).lower() == "her") or (str(key).lower() == "hers"):
                        new_character = Character()
                        new_character.name = str(value)
                        new_character.id = str(value)
                        new_character.gender = "F"
                        new_character.type = []
                        type = find_ent_index(s, str(value))
                        if type != None:
                            print(type)
                            new_character.type.append(type)
                        world.add_character(new_character)
                        world.characters[new_character.id].timesMentioned += 1

        # elif len(scores.get('single_scores')) > 1:
        # extract scores
        #    single_mention = scores.get('single_scores')

        #    pair_mention = scores.get('pair_scores')

        #    single_sc_lib = []
        #    pair_sc_lib = []
        #    count = 0
        #    for i in range(0, len(single_mention)):
        #        if single_mention.get(i) == none.get(0):
        #          count += 1
        #        else:
        #          single_sc_lib.append(float(single_mention.get(i)))
        # count -=1
        # print("COUNT", count)
        # print("SINGLE_SC_LIB", single_sc_lib)
        #
        # print("INDEX min", single_sc_lib.index(min(single_sc_lib)))
        # ow_single_index = single_sc_lib.index(min(single_sc_lib))
        # low_single_index += count

        # print("found it low_single_index: ", low_single_index)
        # holder = {}

        # print(pair_mention.get(low_single_index))
        # holder = pair_mention.get(low_single_index)

        # print("holder", len(holder))
        ##for i in range(0, len(holder)):
        #    pair_sc_lib.append(holder.get(i))

        # print("PAIR!!!!!!!!!!!", pair_sc_lib)
        # high_pair_index = pair_sc_lib.index(max(pair_sc_lib))
        # print("found it high_pair_index: ", high_pair_index)

        # prn.append(mentions[low_single_index])
        # noun.append(mentions[high_pair_index])
        # print(noun, prn)
        # print("numPron", num_pron)

        # for i in range(0, len(prn)):
        #    for k in range(0, len(s.text_token)):
        #        #print("ASAIFHA", str(noun[i]), s.text_token[k])
        #        if s.text_token[k] in str(noun[i]):
        #            if s.pos[k] != 'NOUN' or s.pos[k] != 'PROPN':
        #                return sent_curr
        #    print("SENTENCE", sent_curr)
        #    sent_curr = sent_curr.replace(str(prn[i]), str(noun[i]))

        else:
            first_second = ["i", "me", "my", "mine", \
                            "we", "us", "our", "ours", \
                            "you", "your", "yours"]

            isThis = ""
            changeThis = ""
            for i in range(0, len(s.text_token)):
                print("in loop " + str(i))

                if s.dep[i] == 'nsubj' and (s.pos[i] == 'PROPN' or s.pos[i] == 'NOUN'):
                    # print(s.dep[i], "check prop or noun", s.pos[i])
                    isThis = s.text_token[i]
                    for j in range(0, len(s.text_token)):
                        if s.dep[j] == 'nsubj' and s.pos[j] == 'PRON' or s.tag[j] == 'PRP$' or s.tag[j] == 'PRP':
                            # print(s.dep[j], "check pron", s.pos[j])
                            changeThis = s.text_token[j]

                elif s.pos[i] == 'NOUN' or s.pos[i] == 'PROPN':
                    isThis = s.text_token[i]
                    for j in range(0, len(s.text_token)):
                        if s.dep[j] == 'nsubj' and s.pos[j] == 'PRON' or s.tag[j] == 'PRP$' or s.tag[j] == 'PRP':
                            # print(s.dep[j], "check pron", s.pos[j])
                            changeThis = s.text_token[j]

                if isThis != "" and changeThis != "":
                    if changeThis.lower() == 'her' or changeThis.lower() == 'his' or changeThis.lower() == 'our':
                        isThis = isThis + "'s"

                    split = re.findall(r"[\w']+|[.,!?;]", sent_curr)
                    for i in range(0, len(split)):
                        if split[i] == changeThis and changeThis.lower() in first_second:
                            if split[i].lower() == "you":
                                if split[i-1].lower() != "thank": 
                                    split[i] = "character"
                            else:
                                split[i] = "character"
                        elif split[i] ==changeThis:
                            split[i] = isThis
                    sent_curr = " ".join(split)

                isThis = ""
                changeThis = ""
    ie_fileWriter.write("After Coref Resolution : ")
    ie_fileWriter.write(sent_curr + "\n\n")

    sent_curr = convert_indef_pron(sent_curr)
    ie_fileWriter.write("After Converting Indef : ")
    ie_fileWriter.write(sent_curr + "\n\n")

    return sent_curr


def isAction(sentence):
    isAction = False
    be_forms = ["is", "are", "am", "were", "was", "feels", "looks"]
    for k in range(0, len(be_forms)):
        for i in range(0, len(sentence.text_token)):
            if be_forms[k] == sentence.text_token[i]:
                isAction = True

    return isAction


# ie_event_extract
def event_extraction(sentence, world, current_node):
    print("----- Entering EVENT EXTRACTION -----")
    event_iobj = []
    event_subj = []
    event_subj_act = []
    event_dobj = []
    event_prep = []
    event_detail = []
    event_type = []
    event_attr = []
    event_pobj = []
    event_create = []
    # Getting the count of each annotation
    nsubj_c = 0
    comp_c = 0
    poss_c = 0
    acomp_c = 0
    agent_c = 0
    root_c = 0
    neg_act_c = 0
    pobj_c = 0
    dobj_c = 0
    neg_obj_c = 0
    attr_c = 0
    ccomp_c = 0
    advcl_c = 0
    relcl_c = 0
    dative_c = 0
    oprd_c = 0
    xcomp_c = 0
    advmod_c = 0
    npadvmod_c = 0
    prep_c = 0
    expl_c = 0

    for i in range(0, len(sentence.dep)):
        if sentence.dep[i] == 'nsubj' or sentence.dep[i] == 'nsubjpass':
            nsubj_c += 1
        elif sentence.dep[i] == 'compound':
            comp_c += 1
        elif sentence.dep[i] == 'poss':
            poss_c += 1
        elif sentence.dep[i] == 'acomp':
            acomp_c += 1
        elif sentence.dep[i] == 'agent':
            agent_c += 1

        if sentence.dep[i] == 'ROOT':
            root_c += 1
            if sentence.dep[i - 1] == 'neg':
                neg_act_c += 1

        if sentence.dep[i] == 'pobj':
            pobj_c += 1
        elif sentence.dep[i] == 'dobj':
            dobj_c += 1
        elif sentence.dep[i] == 'attr':
            attr_c += 1
        elif sentence.dep[i] == 'ccomp':
            ccomp_c += 1
        elif sentence.dep[i] == 'advcl':
            advcl_c += 1
        elif sentence.dep[i] == 'relcl':
            relcl_c += 1
        elif sentence.dep[i] == 'dative':
            dative_c += 1
        elif sentence.dep[i] == 'oprd':
            oprd_c += 1
        elif sentence.dep[i] == 'xcomp':
            xcomp_c += 1
        elif sentence.dep[i] == 'advmod':
            advmod_c += 1
        elif sentence.dep[i] == 'npadvmod':
            npadvmod_c += 1
        elif sentence.dep[i] == 'prep':
            prep_c += 1
        elif sentence.dep[i] == 'pobj':
            pobj_c += 1
    # print("nsubj count: ", nsubj_c)
    # print("root count: ", root_c)
    # print("advmod count: ", advmod_c)
    # print("dobj count: ", dobj_c)
    isFound_char = False
    isFound_char_act = False
    isFound_obj = False
    isFound_obj_act = False
    isFound_mobj_act = False
    isFound = False

    if agent_c > 0:
        isPassive = True

    desc = ['being', 'be', 'been', 'is', 'are', 'was', 'were', 'am']
    plural = ['we', 'they', 'them', 'our', 'them', 'us', 'you']
    for i in range(0, len(sentence.dep)):
        # ----START OF CHARACTER EXTRACTION----#

        if nsubj_c == 0:

            if sentence.dep[i] == 'expl':
                expl_c += 1
                print("EXPL", expl_c)
                event_create.append(sentence.text_token[i].lower())
                for y in range(0, len(sentence.dep)):
                    if sentence.dep[y] == 'attr':
                        event_subj.append(sentence.text_token[y])
                        hold_c = sentence.text_token[y]
                        attr_c -= 1
        elif sentence.dep[i] == 'nsubj' or sentence.dep[i] == 'nsubjpass' and nsubj_c > 0:
            if i > 0:
                # Compound Subj
                if sentence.dep[i - 1] == 'compound' and comp_c > 0 and sentence.dep[i] == 'nsubj':
                    # print("Compound and not poss")
                    # if sentence.text_token[i - 1] != sentence.text_token[i]:
                    # 	c_char = sentence.text_token[i - 1] + " " + sentence.head_text[i - 1]
                    # else:
                    # 	c_char = sentence.head_text[i - 1]
                    # done by Jilyan
                    c_char = compound_extraction(sentence ,sentence.text_token[i])

                    event_subj.append(c_char)
                    if (i + 1) < len(sentence.dep):
                        if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                            for k in range(0, len(sentence.dep)):
                                if (i + k) < len(sentence.dep):
                                    if sentence.dep[i + k] == 'conj':
                                        event_subj[len(event_subj) - 1] += ',' + sentence.text_token[i + k]
                                        if sentence.dep[i + k + 1] != 'cc' or sentence.dep[i + k + 1] != 'punct':
                                            k = len(sentence.dep)
                    comp_c -= 1
                    nsubj_c -= 1
                    if nsubj_c == 0:
                        isFound_char = True

                # Poss Subj
                elif poss_c > 0 and sentence.dep[i - 2] == 'poss':
                    if sentence.dep[i - 1] == 'case':
                        # print("poss and not compound")
                        p_char = sentence.text_token[i - 2] + sentence.text_token[i - 1] + " " + sentence.text_token[i]

                        event_subj.append(p_char)
                        poss_c -= 1
                        nsubj_c -= 1

                        if nsubj_c == 0:
                            isFound_char = True

                elif sentence.dep[i - 3] == 'compound' and sentence.dep[i - 2] == 'poss' and comp_c > 0 and poss_c > 0:
                    print("compound and poss")
                    cp_char = sentence.text_token[i - 3] + " " + sentence.text_token[i - 2] + sentence.text_token[
                        i - 1] + " " + sentence.text_token[i]

                    event_subj.append(cp_char)
                    poss_c -= 1
                    comp_c -= 1
                    nsubj_c -= 1
                    if nsubj_c == 0:
                        isFound_char = True

            if (i + 1) < len(sentence.dep) and isFound_char is False:
                if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                    # Multiple Subj
                    test_char = sentence.text_token[i]
                    isAdded = False

                    for k in range(0, len(sentence.dep)):
                        if (i + k) < len(sentence.dep):
                            if sentence.dep[i + k] == 'conj':
                                print("event_subj: ", len(event_subj), event_subj)
                                if isAdded is False:
                                    print("test", test_char)
                                    event_subj.append(test_char)
                                    isAdded = True
                                print("event_subj: ", len(event_subj), event_subj)
                                if sentence.head_text[i + k] == event_subj[len(event_subj) - 1]:
                                    event_subj[len(event_subj) - 1] += "," + sentence.text_token[i + k]
                                    print("event_subj: ", len(event_subj), event_subj)
                                    isFound_mchar = True

                                    nsubj_c -= 1
                                    if nsubj_c == 0:
                                        isFound_char = True
            if nsubj_c > 0 and isFound_char is False:
                event_subj.append(sentence.text_token[i])
                nsubj_c -= 1
                if nsubj_c == 0:
                    isFound_char = True

        # ----END OF CHARACTER EXTRACTION -----#
        # ----START OF CHARACTER ACTION EXTRACTION ----#

        if sentence.dep[i] == 'aux' or sentence.dep[i] == 'auxpass' and (i + 1) < len(sentence.dep):
            isAdded = False
            isFound = False
            if sentence.dep[i + 1] == 'ccomp' and ccomp_c > 0 and isAdded is False:
                isFound = True
                ccomp_c -= 1
                event_subj_act.append(sentence.text_token[i] + " " + sentence.text_token[i + 1])
                isAdded = True
                print("Added Char Action: ", sentence.text_token[i] + " " + sentence.text_token[i + 1])
                head_hold = sentence.text_token[i + 1]
                if (i + 2) < len(sentence.dep):
                    if sentence.dep[i + 2] == 'cc' or sentence.dep[i + 2] == 'punct':
                        for x in range(0, len(sentence.dep)):
                            if sentence.dep[x] == 'conj' and sentence.head_text[x] == head_hold:
                                event_subj.append(event_subj[len(event_subj) - 1])
                                event_subj_act.append(sentence.text_token[x])
                                print("Added Char Action: ", sentence.text_token[x])

            if (i + 2) < len(sentence.dep) and isAdded is False:
                if sentence.dep[i + 1] == 'neg':
                    isFound = True
                    event_subj_act.append(
                        sentence.text_token[i] + " " + sentence.text_token[i + 1] + " " + sentence.text_token[i + 2])
                    isAdded = True
                    print("Added Char Action: ",
                          sentence.text_token[i] + " " + sentence.text_token[i + 1] + " " + sentence.text_token[i + 2])
                    head_hold = sentence.text_token[i + 2]
                    if (i + 3) < len(sentence.dep):
                        if sentence.dep[i + 3] == 'cc' or sentence.dep[i + 3] == 'punct':
                            for x in range(0, len(sentence.dep)):
                                if sentence.dep[x] == 'conj' and sentence.head_text[x] == head_hold:
                                    event_subj.append(event_subj[len(event_subj) - 1])
                                    if sentence.dep[x - 1] == 'neg':
                                        event_subj_act.append(
                                            sentence.text_token[i] + " " + sentence.text_token[x - 1] + " " +
                                            sentence.text_token[x])
                                    elif sentence.dep[x - 3] == 'neg':
                                        event_subj_act.append(
                                            sentence.text_token[i] + " " + sentence.text_token[x - 3] + " " +
                                            sentence.text_token[x])
                                    else:
                                        event_subj_act.append(sentence.text_token[i] + " " + sentence.text_token[x])
                                    event_attr.append('-')
                                    event_dobj.append('-')
                                    event_iobj.append('-')
                                    event_type.append(0)
                                    event_prep.append('-')
                                    event_pobj.append('-')
                                    event_detail.append('-')
                                    print("Added Char Action: ", sentence.text_token[x])

            if (i + 2) < len(sentence.dep) and isAdded is False:
                if sentence.pos[i + 1] == 'VERB' and sentence.dep[i + 2] == 'cc' or sentence.dep[i + 2] == 'punct':
                    isFound = True
                    event_subj_act.append(sentence.text_token[i] + " " + sentence.text_token[i + 1])
                    isAdded = True
                    print("Added Char Action: ", sentence.text_token[i] + " " + sentence.text_token[i + 1])
                    head_hold = sentence.text_token[i + 1]
                    for x in range(0, len(sentence.dep)):
                        if sentence.dep[x] == 'conj' and sentence.head_text[x] == head_hold:
                            event_subj.append(event_subj[len(event_subj) - 1])
                            if sentence.dep[x - 1] == 'neg':
                                event_subj_act.append(sentence.text_token[i] + " " + sentence.text_token[x - 1] + " " +
                                                      sentence.text_token[x])
                            else:
                                event_subj_act.append(sentence.text_token[i] + " " + sentence.text_token[x])
                            event_attr.append('-')
                            event_dobj.append('-')
                            event_iobj.append('-')
                            event_type.append(0)
                            event_prep.append('-')
                            event_pobj.append('-')
                            event_detail.append('-')
                            print("Added Char Action: ", sentence.text_token[i])

            if sentence.pos[i + 1] != 'VERB' and isAdded is False:
                event_subj_act.append(sentence.text_token[i] + " " + sentence.head_text[i])
                isAdded = True
                isFound = True
                print("Added Char Action: ", sentence.text_token[i] + " " + sentence.head_text[i])
                head_hold = sentence.head_text[i]
                if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                    for x in range(0, len(sentence.dep)):
                        if sentence.dep[x] == 'conj' and sentence.head_text[x] == head_hold:
                            event_subj.append(event_subj[len(event_subj) - 1])
                            event_subj_act.append(sentence.text_token[x])
                            event_type.append(0)
                            event_prep.append('-')
                            event_pobj.append('-')
                            event_attr.append('-')
                            event_dobj.append('-')
                            event_iobj.append('-')
                            event_detail.append('-')
                            print("Added Char Action: ", sentence.text_token[x])

            if sentence.pos[i + 1] == 'VERB' and isAdded is False:
                if sentence.dep[i] == 'auxpass':
                    event_subj_act.append(sentence.head_text[i])
                    print("Added Char Action: ", sentence.head_text[i])
                else:
                    event_subj_act.append(sentence.text_token[i] + " " + sentence.head_text[i])
                    print("Added Char Action: ", sentence.text_token[i] + " " + sentence.head_text[i])
                isAdded = True
                isFound = True
                if sentence.dep[i + 1] == 'conj':
                    event_subj.append(event_subj[len(event_subj) - 1])
                    event_detail.append('-')
                    event_pobj.append('-')
                    event_prep.append('-')
                    event_type.append(0)
                    event_dobj.append('-')
                    event_iobj.append('-')
                    event_attr.append('-')

        elif sentence.dep[i] != 'conj' and sentence.pos[i] == 'VERB' and sentence.dep[i] != 'nsubj' and sentence.dep[
            i] != 'advcl' and sentence.dep[i] != 'pcomp' and sentence.dep[i] != 'acomp' and sentence.dep[i] != 'xcomp' and i > 1: # (jilyan) added i>1 bec error
            # print("inside third case", sentence.dep[i])
            if sentence.dep[i - 1] != 'neg' and (sentence.dep[i - 2] != 'aux' or sentence.dep[i - 2] != 'auxpass'):
                if sentence.dep[i - 1] != 'aux' and sentence.dep[i - 1] != 'auxpass':
                    print("inside third case", sentence.dep[i])
                    isFound = False
                    if sentence.dep[i] == 'punct':
                        event_subj_act.append(sentence.text_token[i])
                        print("Added Char Action: ", sentence.text_token[i])
                    elif sentence.dep[i] == 'ccomp':
                        event_subj_act.append(sentence.text_token[i])
                        print("Added Char Action: ", sentence.text_token[i])
                    elif sentence.dep[i - 1] != 'punct':
                        event_subj_act.append(sentence.text_token[i])
                        print("Added Char Action: ", sentence.text_token[i])
                    elif sentence.dep[i - 1] == 'punct' and sentence.pos[i - 1] == 'VERB':
                        event_subj_act[len(event_subj_act) - 1] += " " + sentence.text_token[i]
                        print("Added Char Action: ", sentence.text_token[i])
                    else:
                        event_subj_act.append(sentence.text_token[i])
                        print("Added Char Action: ", sentence.text_token[i])
                    head_hold = sentence.text_token[i]
                    isFound = True
                    if (i + 1) < len(sentence.dep):
                        if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                            head_hold = sentence.text_token[i]
                            for x in range(0, len(sentence.dep)):
                                if sentence.dep[x] == 'conj' and sentence.head_text[x] == head_hold:
                                    event_subj.append(event_subj[len(event_subj) - 1])
                                    if sentence.dep[x - 1] == 'neg':
                                        event_subj_act.append(
                                            sentence.text_token[i] + " " + sentence.text_token[x - 1] + " " +
                                            sentence.text_token[x])
                                    else:
                                        event_subj_act.append(sentence.text_token[x])
                                    event_attr.append('-')
                                    event_dobj.append('-')
                                    event_iobj.append('-')
                                    event_type.append(0)
                                    event_prep.append('-')
                                    event_pobj.append('-')
                                    event_detail.append('-')
                                    print("Added Char Action: ", sentence.text_token[x])
        if isFound is True:
            if event_subj_act[len(event_subj_act) - 1] in desc:
                if expl_c > 0:
                    event_type.append(2)
                    print("Added a CREATION")
                else:
                    event_type.append(1)
                    print("Added a DESCRIPTIVE")
            else:
                event_type.append(0)
                print("Added an EVENT")

            event_detail.append('-')
            event_pobj.append('-')
            event_prep.append('-')
            event_attr.append('-')
            event_dobj.append('-')
            event_iobj.append('-')
            isFound = False
            # if neg_act_c == 0 and (i+1) < len(sentence.dep):
            #    test_char_act = sentence.text_token[i]
            #    isAdded = False

            #    if sentence.dep[i+1] == 'cc' or sentence.dep[i+1] == 'punct' or (sentence.dep[i+1] == 'punct' and sentence.dep[i+2] == 'cc'):
            #        for k in range(0, len(sentence.dep)):
            #            if (i + k) < len(sentence.dep):
            #                if sentence.dep[i + k] == 'conj':
            #                    if isAdded is False:
            #                        event_subj_act.append(test_char_act)
            #                        if test_char_act in desc:
            #                            if expl_c == 1:
            #                                event_type.append(2)
            #                                event_dobj.append('-')
            #                                event_prep.append('-')
            #                                event_pobj.append('-')
            #                                event_attr.append('-')
            #                                event_detail.append('-')
            #                               expl_c -= 1
            #                            else:
            #                                event_type.append(1)
            #                                event_dobj.append('-')
            #                                event_prep.append('-')
            #                                event_pobj.append('-')
            ##                                event_attr.append('-')
            #                               event_detail.append('-')
            #                        else:
            #                            event_type.append(0)
            #                            event_dobj.append('-')
            #                            event_pobj.append('-')
            #                            event_prep.append('-')
            #                            event_attr.append('-')
            #                            event_detail.append('-')
            #                        print("Added Char Action: " + test_char_act)

            #                        isAdded = True

            #                    if sentence.head_text[i+k] == test_char_act:
            #                        test_char_act = sentence.text_token[i+k]
            #                        event_subj_act[len(event_subj_act)-1] += "," + sentence.text_token[i+k]

            #                        print("Added Char Action: " + sentence.text_token[i+k])

            # Neg Action
            # if neg_act_c > 0:
            #    if (i+2) < len(sentence.dep):
            #        if sentence.dep[i+1] == 'neg' and sentence.dep[i] == 'aux' and (sentence.dep[i+3] != 'cc' and sentence.dep[i+3] != 'punct'):
            #            if sentence.pos[i+2] == 'VERB':
            #                event_subj_act.append(sentence.text_token[i] + " not " + sentence.text_token[i+2])
            #                if sentence.text_token[i] in desc:
            #                    if expl_c == 1:
            #                        event_type.append(2)
            #                        event_dobj.append('-')
            #                        event_prep.append('-')
            #                        event_pobj.append('-')
            #                        event_attr.append('-')
            #                        event_detail.append('-')
            #                        expl_c -= 1
            #                    else:
            #                        event_type.append(1)
            #                        event_dobj.append('-')
            #                        event_attr.append('-')
            #                        event_prep.append('-')
            #                        event_pobj.append('-')
            #                        event_detail.append('-')
            #                else:
            #                    event_type.append(0)
            #                    event_attr.append('-')
            #                    event_dobj.append('-')
            #                    event_pobj.append('-')
            #                    event_prep.append('-')
            #                    event_detail.append('-')

            #                print("Added Char Action: " + sentence.text_token[i+2], " not " + sentence.text_token[i])

            # Multiple Action
            #    test_char_act = sentence.text_token[i]
            #    isAdded = False
            #    if (i+3) < len(sentence.dep):
            #        if sentence.dep[i+1] == 'neg' and sentence.dep[i] == 'aux':
            #            if sentence.dep[i+3] == 'cc' or sentence.dep[i+3] == 'punct':
            #                for k in range(0, len(sentence.dep)):
            #                    if (i+k) < len(sentence.dep):
            #                        if sentence.dep[i+k] == 'conj':
            #                            if isAdded is False:
            #                                event_subj_act.append(test_char_act)
            #                                if test_char_act in desc:
            #                                    if expl_c == 1:
            #                                        event_type.append(2)
            #                                        event_dobj.append('-')
            #                                        event_prep.append('-')
            #                                        event_pobj.append('-')
            #                                        event_attr.append('-')
            #                                        event_detail.append('-')
            #                                        expl_c -= 1
            #                                    else:
            #                                        event_type.append(1)
            #                                        event_dobj.append('-')
            #                                        event_prep.append('-')
            #                                        event_pobj.append('-')
            #                                        event_attr.append('-')
            #                                        event_detail.append('-')
            #                                else:
            #                                    event_type.append(0)
            #                                    event_dobj.append('-')
            #                                    event_pobj.append('-')
            #                                    event_attr.append('-')
            #                                    event_prep.append('-')
            #                                    event_detail.append('-')
            #                                print("@Added Char Action: ", test_char_act)
            #                                isAdded = True

            #                            if sentence.head_text[i+k] == test_char_act:
            #                                test_char_act = sentence.text_token[i+k]
            #                                event_subj_act[len(event_subj_act)-1] += "," + "not " + sentence.text_token[i + k]
            #                                print("@Added Char Action: ", event_subj_act[len(event_subj_act)-1])
            #                                neg_act_c -= 1

            # Preposition
            # if (i+3) < len(sentence.dep):
            #    if sentence.dep[i] == 'aux' and sentence.dep[i+2] == 'prep' and sentence.dep[i+3] == 'pcomp':
            #        event_subj_act.append(sentence.text_token[i] + " " + sentence.text_token[i+1])
            #        if sentence.text_token[i+1] in desc:
            #            if expl_c == 1:
            #                event_type.append(2)
            #                event_dobj.append('-')
            #                event_prep.append('-')
            #                event_pobj.append('-')
            #                event_attr.append('-')
            #                event_detail.append('-')
            #                expl_c -= 1
            #            else:
            #                event_type.append(1)
            #                event_dobj.append('-')
            #                event_prep.append('-')
            #                event_pobj.append('-')
            #                event_attr.append('-')
            #                event_detail.append('-')
            #        else:
            #            event_type.append(0)
            #            event_dobj.append('-')
            #            event_pobj.append('-')
            #            event_prep.append('-')
            #            event_attr.append('-')
            #            event_detail.append('-')

            #        head_hold = sentence.text_token[i] + " " + sentence.text_token[i+1]
            #        for z in range(0, len(event_subj_act)):
            #            if event_subj_act[z] == head_hold and event_prep[z] == '-':
            #                event_prep[z] = sentence.text_token[i+2]
            #                prep_c -= 1
            #                event_pobj[z] = sentence.text_token[i+3]
            #                pobj_c -= 1

            #        print("Added Char Action: ", head_hold)

            #    if sentence.dep[i] == 'aux' or sentence.dep[i] == 'auxpass':
            #        event_subj_act.append(sentence.text_token[i] + " " +sentence.head_text[i])
            #    else:
            #        event_subj_act.append(sentence.text_token[i])

            #   isFound_agent = False
            #    if sentence.text_token[i] in desc:
            #        if expl_c == 1:
            #            event_type.append(2)
            #            event_dobj.append('-')
            #            event_prep.append('-')
            #            event_pobj.append('-')
            #            event_attr.append('-')
            #            event_detail.append('-')
            #            expl_c -= 1
            #        else:
            #            event_type.append(1)
            #            if agent_c > 0:
            #                for x in range(0, len(sentence.dep)):
            #                    if sentence.dep[x] == 'agent':
            #                        event_prep.append(sentence.text_token[x])
            #                        event_dobj.append(sentence.text_token[x-1])
            #                        isFound_agent = True

            #            if isFound_agent is False:
            #                event_dobj.append('-')
            #                event_prep.append('-')

            #            event_attr.append('-')
            #            event_pobj.append('-')
            #            event_detail.append('-')
            #    else:
            #        event_type.append(0)
            #        event_dobj.append('-')
            #        event_prep.append('-')
            #        event_pobj.append('-')
            #        event_attr.append('-')
            #        event_detail.append('-')

            #    print("Added Char Action: ", sentence.text_token[i])
            #    isFound_char_act = True
            #    root_c -= 1

        # ----END OF CHARACTER ACTION EXTRACTION----#

        # ----START OF OBJECT EXTRACTION----#
        if sentence.dep[i] == 'acomp':
            isFound_acomp = False
            head_hold = sentence.head_text[i]
            if (i + 1) < len(sentence.dep):
                if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                    # Multiple Object
                    test_obj = sentence.text_token[i]
                    isAdded = False
                    if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                        for k in range(0, len(sentence.dep)):
                            if (i + k) < len(sentence.dep):
                                if sentence.dep[i + k] == 'conj':
                                    if isAdded is False:
                                        if head_hold in event_dobj:
                                            for x in range(0, len(event_dobj)):
                                                if event_dobj[x] == head_hold and event_attr[x] == '-':
                                                    if sentence.dep[i - 1] == 'neg':
                                                        event_attr[x] = sentence.text_token[i - 1] + " " + test_obj
                                                    else:
                                                        event_attr[x] = test_obj
                                                    isAdded = True
                                                    isFound_acomp = True
                                        elif head_hold in event_subj_act:
                                            for x in range(0, len(event_subj_act)):
                                                if event_subj_act[x] == head_hold and event_attr[x] == '-':
                                                    if sentence.dep[i - 1] == 'neg':
                                                        event_attr[x] = sentence.text_token[i - 1] + " " + test_obj
                                                    elif sentence.dep[i - 1] == 'aux':
                                                        event_attr[x] = sentence.text_token[i - 1] + " " + test_obj
                                                    else:
                                                        event_attr[x] = test_obj
                                                    isAdded = True
                                                    isFound_acomp = True

                                    if sentence.head_text[i + k] == test_obj or sentence.head_text[i + k] == ',':
                                        test_obj = sentence.text_token[i + k]

                                        if sentence.dep[i + k - 1] == 'neg' or sentence.dep[i + k - 1] == 'aux':
                                            event_attr[len(event_attr)-1] += "," + sentence.text_token[i + k - 1] + " " + test_obj  # this was originally event_attr[x] but i changed it because there is no x and it keeps getting errors - jilyan
                                        elif len(event_attr) > 0:
                                            event_attr[len(event_attr)-1] += "," + test_obj # this was originally event_attr[x] but i changed it because there is no x and it keeps getting errors - jilyan

            if isFound_acomp is False:
                if sentence.dep[i - 1] == 'neg':
                    if head_hold in event_dobj:
                        for x in range(0, len(event_dobj)):
                            if event_dobj[x] == head_hold and event_attr[x] == '-':
                                event_attr[x] = sentence.text_token[i - 1] + " " + sentence.text_token[i]

                    elif head_hold in event_subj_act:
                        for x in range(0, len(event_subj_act)):
                            if event_subj_act[x] == head_hold and event_attr[x] == '-':
                                event_attr[x] = sentence.text_token[i - 1] + " " + sentence.text_token[i]

                else:
                    if head_hold in event_dobj:
                        for x in range(0, len(event_dobj)):
                            if event_dobj[x] == head_hold and event_attr[x] == '-':
                                event_attr[x] = sentence.text_token[i]

                    elif head_hold in event_subj_act:
                        print(event_subj_act)
                        for x in range(0, len(event_subj_act)):
                            if event_subj_act[x] == head_hold and event_attr[x] == '-':
                                event_attr[x] = sentence.text_token[i]

        if sentence.dep[i] == 'dobj':
            isFound_dobj = False
            head_hold = sentence.head_text[i]
            saved_index = 0
            if (i + 1) < len(sentence.dep):
                if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                    # Multiple Object
                    test_obj = sentence.text_token[i]
                    isAdded = False
                    saved_index = 0
                    head_hold = sentence.head_text[i]
                    if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                        for k in range(0, len(sentence.dep)):
                            if (i + k) < len(sentence.dep):
                                if sentence.dep[i + k] == 'conj':
                                    if isAdded is False:
                                        isConnected = False
                                        for z in range(0, len(event_subj_act)):
                                            if head_hold == event_subj_act[z] and event_dobj[z] == '-':
                                                event_dobj[z] = sentence.text_token[i]
                                                print("Added Obj: ", sentence.text_token[i])
                                                saved_index = z
                                                z = len(event_subj_act)
                                                isConnected = True
                                                isAdded = True

                                        if isConnected is False and len(event_dobj) >= len(event_subj_act) and len(event_subj_act) != 0:
                                            event_dobj[len(event_subj_act) - 1] = sentence.text_token[i]

                                        dobj_c -= 1
                                        isFound_dobj = True
                                    if sentence.head_text[i + k] == test_obj or sentence.head_text[i + k] == ',':
                                        test_obj = sentence.text_token[i + k]
                                        if saved_index < len(event_dobj):
                                            event_dobj[saved_index] += "," + test_obj
                                        print("Added Object: ///", test_obj)
                                        isFound_dobj = True

            if isFound_dobj is False:
                print("not yet found dobj")
                head_hold = sentence.head_text[i]
                isConnected = False
                for z in range(0, len(event_subj_act)):
                    if head_hold == event_subj_act[z] and event_dobj[z] == '-':
                        event_dobj[z] = sentence.text_token[i]
                        isConnected = True
                for x in range(0, len(event_pobj)):
                    if head_hold == event_pobj[z] and event_dobj[z] == '-':
                        event_dobj[z] = sentence.text_token[i]
                        isConnected = True

                if isConnected is False:
                    if len(event_subj_act) - 1 <= 0:
                        print("it is zero")
                    elif len(event_subj_act) - 1 < len(event_dobj):
                        event_dobj[len(event_subj_act) - 1] = sentence.text_token[i]

                    isFound_dobj = True

        if sentence.dep[i] == 'attr' and attr_c > 0:
            isFound_attr = False
            head_hold = sentence.head_text[i]
            if sentence.dep[i - 2] == 'neg' and sentence.dep[i - 1] == 'det':
                for x in range(0, len(event_subj_act)):
                    if event_subj_act[x] == head_hold and event_attr[x] == '-':
                        event_attr[x] = "not " + sentence.text_token[i - 1] + " " + sentence.text_token[i]
                        test_obj = sentence.text_token[i]
                        attr_c -= 1
                        isAdded = True
                        isFound_attr = True
            elif sentence.dep[i - 1] == 'neg':
                for x in range(0, len(event_subj_act)):
                    if event_subj_act[x] == head_hold and event_attr[x] == '-':
                        event_attr[x] = sentence.text_token[i - 1] + " " + sentence.text_token[i]
                        attr_c -= 1
                        test_obj = sentence.text_token[i]
                        isFound_attr = True
                        isAdded = True
            elif sentence.dep[i - 1] == 'compound' or sentence.dep[i - 1] == 'nummod':
                for x in range(0, len(event_subj_act)):
                    if event_subj_act[x] == head_hold and event_attr[x] == '-':
                        event_attr[x] = sentence.text_token[i - 1] + " " + sentence.text_token[i]
                        attr_c -= 1
                        test_obj = sentence.text_token[i]
                        isFound_attr = True
                        isAdded = True

            if (i + 1) < len(sentence.dep):
                if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                    # Multiple Object
                    test_obj = sentence.text_token[i]
                    isAdded = False
                    if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                        for k in range(0, len(sentence.dep)):
                            if (i + k) < len(sentence.dep):
                                if sentence.dep[i + k] == 'conj':
                                    if isAdded is False:
                                        for x in range(0, len(event_subj_act)):
                                            if event_subj_act[x] == head_hold and event_attr[x] == '-':
                                                event_attr[x] = test_obj
                                                attr_c -= 1
                                                isFound_attr = True
                                        isAdded = True

                                    if (sentence.head_text[i + k] == test_obj or sentence.head_text[i + k] == ',') and len(event_attr) > 0:
                                        if sentence.dep[i + k - 1] == 'neg':
                                            event_attr[len(event_attr) - 1] += "," + sentence.text_token[i + k - 1] + " " + \
                                                             sentence.text_token[i + k]
                                        elif sentence.dep[i + k - 2] == 'neg' and sentence.dep[i + k - 1] == 'det':
                                            event_attr[len(event_attr) - 1] += "," + sentence.text_token[i + k - 2] + " " + \
                                                             sentence.text_token[i + k]
                                        else:
                                            event_attr[len(event_attr) - 1] += "," + sentence.text_token[i + k]

                                        isFound_obj = True
                                        attr_c -= 1

            if isFound_attr is False:
                for x in range(0, len(event_subj_act)):
                    if event_subj_act[x] == head_hold and event_attr[x] == '-':
                        event_attr[x] = sentence.text_token[i]
                        x = len(event_subj_act)
                        attr_c -= 1



        elif sentence.dep[i] == 'xcomp' and xcomp_c > 0:
            head_hold = sentence.head_text[i]
            saved_index = 0
            isFound_xcomp = False
            for x in range(0, len(event_subj_act)):
                if head_hold in event_subj_act[x]:
                    if sentence.dep[i - 2] == 'aux' and sentence.dep[i - 1] == 'neg':
                        event_subj_act[x] += " " + sentence.text_token[i - 1] + " not " + sentence.text_token[i]
                    elif sentence.dep[i - 1] == 'neg':
                        event_subj_act[x] += " not " + sentence.text_token[i]
                    elif sentence.dep[i - 1] == 'aux':
                        event_subj_act[x] += " " + sentence.text_token[i - 1] + " " + sentence.text_token[i]
                    else:
                        event_subj_act[x] += " " + sentence.text_token[i]

                    test_xcomp = sentence.text_token[i]
                    for k in range(0, len(sentence.dep)):
                        if (i + 2 + k) < len(sentence.dep):
                            if sentence.dep[i + k] == 'cc' or sentence.dep[i + k] == 'punct' and test_xcomp == \
                                    sentence.head_text[i + k]:
                                event_subj_act[x] += "," + sentence.text_token[i + 2 + k]
                                test_xcomp = sentence.text_token[i + 2 + k]

        if sentence.dep[i] == 'prep' and sentence.text_token[i - 1] != '-':
            head_hold = sentence.head_text[i]
            # print("found prep")
            if sentence.head_text[i] in event_subj_act:
                for z in range(0, len(event_subj_act)):
                    if head_hold == event_subj_act[z]:
                        event_prep[z] = sentence.text_token[i]
                        prep_c -= 1
            elif sentence.head_text[i] in event_attr:
                for z in range(0, len(event_attr)):
                    if head_hold == event_attr[z] and event_prep[z] == '-':
                        event_prep[z] = sentence.text_token[i]
                        prep_c -= 1
            else:
                for x in range(0, len(event_subj_act)):
                    holder = event_subj_act[x]
                    if holder.find(head_hold) == -1:
                        print("")
                    else:
                        event_prep[x] = sentence.text_token[i]
                        prep_c -= 1

            for x in range(0, len(sentence.dep)):
                # if (len(event_prep)-1 > x): #I ADDED THIS - CELINA. If will remove, lipat yung mga naka tab na if!
                if len(event_prep) > 0: # Jilyan added this, not sure if tama pero just to avoid index out of bounds
                    if sentence.dep[x] == 'conj' and sentence.head_text[x] == event_prep[len(event_prep) - 1]:
                        event_subj.append(event_subj[len(event_subj) - 1])
                        event_type.append(event_type[len(event_type) - 1])
                        event_subj_act.append(event_subj_act[len(event_subj_act) - 1])
                        event_prep.append(sentence.text_token[x])
                        event_pobj.append('-')
                        event_iobj.append('-')
                        event_attr.append(event_attr[len(event_attr) - 1])
                        event_detail.append(event_detail[len(event_detail) - 1])
                        event_dobj.append(event_dobj[len(event_dobj) - 1])

        if sentence.dep[i] == 'pobj' or sentence.dep[i] == 'pcomp':
            head_hold = sentence.head_text[i]
            saved_index = 0
            for z in range(0, len(event_prep)):
                print(head_hold, event_prep[z], z)
                if head_hold == event_prep[z] and event_pobj[z] == '-':
                    event_pobj[z] = sentence.text_token[i]
                    break

            index = 0
            if sentence.head_text[i] == 'by':
                for x in range(0, len(sentence.text_token)):
                    if sentence.text_token[x] == 'by':
                        index = x
                        break
                for z in range(0, len(event_prep)):
                    if sentence.head_text[index] == event_subj_act[z] and len(event_dobj) > z and len(event_subj) > z:
                        event_dobj[z] = event_subj[z]
                        event_subj[z] = sentence.text_token[i]
                        test_pchar = sentence.text_token[i]
                        if (i + 1) < len(sentence.dep):
                            if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                                for y in range(0, len(sentence.dep)):
                                    print(sentence.head_text[y], test_pchar, "IT IS")
                                    if sentence.dep[y] == 'conj' and sentence.head_text[y] == test_pchar:
                                        test_pchar = sentence.text_token[y]
                                        event_subj[z] += "," + test_pchar
                        break

        # ----END OF OBJECT EXTRACTION----#

        # ----START OF OBJECT ACTION EXTRACTION----#
        elif sentence.dep[i] == 'npadvmod' and npadvmod_c > 0 and isFound_obj_act is False:
            head_hold = sentence.head_text[i]
            if (i + 1) < len(sentence.dep):
                if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                    # Multiple Object
                    test_obj = sentence.text_token[i]
                    isAdded = False
                    if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                        for k in range(0, len(sentence.dep)):
                            if (i + k) < len(sentence.dep):
                                if sentence.dep[i + k] == 'conj':
                                    if isAdded is False:
                                        for x in range(0, len(event_subj_act)):
                                            if event_subj_act[x] == head_hold and event_detail[x] == '-':
                                                event_detail[x] = test_obj
                                                isAdded = True

                                        isAdded = True

                                    if sentence.head_text[i + k] == test_obj or sentence.head_text[i + k] == ',':
                                        test_obj = sentence.text_token[i + k]
                                        if len(event_detail) > 0:
                                            event_detail[len(event_detail)-1] += "," + test_obj
                                        isFound_obj_act = True
                                        npadvmod_c -= 1

            else:
                for x in range(0, len(event_subj_act)):
                    if event_subj_act[x] == head_hold and event_detail[x] == '-':
                        if sentence.dep[i - 1] == 'amod':
                            event_detail[x] = sentence.text_token[i - 1] + " " + sentence.text_token[i]
                        else:
                            event_detail[x] = sentence.text_token[i]

                    npadvmod_c -= 1
                print("Added Obj Act: ", sentence.text_token[i])
                isFound_obj_act = True

        elif sentence.dep[i] == 'advmod' and advmod_c > 0 and isFound_obj_act is False:
            head_hold = sentence.head_text[i]
            if (i + 1) < len(sentence.dep):
                if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                    # Multiple Object
                    test_obj = sentence.text_token[i]
                    isAdded = False
                    if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                        for k in range(0, len(sentence.dep)):
                            if (i + k) < len(sentence.dep):
                                if sentence.dep[i + k] == 'conj':
                                    if isAdded is False:
                                        for x in range(0, len(event_subj_act)):
                                            if event_subj_act[x] == head_hold and event_detail[x] == '-':
                                                event_detail[x] = test_obj
                                                isAdded = True

                                    if sentence.head_text[i + k] == test_obj or sentence.head_text[i + k] == ',':
                                        test_obj = sentence.text_token[i + k]

                                        event_detail[x] += "," + test_obj
                                        isFound_mobj_act = True
                                        isFound_obj_act = True

                        if isFound_mobj_act is True:
                            for l in range(1, len(event_detail)):
                                event_detail[0] += "," + event_detail.pop()
            if advmod_c > 0:
                for x in range(0, len(event_subj_act)):
                    if x < len(event_detail):
                        if event_subj_act[x] == head_hold and event_detail[x] == '-':
                            if sentence.dep[i - 1] == 'amod':
                                event_detail[x] = sentence.text_token[i - 1] + " " + sentence.text_token[i]
                            else:
                                event_detail[x] = sentence.text_token[i]
                            advmod_c -= 1

        # ----END OF OBJECT ACTION EXTRACTION----#
        # ----START OF SPECIAL CASES----#

        if sentence.dep[i] == 'appos':
            event_subj.insert(0, sentence.head_text[i])
            event_subj_act.insert(0, "is")
            # print("Added Char Action: is/")
            event_type.insert(0, 1)
            event_dobj.insert(0, '-')
            event_iobj.insert(0, '-')  # I ADDED THIS - CELINA
            event_prep.insert(0, '-')
            event_pobj.insert(0, '-')
            event_detail.insert(0, '-')
            event_attr.insert(0, sentence.text_token[i])
        elif sentence.dep[i] == 'poss':

            if sentence.pos[i - 1] != 'ADJ':
                print("a", event_subj)
                event_subj.insert(0, sentence.text_token[i])
                if sentence.text_token[i] in plural:
                    event_subj_act.insert(0, "have")
                else:
                    event_subj_act.insert(0, "has")

                event_dobj.insert(0, sentence.head_text[i])
                event_iobj.insert(0, '-')  # I ADDED THIS - CELINA
                event_type.insert(0, 0)
                event_prep.insert(0, '-')
                event_pobj.insert(0, '-')
                event_detail.insert(0, '-')
                event_attr.insert(0, '-')
            else:
                event_subj.insert(0, sentence.text_token[i])
                if sentence.text_token[i] in plural:
                    event_subj_act.insert(0, "have")
                else:
                    event_subj_act.insert(0, "has")
                    # print("this is it")
                event_dobj.insert(0, sentence.head_text[i])
                event_iobj.insert(0, '-')  # I ADDED THIS - CELINA
                event_type.insert(0, 0)
                event_detail.insert(0, '-')
                event_prep.insert(0, '-')
                event_pobj.insert(0, '-')
                event_attr.insert(0, '-')

        elif sentence.dep[i] == 'relcl' and relcl_c > 0:
            event_subj_act.append(sentence.text_token[i])
            if sentence.text_token[i] in desc:
                event_type.append(1)
                event_prep.append('-')
                event_pobj.append('-')
                event_detail.append('-')
                event_attr.append('-')
            else:
                event_type.append(0)
                event_prep.append('-')
                event_pobj.append('-')
                event_attr.append('-')
                event_detail.append('-')

            event_dobj.append(sentence.head_text[i])
            event_iobj.append('-')

        elif sentence.dep[i] == 'dative':
            head_hold = sentence.head_text[i]
            for x in range(0, len(event_subj_act)):
                if head_hold == event_subj_act[x]:
                    event_iobj[x] = sentence.text_token[i]
                    x = len(event_subj_act)
                elif head_hold == event_pobj[x]:
                    event_iobj[x] = sentence.text_token[i]
                    x = len(event_subj_act)
            if (i + 1) < len(sentence.dep):
                if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                    # Multiple Subj
                    test_io = sentence.text_token[i]
                    isAdded = False

                    for k in range(0, len(sentence.dep)):
                        if (i + k) < len(sentence.dep):
                            if sentence.dep[i + k] == 'conj':
                                print("event_iobj: ", len(event_iobj), event_iobj)
                                if isAdded is False:
                                    print("test", test_io)
                                    event_iobj.append(test_io)
                                    isAdded = True
                                print("event_iobj: ", len(event_iobj), event_iobj)
                                if sentence.head_text[i + k] == event_iobj[len(event_iobj) - 1]:
                                    event_iobj[len(event_iobj) - 1] += "," + sentence.text_token[i + k]
                                    print("event_iobj: ", len(event_iobj), event_iobj)
        elif sentence.dep[i] == 'amod':
            isadv = False

            if (i + 1) < len(sentence.dep):
                if sentence.dep[i + 1] == 'npadvmod' or sentence.dep[i + 1] == 'advmod':
                    print("don't add anymore")
                    isadv = True

            if isadv is False:
                isFound_char_amod = False
                test = ""
                event_type.insert(0, 1)
                event_dobj.insert(0, '-')
                event_iobj.insert(0, '-')  #### I ADDED THIS LINE -CELINA (MARY HAD A RED DRESS)
                event_prep.insert(0, '-')
                event_pobj.insert(0, '-')
                event_detail.insert(0, '-')
                if (i + 2) < len(sentence.dep):
                    if sentence.dep[i + 2] == 'cc':
                        if (i + 3) < len(sentence.dep):
                            if sentence.dep[i + 3] == 'neg':
                                if (i + 4) < len(sentence.dep):
                                    if sentence.dep[i + 4] == 'amod':
                                        print("not connected")
                            elif sentence.dep[i + 3] == 'amod':
                                print("not connected")
                            elif sentence.dep[i + 3] == 'conj':
                                # print("I added it here")
                                event_subj.insert(0, sentence.head_text[i] + "," + sentence.text_token[i + 3])
                                test = sentence.head_text[i] + "," + sentence.text_token[i + 3]
                                isFound_char_amod = True

                if isFound_char_amod is False:
                    event_subj.insert(0, sentence.head_text[i])
                    test = sentence.head_text[i]

                if test in plural:
                    event_subj_act.insert(0, 'are')
                elif ',' in test:
                    event_subj_act.insert(0, 'are')
                else:
                    event_subj_act.insert(0, 'is')
                event_attr.insert(0, sentence.text_token[i])
                head_hold = sentence.text_token[i]
                if (i + 2) < len(sentence.dep):
                    if sentence.dep[i + 1] == 'cc' or sentence.dep[i + 1] == 'punct':
                        test_attr = sentence.text_token[i + 2]
                        for x in range(0, len(sentence.dep)):
                            if sentence.dep[x] == 'conj' and head_hold == sentence.head_text[x]:
                                head_hold = sentence.head_text[x]
                                event_attr[0] += ',' + sentence.text_token[x]

        elif sentence.dep[i] == 'advcl':
            if sentence.dep[i - 1] != 'nsubj':
                print("not added anymore")
            else:
                event_type.append(0)
                event_subj_act.append(sentence.text_token[i])
                event_dobj.append('-')
                event_iobj.append('-')
                event_pobj.append('-')
                event_prep.append('-')
                event_attr.append('-')
                event_detail.append('-')
        elif sentence.dep[i] == 'oprd':
            head_hold = sentence.head_text[i]
            for z in range(0, len(event_subj_act)):
                if head_hold == event_subj_act[z] and event_detail[z] == '-':
                    event_detail[z] = sentence.text_token[i]
                    z = len(event_subj_act)

        # ----END OF SPECIAL CASES----#

    # for checking
    for i in range(0, len(event_subj_act)):
        print("----Event Frame:----")
        print("Event Type: ", event_type)
        print("Subject: ", event_subj)
        print("Action: ", event_subj_act)
        print("Direct Object: ", event_dobj)
        print("Indirect Object: ", event_iobj)
        print("Preposition: ", event_prep)
        print("Object of Preposition: ", event_pobj)
        print("Attribute: ", event_attr)
        print("Detail: ", event_detail)
        print("-------------------")

    for x in range(0, len(event_type)):
        add_event(event_type, event_subj, event_subj_act, event_prep, event_pobj, event_detail, event_dobj, event_attr,
                  event_iobj,
                  event_create, world)


# Add event to the world
def add_event(type, subj, subj_act, prep, pobj, detail, dobj, attr, iobj, create, world):
    list_char = world.characters
    subj_hold = list()
    text_hold = list()
    dobj_hold = list()
    iobj_hold = list()
    attr_hold = list()
    crt_hold = list()
    print("list_char: ", list_char)
    list_obj = world.objects
    print("list_obj: ", list_obj)
    isHere = False

    for x in range(0, len(type)):
        while len(dobj_hold) > 0:
            dobj_hold.pop()
        while len(iobj_hold) > 0:
            iobj_hold.pop()
        while len(attr_hold) > 0:
            attr_hold.pop()
        while len(subj_hold) > 0:
            subj_hold.pop()

        if type[x] == 0:
            new_eventframe = EventFrame(len(world.event_chain), FRAME_EVENT)
        elif type[x] == 1:
            new_eventframe = EventFrame(len(world.event_chain), FRAME_DESCRIPTIVE)
        elif type[x] == 2:
            new_eventframe = EventFrame(len(world.event_chain), FRAME_CREATION)

        if subj:
            hold = subj.pop(0)
            if ',' in hold:
                subj_hold = hold.split(',')
            else:
                subj_hold.append(hold)
            print(subj_hold)
            for i in range(0, len(subj_hold)):
                print(subj_hold[i])
                if subj_hold[i].lower().find("'s") != -1:
                    text_hold = subj_hold[i].lower().split(" ")

                    if text_hold[1].lower() in list_obj:
                        new_eventframe.subject.append(text_hold[1].lower())
                        isHere = True
                    elif text_hold[1].lower() in list_char:
                        new_eventframe.subject.append(text_hold[1].lower())
                        isHere = True
                    else:
                        isHere = False
                elif subj_hold[i].lower() in list_obj:
                    new_eventframe.subject.append(subj_hold[i].lower())
                    isHere = True
                elif subj_hold[i].lower() in list_char:
                    new_eventframe.subject.append(subj_hold[i].lower())
                    isHere = True
                else:
                    isHere = False

            if isHere is True:
                if new_eventframe.event_type is FRAME_EVENT:
                    if x < len(subj_act):
                        new_eventframe.action = subj_act[x]
                    if prep[x] != '-':
                        new_eventframe.preposition = prep[x]
                    if pobj[x] != '-':
                        new_eventframe.obj_of_preposition = pobj[x]
                    if dobj[x] != '-':
                        hold_o = dobj[x]
                        if ',' in hold_o:
                            dobj_hold = hold_o.split(',')
                        else:
                            dobj_hold.append(hold_o)

                        for y in range(0, len(dobj_hold)):
                            if dobj_hold[y].lower() in list_obj:
                                new_eventframe.direct_object.append(dobj_hold[y].lower())
                            elif dobj_hold[y].lower() in list_char:
                                new_eventframe.direct_object.append(dobj_hold[y].lower())
                    if iobj[x] != '-':
                        hold_o = iobj[x]
                        if ',' in hold_o:
                            iobj_hold = hold_o.split(',')
                        else:
                            iobj_hold.append(hold_o)

                        for y in range(0, len(iobj_hold)):
                            if iobj_hold[y].lower() in list_obj:
                                new_eventframe.indirect_object.append(iobj_hold[y].lower())
                            elif iobj_hold[y].lower() in list_char:
                                new_eventframe.indirect_object.append(iobj_hold[y].lower())
                    if detail[x] != '-':
                        new_eventframe.adverb = detail[x]
                elif new_eventframe.event_type is FRAME_DESCRIPTIVE:
                    if attr:
                        hold_a = attr[x]
                        if ',' in hold_a:
                            attr_hold = hold_a.split(',')
                        else:
                            attr_hold.append(hold_a)

                        for y in range(0, len(attr_hold)):
                            if attr_hold[y] != '-':
                                new_eventframe.attributes.append(attr_hold[y].lower())

                elif new_eventframe.event_type is FRAME_CREATION:
                    if attr:
                        hold_a = attr[x]
                        if ',' in hold_a:
                            attr_hold = hold_a.split(',')
                        else:
                            attr_hold.append(hold_a)

                        for y in range(0, len(attr_hold)):
                            if attr_hold[y] != '-':
                                new_eventframe.attributes.append(attr_hold[y].lower())

                isHere = False
                world.add_eventframe(new_eventframe)

    print(world.event_chain)

# get label of given entity
def get_entity_label(sent, entity):
    for i in range(len(sent.text_ent)):
        if entity.lower() in str(sent.text_ent[i]).lower():
            return sent.label[i]
    
    return None

def get_text_ents(sent, entity):
    for i in range(len(sent.text_ent)):
        if entity.lower() in str(sent.text_ent[i]).lower():
            return sent.text_ent[i]
    
    return None

# check for unkown word one by one
def find_unkown_word(sent):
    ignore = ["kill", "murder", "suicide", "sex", "rape", "war", "torture", "die", "stab", "penis", "dick", "vagina", "boobs", "breast", 
            "nobody", "none", "every", "any", "some", "other", "something", "anything", "nothing", "everything", "all", "this", "that", 
            "these", "those", "who", "what", "when", "where", "which", "why"]

    # print("ENTER find_unkown_word")
    for i in range(len(sent.lemma)):
        if str(sent.pos[i]).lower() == "noun" or str(sent.pos[i]).lower() == "propn":
            # check if word exists in global knowledge base
            if DBO_Concept.get_word_concept(sent.lemma[i]) == []:
                # check if word exists in local knowledge base
                if DBO_Local_Concept.get_word_concept(sent.lemma[i]) == []:
                    # if the word is not a name of a character
                    ent_label = get_entity_label(sent, sent.text_token[i])
                    if sent.lemma[i] not in ignore:
                        if ent_label != None:
                            if ent_label != "PERSON":
                                print("New Unkown Word: " + sent.lemma[i])
                                return sent.lemma[i]
                        else:
                            print("New Unkown Word: " + sent.lemma[i])
                            return sent.lemma[i]

    print("Found None")
    return None

def find_token_index(sent, token):
    for i in range(len(sent.text_token)):
        if sent.text_token[i] == token:
            return i
    
    return -1

def extract_instance_of(sent, first_word):
    # check for compound words in first_word
    first_entity = get_entity_label(sent, first_word)
    if first_entity == "GPE" or first_entity == "LOC":
        # add proper nouns to InstanceOf
        return Relation.Relation(-1, "InstanceOf", first_word, "", "location")
    elif first_entity == "PERSON" or first_word.lower() == "-pron-":
        if first_word.lower() != "-pron-":
            # add proper nouns to InstanceOf
            return Relation.Relation(-1, "InstanceOf", first_word, "", "character")
    return None

def extract_conj_index(sent, char_index):
    characters = []
    characters.append(char_index)
    mark = ["punct", "cc", "conj"]

    for index in range(char_index + 1, len(sent.dep)):
        if sent.dep[index] == "conj" and sent.head_text[index] == sent.text_token[char_index]:
            characters.append(index)
        if sent.dep[index] not in mark:
            break
    
    return characters

# extract all possible relations from input based on templates
def extract_relation(sent, world, ie_fileWriter):
    print("ENTER extract_relation function")
    ie_fileWriter.write("Extracted at extract_relation \n")

    # get unique first of templates
    templates_first = DBO_Relation.get_unique_first()

    first_index = 0
    second_index = 0
    extracted = []
    be_verb = ["be", "can", "could", "have", "will", "would"]
    ignore = ["kill", "murder", "suicide", "sex", "rape", "war", "torture", "die", "stab", "penis", "dick", "vagina", "boobs", "breast", 
            "nobody", "none", "every", "any", "some", "other", "something", "anything", "nothing", "everything", "all", "this", "that", 
            "these", "those", "who", "what", "when", "where", "which", "why"]

    # loop through the dependencies of input
    while first_index < len(sent.dep):
        second_word = ""
        character_index_list = []
        character_list = []
        adj_list = []
        relation = None
        flag = False
        
        # check dependency from sentence if it matches any of the first from tempates
        # if there is a match and it is not an ignore word
        if sent.dep[first_index] in templates_first and sent.lemma[first_index] != "-PRON-" and sent.lemma[first_index] not in ignore and sent.lemma[first_index] not in be_verb :
            # for amod amod noun cases
            if sent.dep[first_index] == "amod":
                adj_list.append(compound_extraction(sent, sent.lemma[first_index]))
                while sent.dep[first_index + 1] == "amod":
                    first_index += 1
                    adj_list.append(compound_extraction(sent, sent.lemma[first_index]))

            # get second from templates where first
            templates_second = DBO_Relation.get_second_where_first(sent.dep[first_index])
            character_index_list = extract_conj_index(sent, first_index)
            for c_index in character_index_list:
                
                # check for compound words in first_word
                first_temp = compound_extraction(sent, sent.lemma[c_index])
                temp = extract_instance_of(sent, first_temp)
                if temp is not None:
                    extracted.append(temp)
                    print("appended 1: " + extracted[len(extracted)-1].__str__())
                    ie_fileWriter.write("appended 1: " + extracted[len(extracted)-1].__str__() + "\n")
                    if temp.second == "location":
                        first_temp = temp.first
                if (temp is None and sent.lemma[c_index] == "-PRON-") or (temp is not None and temp.second == "character"):
                    first_temp = "character"
                character_list.append(first_temp)

            for second_index in range(first_index + 1, len(sent.dep)):
                
                if sent.dep[second_index] == "punct" or sent.lemma[second_index] == "then":
                    break
                # check if dependency from sentence matches current second from template
                if sent.dep[second_index] in templates_second and sent.lemma[second_index] != "-PRON-" and \
                    sent.lemma[second_index] not in ignore and sent.lemma[second_index] not in be_verb and \
                        sent.lemma[first_index] != sent.lemma[second_index]:
                    templates_keywords = DBO_Relation.get_keywords(sent.dep[first_index], sent.dep[second_index])
                    templates_keyword_type = DBO_Relation.get_keyword_type(sent.dep[first_index], sent.dep[second_index])
                    
                    # get in between words 
                    actual_keywords_dep = sent.dep[first_index + 1 : second_index]
                    actual_keywords_lem = sent.lemma[first_index + 1 : second_index]
                    
                    if len(character_index_list) > 1:
                        actual_keywords_dep = sent.dep[character_index_list[len(character_index_list) - 1] + 1 : second_index]
                        actual_keywords_lem = sent.lemma[character_index_list[len(character_index_list) - 1] + 1 : second_index]

                    if "neg" not in actual_keywords_dep and ("no" not in actual_keywords_lem or "not" not in actual_keywords_lem):
                        # loop through all keywords
                        for templates_k_index in range(0, len(templates_keywords)):
                            if templates_keyword_type[templates_k_index] == 0:
                                actual_keywords = actual_keywords_dep
                            else:
                                actual_keywords = actual_keywords_lem
                                
                            # if actual is match to template keywords
                            if templates_keywords[templates_k_index] in actual_keywords or (templates_keywords[templates_k_index] == "" and actual_keywords == []):
                                # check for compound words in second_word
                                second_word = compound_extraction(sent, sent.lemma[second_index])
                                temp = extract_instance_of(sent, second_word)
                                if temp is not None:
                                    extracted.append(temp)
                                    print("appended 2: " + extracted[len(extracted)-1].__str__())
                                    ie_fileWriter.write("appended 2: " + extracted[len(extracted)-1].__str__() + "\n")
                                    if temp.second == "location":
                                        second_word = temp.first
                                if (temp is None and sent.lemma[second_index] == "-PRON-") or (temp is not None and temp.second == "character"):
                                    second_word = "character"

                                # save new extracted relation
                                relation  = DBO_Relation.get_matching_relation_pattern(sent.dep[first_index], templates_keywords[templates_k_index], sent.dep[second_index])
                                if relation is not None:
                                    if relation.third != "":
                                        if second_index < len(sent.dep) - 1:
                                            if relation.third == sent.dep[second_index + 1]:
                                                second_index += 1
                                                second_word += " " + sent.lemma[second_index]
                                            if relation.third == sent.dep[second_index - 1]:
                                                second_word = sent.lemma[second_index - 1] + " " + second_word

                                    if relation.first == "amod" and len(adj_list) > 1:
                                        character_list = adj_list
                                    for first in character_list:
                                        # for cases that relations should be flipped ex. beautiful flower -> HasProperty(flower, beautiful)
                                        if relation.is_flipped == 'y':
                                            extracted.append(Relation.Relation(relation.id, relation.relation, second_word, relation.keywords, first))
                                            print("appended 3: " + extracted[len(extracted)-1].__str__())
                                            ie_fileWriter.write("appended 3: " + extracted[len(extracted)-1].__str__() + "\n")
                                        else:
                                            extracted.append(Relation.Relation(relation.id, relation.relation, first, relation.keywords, second_word))
                                            print("appended 4: " + extracted[len(extracted)-1].__str__())
                                            ie_fileWriter.write("appended 4: " + extracted[len(extracted)-1].__str__() + "\n")

                                    if not (relation.relation == "HasProperty" and relation.first == "amod"):
                                        while (second_index + 2 < len(sent.dep) and sent.dep[second_index + 2] == "conj" and sent.pos[second_index + 2] == sent.pos[second_index]) or \
                                            (second_index + 3 < len(sent.dep) and sent.dep[second_index + 3] == "conj" and sent.pos[second_index + 3] == sent.pos[second_index]):
                                            second_index += 1
                                            while sent.dep[second_index] != "conj":
                                                second_index += 1
                                            
                                             # check for compound words in second_word
                                            second_word = compound_extraction(sent, sent.lemma[second_index])
                                            temp = extract_instance_of(sent, second_word)
                                            if temp is not None:
                                                extracted.append(temp)
                                                print("appended 5: " + extracted[len(extracted)-1].__str__())
                                                ie_fileWriter.write("appended 5: " + extracted[len(extracted)-1].__str__() + "\n")
                                                if temp.second == "location":
                                                    second_word = temp.first
                                            if (temp is None and sent.lemma[second_index] == "-PRON-") or (temp is not None and temp.second == "character"):
                                                second_word = "character"
                                                
                                            if relation.third != "":
                                                if second_index < len(sent.dep) - 1:
                                                    if relation.third == sent.dep[second_index + 1]:
                                                        second_index += 1
                                                        second_word += " " + sent.lemma[second_index]
                                                    if relation.third == sent.dep[second_index - 1]:
                                                        second_word = sent.lemma[second_index - 1] + " " + second_word

                                            for first in character_list:
                                                if relation.is_flipped == 'y':
                                                    extracted.append(Relation.Relation(relation.id, relation.relation, second_word, relation.keywords, first))
                                                    print("appended 6: " + extracted[len(extracted)-1].__str__())
                                                    ie_fileWriter.write("appended 6: " + extracted[len(extracted)-1].__str__() + "\n")
                                                else:
                                                    extracted.append(Relation.Relation(relation.id, relation.relation, first, relation.keywords, second_word))
                                                    print("appended 7: " + extracted[len(extracted)-1].__str__())
                                                    ie_fileWriter.write("appended 7: " + extracted[len(extracted)-1].__str__() + "\n")

                                flag = True
                                break
                if flag:
                    break
        first_index += 1

    for i in range(len(sent.label)):
        if sent.label[i] == "TIME":
            extracted.append(Relation.Relation(-1, "InstanceOf", sent.text_ent[i], "", "time"))
            print("appended 8: " + extracted[len(extracted)-1].__str__())
            ie_fileWriter.write("appended 8: " + extracted[len(extracted)-1].__str__() + "\n")

        if sent.label[i] == "DATE":
            extracted.append(Relation.Relation(-1, "InstanceOf", sent.text_ent[i], "", "date"))
            print("appended 9: " + extracted[len(extracted)-1].__str__())
            ie_fileWriter.write("appended 9: " + extracted[len(extracted)-1].__str__() + "\n")

    ie_fileWriter.write("\n")
    return extracted

# filter relations that do not exist in global knowledge base
def remove_existing_relations_global(extracted, ie_fileWriter):
    result = []

    for i in range(len(extracted)):
        if DBO_Concept.get_concept_specified(extracted[i].first, extracted[i].relation, extracted[i].second) == None:
            result.append(extracted[i])

    # print left in extracted list
    print("What's left after removing existing global relations")
    ie_fileWriter.write("What's left after removing existing global relations\n")
    for i in result:
        print(i.__str__())
        ie_fileWriter.write(i.__str__() + "\n")

    ie_fileWriter.write("\n")
    return result

# filter relations that do not exist in local knowledge base
def remove_existing_relations_local(userid, extracted, ie_fileWriter):
    # print("ENTER remove_existing_relations_local")
    result = []
    temp = None

    for i in range(len(extracted)):
        temp = DBO_Local_Concept.get_concept_specified(extracted[i].first, extracted[i].relation, extracted[i].second)
        # if concept does not exists in local append to list to be returned
        if temp == None:
            result.append(extracted[i])
        # else update it's score
        elif temp.valid == 1:
            if temp.userid != userid:
                ie_fileWriter.write("Updated score of this concept : " + temp.__str__() + "\n")
                DBO_Local_Concept.update_score(temp.id, temp.score + 2)
            if temp.score + 2 >= 5: # change the 5
                ie_fileWriter.write("Moved this concept from local to global : " + temp.__str__() + "\n")
                DBO_Concept.add_concept(Concept(0,temp.first, temp.relation, temp.second))
                DBO_Local_Concept.update_valid(temp.id, 0)
            temp = None

    # print left in extracted list
    print("What's left after removing existing local relations")
    ie_fileWriter.write("What's left after removing existing local relations \n")
    for i in result:
        print(i.__str__())
        ie_fileWriter.write(i.__str__() + "\n")

    
    ie_fileWriter.write("\n")
    return result

# add new relations to local knowledge base
def add_relations_to_local(userid, extracted):
    # print("ENTER add_relations_to_local")
    temp = None
    for i in range(len(extracted)):
        if DBO_Local_Concept.get_concept_specified(extracted[i].first, extracted[i].relation, extracted[i].second) == None:
            temp = Local_Concept(0, userid, extracted[i].first, extracted[i].relation, extracted[i].second, 0, 1)
            DBO_Local_Concept.add_concept(temp)
