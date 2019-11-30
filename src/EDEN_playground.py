from EDEN.OCC.OCCManager import OCCManager
from EDEN.constants import *
from EDEN.db import DBOEmotion
from EDEN.models import EmotionActionEvent
from src.ORSEN import ORSEN, EVENT_CREATION, CreationEvent, EVENT_DESCRIPTION, EVENT_ACTION, ActionEvent
from src import Logger
import pickle
import datetime

from src.models import World
from src.models.elements import Object, Attribute, Setting, Character
import time
import csv


def test_eden():
    response = ["I loved you too much to let you die, dear sister, but your heart was failing you, so I gave you mine.",
                "He started worrying if he was important and decided he wanted to ask the people he knew if they thought he was important",
                "They all ignored him and he was very confused on why this was happening.",
                "As people gathered ’round him, singing loudly, shining bright lights everywhere, he kept his eyes on the light blue horizon.",
                "Smile, after all, it is Christmas and you have no reason to not smile on Christmas.",
                "Breathing heavily, Arabella lurched forwards, bearing her sword.",
                "I must congratulate you on your victory",
                "You think that I am his true love?",
                "I will do my best to save our Prince.",
                "She cried out as the sword flew from her grasp.",
                "I have broken our promise and cannot help you anymore.",
                "As soon as I saw him I knew it was a match made in heaven.",
                "Hansel got angry with Gretel",
                "I fought, endured, and cried my way to my degree.",
                "I thought he might miss the flight but I suddenly found him on the plane."]

    # response = ["I thought he might miss the flight but I suddenly found him on the plane."]

    Logger.setup_loggers()


    for X in response:
        orsen.perform_text_understanding(X)
        # emotion = orsen.get_emotion(X)



        Logger.dump_log("=======================================")

    print("DONE CHECKING")

def test_open_pickle(date, dogs_dict):
    with open('../logs/user world/' + date, 'wb') as f:
        pickle.dump(object, f)
        f.close()
    # outfile = open(filename, 'wb')
    #
    # pickle.dump(dogs_dict, outfile)
    # outfile.close()

def test_read_pickle(filepath):
    # with open('../logs/user world/' + date, 'rb') as f:
    new_dict = None
    try:

        with open(filepath, 'rb') as f:
            new_dict = pickle.load(f)
            f.close()
    except:
        print("File not found")



    return new_dict

def test_pickle():
    date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    filename = date
    dogs_dict = {'Ozzy': 3, 'Filou': 8, 'Luna': 5, 'Skippy': 10, 'Barco': 12, 'Balou': 9, 'Laika': 16}
    test_open_pickle(date, dogs_dict)
    test_read_pickle(date, dogs_dict)

    dogs_dict = {'Ozzy': 3}
    test_open_pickle(date, dogs_dict)
    test_read_pickle(date, dogs_dict)


