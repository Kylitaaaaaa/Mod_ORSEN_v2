import spacy
from src.objects.ServerInstance import ServerInstance
from src.objects.storyworld.World import World
from src.inputprocessor import infoextraction
from src.dialoguemanager import DialoguePlanner
from src.dialoguemanager.story_generation import generate_basic_story, generate_collated_story

server = ServerInstance()
#Loading of text and segmentation of sentences
nlp = spacy.load('en_coref_sm')
doc = nlp(u'My sister has a dog. She loves him.')
print(doc._.coref_clusters)
result = None
prompt_unknown = 0

def get_unkown_word():
    return result

def new_world(id):
    global world_id
    world_id = id
    server.new_world(world_id)

def extract_info(userid, text, ie_fileWriter):
    global result, prompt_unknown
    if result != None and result.lower() in str(text[len(text)-1]).lower():
        result = None
        prompt_unknown = 0
    elif result != None and prompt_unknown < 2:
        prompt_unknown = prompt_unknown + 1
    else:
        prompt_unknown = 0
        result = None

    world = server.get_world(world_id)
    document_curr = nlp(str(text[len(text)-1]))
    sentences = [sent.string.strip() for sent in document_curr.sents]
    if len(text) > 1:
        document_prev = nlp(str(text[len(text)-2]))
        sentences_prev = [sent.string.strip() for sent in document_prev.sents]
        sentences = sentences_prev + sentences
    list_of_sentences = []
    list_of_sent = []
    characters = []

    # Part-Of-Speech, NER, Dependency Parsing
    for sent in sentences:
        sent = nlp(sent) # go thru spacy
        list_of_sentences.append(infoextraction.pos_ner_nc_processing(sent, ie_fileWriter))

    for curr in range (0, len(list_of_sentences)):
        # DetailsExtraction
        if curr == 0:
            sentences[curr] = infoextraction.coref_resolution(list_of_sentences[curr], sentences[curr], sentences[curr], world, True, ie_fileWriter)
        else:
            sentences[curr] = infoextraction.coref_resolution(list_of_sentences[curr], sentences[curr], sentences[curr - 1], world, False, ie_fileWriter)

    for curr in sentences:
        s = nlp(curr)
        list_of_sent.append(infoextraction.pos_ner_nc_processing(s, ie_fileWriter))

    for s in list_of_sent:
        infoextraction.details_extraction(s, world, "ROOT")
        infoextraction.event_extraction(s, world, "ROOT")

    print("-------- CHARACTERS")
    for c in world.characters:
        print(world.characters[c])
        for a in world.characters[c].attributes:
            print("attr", a.relation, a.name, a.isNegated)

    print("-------- OBJECTS")
    for c in world.objects:
        print(world.objects[c])
        for a in world.objects[c].attributes:
            print("attr", a.relation, a.name, a.isNegated)

    print("-------- SETTINGS")
    for s in world.settings:
        print(world.settings[s])

    print("-------- EVENT CHAIN")
    for e in world.event_chain:
        print(str(e))

    # For Event Extraction
    seq_no = []
    event_type = []
    doer = []
    doer_act = []
    rec = []
    rec_act = []
    location = []
    event_frame = [seq_no, event_type, doer, doer_act, rec, rec_act, location]

    for sent in list_of_sent:
        extracted = None
        
        # extract all possible relations from sentence input
        extracted = infoextraction.extract_relation(sent, world, ie_fileWriter)

        # remove relations that already exist in the global kb
        extracted = infoextraction.remove_existing_relations_global(extracted, ie_fileWriter)

        # remove relations that already exist in the local kb
        extracted = infoextraction.remove_existing_relations_local(userid, extracted, ie_fileWriter)

        # add new relations to local kb
        if extracted != []:
            infoextraction.add_relations_to_local(userid, extracted)
        else:
            temp = infoextraction.find_unkown_word(sent) 
            if temp != None:
                prompt_unknown = prompt_unknown + 1
                result = temp

    return sentences[len(sentences)-1]


'''
output = "Hello, I am ORSEN. Let's start."
retrieved = None
world_id = "0"
new_world(world_id)
while True:
    if retrieved is not None:
        output = retrieved.get_string_response()
        print("IN: "+text)
    text = input("OUT: " + output + "\n")

    if infoextraction.getCategory(text) == infoextraction.CAT_STORY:
        extract_info(text)

    #dialogue
    retrieved = DialoguePlanner.retrieve_output(text, world_id)

    if retrieved.type_num == DialoguePlanner.MOVE_HINT:
        extract_info(retrieved.get_string_response())

    if text == "The end":
        print("FINAL STORY -----------------")
        print(generate_collated_story(server.get_world(world_id)))
        print("-----------------------------")
'''