def test_occ_model():
    # occ_manager = OCCManager()

    #shame
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_DISPLEASED,
                           sp=SP_UNDESIRABLE,
                           sa=SA_BLAME,
                           vr=VR_TRUE)
    print_emotion(OCC_SHAME, occ_manager.choose_emotion())

    # disappointment
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_DISPLEASED,
                           sp=SP_DESIRABLE,
                           pros=PROS_POSITIVE,
                           stat=STAT_DISCONFIRMED,
                           vr=VR_TRUE)
    print_emotion(OCC_DISAPPOINTMENT, occ_manager.choose_emotion())

    # distress
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_DISPLEASED,
                           sp=SP_UNDESIRABLE,
                           vr=VR_TRUE)
    print_emotion(OCC_DISTRESS, occ_manager.choose_emotion())

    # fear
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_DISPLEASED,
                           sp=SP_UNDESIRABLE,
                           pros=PROS_NEGATIVE,
                           stat=STAT_UNCONFIRMED,
                           vr=VR_TRUE)
    print_emotion(OCC_FEAR, occ_manager.choose_emotion())

    # fear confirmed
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_DISPLEASED,
                           sp=SP_UNDESIRABLE,
                           pros=PROS_NEGATIVE,
                           stat=STAT_CONFIRMED,
                           vr=VR_TRUE)
    print_emotion(OCC_FEARS_CONFIRMED, occ_manager.choose_emotion())

    # pride
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_PLEASED,
                           sp=SP_DESIRABLE,
                           sa=SA_PRAISE,
                           vr=VR_TRUE)
    print_emotion(OCC_PRIDE, occ_manager.choose_emotion())

    # admiration
    occ_manager.set_values(de=DE_OTHERS,
                           sr=SR_PLEASED,
                           op=OP_DESIRABLE,
                           sa=SA_PRAISE,
                           vr=VR_TRUE)
    print_emotion(OCC_ADMIRATION, occ_manager.choose_emotion())

    # hate
    occ_manager.set_values(de=DE_OTHERS,
                           of=OF_NOT_LIKED,
                           oa=OA_NOT_ATTRACTIVE,
                           sr=SR_DISPLEASED,
                           sp=SP_UNDESIRABLE,
                           vr=VR_TRUE)
    print_emotion(OCC_HATE, occ_manager.choose_emotion(event_valence=VADER_NEGATIVE))

    # joy
    occ_manager.set_values(sr=SR_PLEASED,
                           sp=SP_DESIRABLE,
                           vr=VR_TRUE)
    print_emotion(OCC_JOY, occ_manager.choose_emotion())

    # love
    occ_manager.set_values(de=DE_OTHERS,
                           of=OF_LIKED,
                           oa=OA_ATTRACTIVE,
                           sr=SR_PLEASED,
                           sp=SP_DESIRABLE,
                           vr=VR_TRUE)
    print_emotion(OCC_LOVE, occ_manager.choose_emotion(event_valence=VADER_POSITIVE))

    # relief
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_PLEASED,
                           sp=SP_UNDESIRABLE,
                           pros=PROS_NEGATIVE,
                           stat=STAT_DISCONFIRMED,
                           vr=VR_TRUE)
    print_emotion(OCC_RELIEF, occ_manager.choose_emotion())

    # resentment
    occ_manager.set_values(af=AF_NOT_LIKED,
                           de=DE_OTHERS,
                           sr=SR_DISPLEASED,
                           op=OP_DESIRABLE,
                           vr=VR_TRUE)
    print_emotion(OCC_RESENTMENT, occ_manager.choose_emotion())

    # hope
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_PLEASED,
                           sp=SP_DESIRABLE,
                           pros=PROS_POSITIVE,
                           stat=STAT_UNCONFIRMED,
                           vr=VR_TRUE)
    print_emotion(OCC_HOPE, occ_manager.choose_emotion())

    # satisfaction
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_PLEASED,
                           sp=SP_DESIRABLE,
                           pros=PROS_POSITIVE,
                           stat=STAT_CONFIRMED,
                           vr=VR_TRUE)
    print_emotion(OCC_SATISFACTION, occ_manager.choose_emotion())

    # sorry for
    occ_manager.set_values(af=AF_LIKED,
                           de=DE_OTHERS,
                           sr=SR_DISPLEASED,
                           op=OP_UNDESIRABLE,
                           vr=VR_TRUE)
    print_emotion(OCC_SORRY_FOR, occ_manager.choose_emotion())

    ###COMPLEX EMOTIONS
    # gratification
    # joy + pride
    occ_manager.set_values(sr=SR_PLEASED,
                           sp=SP_DESIRABLE,
                           de=DE_SELF,
                           sa=SA_PRAISE,
                           vr=VR_TRUE)
    print_emotion(OCC_GRATIFICATION, occ_manager.choose_emotion())

    # remorse
    # distress + shame
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_DISPLEASED,
                           sp=SP_UNDESIRABLE,
                           sa=SA_BLAME,
                            vr=VR_TRUE)
    print_emotion(OCC_REMORSE, occ_manager.choose_emotion())

    # gratitude
    #joy + admiration
    occ_manager.set_values(sr=SR_PLEASED,
                           sp=SP_DESIRABLE,
                           de=DE_OTHERS,
                           op=OP_DESIRABLE,
                           sa=SA_PRAISE,
                           vr=VR_TRUE)
    print_emotion(OCC_ADMIRATION, occ_manager.choose_emotion())

    # shock
    occ_manager.set_values(de=DE_SELF,
                           sr=SR_DISPLEASED,
                           sp=SP_UNDESIRABLE,
                           unexp=UNEXP_TRUE,
                           vr=VR_TRUE)
    print_emotion(OCC_SHOCK, occ_manager.choose_emotion())

    # surprise
    occ_manager.set_values(sr=SR_PLEASED,
                           sp=SP_DESIRABLE,
                           unexp=UNEXP_TRUE,
                           vr=VR_TRUE)
    print_emotion(OCC_SURPRISE, occ_manager.choose_emotion())


def print_emotion(expected_emotion, chosen_emotion_list):
    print("==== EXPECTING: ", expected_emotion, "====")
    if len(chosen_emotion_list) > 0:
        str = ""
        for emotion in chosen_emotion_list:
            str = str + "\t" + emotion.emotion
        print("CANDIDATE EMOTIONS ARE: ", str)
        print("SELECTED EMOTION: ", occ_manager.get_final_emotion(chosen_emotion_list).emotion)
    else:
        print("NO EMOTION FOUND")
    print("===============================")


def convert_pickle_to_world(curr_pickle):
    world_list = []
    for world in curr_pickle:

        print("Objects: ", len(world[0]) )
        #extract objects
        objects = []
        for object in world[0]:
            objects.append(get_unpickled_object(object))

        print("Char: ", len(world[1]))
        #extract char
        characters = []
        for character in world[1]:
            characters.append(get_unpickled_character(character))

        print("Setting: ", len(world[2]))
        #extract setting
        settings = []
        for setting in world[2]:
            settings.append(get_unpickled_setting(setting))

        print("Events: ", len(world[3]))
        #extract event
        events = []
        for event in world[3]:
            events.append(get_unpickled_event(event))

        print("Emotion Event: ", len(world[4]))
        #extract emotion event
        emotion_events = []
        for emotion_event in world[4]:
            emotion_events.append(get_unpickled_emotion_event(emotion_event))

        # curr_world = World()

        curr_world = World(objects = objects,
              characters = characters,
              settings = settings,
              event_chains = events,
              emotion_events = emotion_events)

        print(curr_world)
        world_list.append(curr_world)
    return world_list



def get_unpickled_object(pickled_object):
    attributes = []

    for attribute in pickled_object.attribute:
        attributes.append(get_unpickled_attribute(attribute))

    settings = []
    for setting in pickled_object.setting:
        settings.append(get_unpickled_setting(setting))

    return Object(id = pickled_object.id,
                  name = pickled_object.name,
                  attribute= attributes,
                  in_setting= settings,
                  mention_count= pickled_object.mention_count)

def get_unpickled_attribute(pickled_attribute):
    return Attribute(pickled_attribute.relation,
                     pickled_attribute.description,
                     pickled_attribute.is_negated,
                     keyword=pickled_attribute.keyword)

def get_unpickled_setting(pickled_setting):
    return Setting(pickled_setting.type, pickled_setting.value)

def get_unpickled_character(pickled_character):
    types = []
    for type in pickled_character.type:
        types.append(get_unpickled_attribute(type))

    settings = []
    for setting in pickled_character.in_setting:
        settings.append(get_unpickled_setting(setting))

    return Character(id = pickled_character.id,
                     name = pickled_character.name,
                     type=[],
                     attribute = types,
                     in_setting = settings,
                     mention_count = pickled_character.mention_count,
                     gender = pickled_character.gender)

def get_unpickled_char_obj (pickled):
    print("picked thing is: ", type(pickled))
    if pickled is not None:
        if pickled.pickled_char_obj == 'Object':
            return get_unpickled_object(pickled)
        elif pickled.pickled_char_obj == 'Character':
            return get_unpickled_character(pickled)
    return None

def get_unpickled_event(pickled_event):
    if pickled_event.type == EVENT_CREATION or pickled_event.type == EVENT_DESCRIPTION:
        attributes = []
        for attribute in pickled_event.attributes:
            attributes.append(get_unpickled_attribute(attribute))

        return CreationEvent(pickled_event.sequence_number,
                             get_unpickled_char_obj(pickled_event.subject),
                             attributes)

    elif pickled_event.type == EVENT_ACTION:
        return ActionEvent(pickled_event.sequence_number,
                           get_unpickled_char_obj(pickled_event.subject),
                           pickled_event.verb,
                           get_unpickled_char_obj(pickled_event.direct_object),
                           pickled_event.adverb,
                           pickled_event.preposition,
                           get_unpickled_char_obj(pickled_event.object_of_preposition))


def get_unpickled_emotion_event(pickled_event):
    return EmotionActionEvent(get_unpickled_event(pickled_event),
                              emotion =pickled_event.emotion,
                              af=pickled_event.af,
                              de=pickled_event.de,
                              of=pickled_event.of,
                              oa=pickled_event.oa,
                              sp=pickled_event.sp,
                              sr=pickled_event.sr,
                              op=pickled_event.op,
                              pros=pickled_event.pros,
                              stat=pickled_event.stat,
                              unexp=pickled_event.unexp,
                              sa=pickled_event.sa,
                              vr=pickled_event.vr,
                              ed=pickled_event.ed,
                              eoa=pickled_event.eoa,
                              edev=pickled_event.edev,
                              ef=pickled_event.ef)

"""LOG EXTRACTOR"""
def extract_convo(file_path):
    file_path = file_path + 'conv.txt'
    user_resp = []
    orsen_resp = []
    user_orsen_resp = []
    orsen_dmoves = []

    user_lat = []
    orsen_lat = []
    user_orsen_lat = []

    f = open(file_path, "r")
    for X in f:
        if "???: " in X:
            user_resp.append(X.split("???: ", 1)[1].replace('\n', ''))
            user_orsen_resp.append(X.split("???: ", 1)[1].replace('\n', ''))
            orsen_dmoves.append('')
        elif "User : " in X:
            user_resp.append(X.split("User : ", 1)[1].replace('\n', ''))
            user_orsen_resp.append(X.split("User : ", 1)[1].replace('\n', ''))
            orsen_dmoves.append('')
        elif "ORSEN: " in X:
            orsen_resp.append(X.split("ORSEN: ", 1)[1].replace('\n', ''))
            user_orsen_resp.append(X.split("ORSEN: ", 1)[1].replace('\n', ''))
        elif "EDEN: " in X:
            orsen_resp.append(X.split("EDEN: ", 1)[1].replace('\n', ''))
            user_orsen_resp.append(X.split("EDEN: ", 1)[1].replace('\n', ''))
        elif "EREN: " in X:
            orsen_resp.append(X.split("EREN: ", 1)[1].replace('\n', ''))
            user_orsen_resp.append(X.split("EREN: ", 1)[1].replace('\n', ''))
        elif "USER LATENCY TIME (seconds): " in X:
            user_lat.append(float(X.split("USER LATENCY TIME (seconds): ", 1)[1].replace('\n', '')))
            user_orsen_lat.append(float(X.split("USER LATENCY TIME (seconds): ", 1)[1].replace('\n', '')))
        elif "ORSEN LATENCY TIME (seconds): " in X:
            orsen_lat.append(float(X.split("ORSEN LATENCY TIME (seconds): ", 1)[1].replace('\n', '')))
            user_orsen_lat.append(float(X.split("ORSEN LATENCY TIME (seconds): ", 1)[1].replace('\n', '')))
        elif "CHOSEN DIALOGUE MOVE: " in X:
            move_to_add = X.split("CHOSEN DIALOGUE MOVE: ", 1)[1].replace('\n', '')
            if move_to_add == 'e-label':
                orsen_dmoves.append('Labelling')
            elif move_to_add == 'e-pumping':
                orsen_dmoves.append('Emotion')
            elif move_to_add == 'c-pumping':
                orsen_dmoves.append('Cause')
            elif move_to_add == 'd-praise':
                orsen_dmoves.append('Praise')
            elif move_to_add == 'e-emphasis':
                orsen_dmoves.append('Emphasis')
            elif move_to_add == 'd-correcting':
                orsen_dmoves.append('Corrective')
            elif move_to_add == 'd-pumping':
                orsen_dmoves.append('Discipline')
            elif move_to_add == 'evaluation':
                orsen_dmoves.append('Evaluating')
            elif move_to_add == 'recollection':
                orsen_dmoves.append('Recollecting')
            elif move_to_add == 'e-followup':
                orsen_dmoves.append('Followup')
            elif move_to_add == 'general':
                orsen_dmoves.append('General')
            elif move_to_add == 'specific':
                orsen_dmoves.append('Specific')




    # print("===PRINTING USER RESPONSES===")
    # print_list(user_resp)
    # print("===PRINTING ORSEN RESPONSES===")
    # print_list(orsen_resp)
    # print("===PRINTING USER LATENCY===")
    # print_list(user_lat)
    # print("===PRINTING ORSEN LATENCY===")
    # print_list(orsen_lat)
    print("===PRINTING USER ORSEN RESPONSES===")
    print_list(user_orsen_resp)
    print("===PRINTING USER ORSEN LATENCY===")
    print_list(user_orsen_lat)
    print("===PRINTING ORSEN MOVES===")
    print_list(orsen_dmoves)

    return user_resp, orsen_resp, user_orsen_resp, user_lat, orsen_lat, orsen_dmoves
    # return user_orsen_resp

def print_list(list):
    for X in list:
        print(X)


def get_time(file_path):
    file_path = file_path + 'conv.txt'
    user_orsen_lat = []

    f = open(file_path, "r")
    for X in f:
        if " - ???: " in X:
            temp_time = X.split(" - ???:", 1)[0]
            user_orsen_lat.append(time.strptime(temp_time, '%m-%d-%y %H:%M:%S'))
        elif " - ORSEN:" in X:
            temp_time = X.split(" - ORSEN:", 1)[0]
            user_orsen_lat.append(time.strptime(temp_time, '%m-%d-%y %H:%M:%S'))


    user_lat = []
    for i in range (len(user_orsen_lat)):
        if i < len(user_orsen_lat)-1:
            user_lat.append(time.mktime(user_orsen_lat[i+1]) - time.mktime(user_orsen_lat[i]))

    print_list(user_lat)

def test_dataset():
    dbo_emotion = DBOEmotion('nrc_emotion')
    dbo_emotion.get_all_terms()

def get_data_csv():
    file_path = "/Users/kylesantos/Desktop/Thesis/ScratchCompiled-User-Input.csv"

    sheets = []


    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        curr_participant_num = 1
        curr_participant = []
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            line_count += 1

            if row["Turn"] != "" and row["Turn"] != "Turn":
                if row["Participant #"] == str(curr_participant_num):
                    curr_participant.append(row)
                else:
                    print("CHECKING: ", curr_participant)
                    sheets.append(curr_participant)
                    curr_participant = []
                    curr_participant_num += 1

        sheets.append(curr_participant)

        print(f'Processed {line_count} lines.')

    print("PRINTING SHEETS LEN: ", len(sheets))

    return sheets


def extract_time(participant_list):
    dialogue_moves = ["Emphasis", "Praise", "Corrective", "General", "Emotion", "Cause", "Discipline", "Evaluating", "Labelling", "Recollecting", "Specific", "Followup"]
    num_iterations = 3
    iteration_1 = [1, 2, 3, 4, 5]
    iteration_2 = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    iteration_3 = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]


    # user_latency_time = [[0] * len(dialogue_moves)] * num_iterations
    # eren_latency_time = [[0] * len(dialogue_moves)] * num_iterations
    # user_dialogue_count = [[0] * len(dialogue_moves)] * num_iterations
    # eren_dialogue_count = [[0] * len(dialogue_moves)] * num_iterations

    user_latency_time = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    eren_latency_time = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    user_dialogue_count = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    eren_dialogue_count = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    all_user_latency_time = []
    all_eren_latency_time = []
    all_user_dialogue_count = []
    all_eren_dialogue_count = []

    for participant in participant_list:
        curr_user_latency_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        curr_eren_latency_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        curr_user_dialogue_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        curr_eren_dialogue_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for response in participant:
            curr_iteration = -1

            if int(response["Participant #"]) in iteration_1:
                curr_iteration = 0
            elif int(response["Participant #"]) in iteration_2:
                curr_iteration = 1
            elif int(response["Participant #"]) in iteration_3:
                curr_iteration = 2

            print("curr Iter: ", curr_iteration, "   :   user: ", response["Participant #"])
            if response["User Dialogue Move"] != "":
                try:
                    (user_latency_time[curr_iteration])[dialogue_moves.index(response["User Dialogue Move"])] += float(response["Latency"])
                    (user_dialogue_count[curr_iteration])[dialogue_moves.index(response["User Dialogue Move"])] += 1

                    curr_user_latency_time[dialogue_moves.index(response["User Dialogue Move"])] += float(
                        response["Latency"])
                    curr_user_dialogue_count[dialogue_moves.index(response["User Dialogue Move"])] += 1
                except:
                    print("heh")
            elif response["Dialogue Move Used 1"] != "":
                try:
                    (eren_latency_time[curr_iteration])[dialogue_moves.index(response["Dialogue Move Used 1"])] += float(response["Latency"])
                    (eren_dialogue_count[curr_iteration])[dialogue_moves.index(response["Dialogue Move Used 1"])] += 1

                    curr_eren_latency_time[dialogue_moves.index(response["User Dialogue Move"])] += float(
                        response["Latency"])
                    curr_eren_dialogue_count[dialogue_moves.index(response["User Dialogue Move"])] += 1
                except:
                    print("heh")
            elif response["Dialogue Move Used 2"] != "":
                try:
                    (eren_latency_time[curr_iteration])[dialogue_moves.index(response["Dialogue Move Used 2"])] += float(response["Latency"])
                    (eren_dialogue_count[curr_iteration])[dialogue_moves.index(response["Dialogue Move Used 1"])] += 1

                    curr_eren_latency_time[dialogue_moves.index(response["User Dialogue Move"])] += float(
                        response["Latency"])
                    curr_eren_dialogue_count[dialogue_moves.index(response["User Dialogue Move"])] += 1
                except:
                    print("heh")
        all_user_latency_time.append(curr_user_latency_time)
        all_eren_latency_time.append(curr_eren_latency_time)
        all_user_dialogue_count.append(curr_user_dialogue_count)
        all_eren_dialogue_count.append(curr_eren_dialogue_count)

    # print("===DIALOGUE MOVES===")
    # print_list(dialogue_moves)
    #
    #
    # print("===USER LATENCEY===")
    # # print_list(user_latency_time)
    #
    # for i in range (len(user_latency_time)):
    #     print("*****Iteration ", i)
    #     print_list(user_latency_time[i])
    #
    # print("===EREN LATENCEY===")
    # # print_list(eren_latency_time)
    #
    # for i in range (len(eren_latency_time)):
    #     print("*****Iteration ", i)
    #     print_list(eren_latency_time[i])
    #
    # print("===USER COUNT===")
    # # print_list(user_dialogue_count)
    #
    # for i in range (len(user_dialogue_count)):
    #     print("*****Iteration ", i)
    #     print_list(user_dialogue_count[i])
    #
    # print("===EREN COUNT===")
    # # print_list(eren_dialogue_count)
    #
    # for i in range (len(eren_dialogue_count)):
    #     print("*****Iteration ", i)
    #     print_list(eren_dialogue_count[i])

    import numpy
    all_user_latency_time_numpy = numpy.asarray(all_user_latency_time)
    numpy.savetxt("all_user_latency_time.csv", all_user_latency_time_numpy, delimiter=",")

    all_eren_latency_time_numpy = numpy.asarray(all_eren_latency_time)
    numpy.savetxt("all_eren_latency_time.csv", all_eren_latency_time_numpy, delimiter=",")

    all_user_dialogue_count_numpy = numpy.asarray(all_user_dialogue_count)
    numpy.savetxt("all_user_dialogue_count.csv", all_user_dialogue_count_numpy, delimiter=",")

    all_eren_dialogue_count_numpy = numpy.asarray(all_eren_dialogue_count)
    numpy.savetxt("all_eren_dialogue_count.csv", all_eren_dialogue_count_numpy, delimiter=",")






# main_file_path = '/Users/kylesantos/Desktop/Thesis/raw data/oct 31 testing/'
#
# file_paths = ['3L celine/',
#               '3M kiara/',
#               '3N embry/',
#               '3N embry 2/',
#               '3O trisha/',
#               '3P christian/'
#
#               ]
#
# for X in file_paths:
#     print(" === " + X + " === ")
#     user_resp, orsen_resp, user_orsen_resp, user_lat, orsen_lat, orsen_dmoves= extract_convo(main_file_path + X)
#     # get_time(main_file_path + X)


sheet_data = get_data_csv()
extract_time(sheet_data)


# occ_manager = OCCManager()
# orsen = ORSEN()
# test_eden()