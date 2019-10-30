from EDEN.OCC import OCCManager
from EDEN.constants import *
from EDEN.models import EmotionActionEvent
from src.ORSEN import ORSEN, EVENT_CREATION, CreationEvent, EVENT_DESCRIPTION, EVENT_ACTION, ActionEvent
from src import Logger
import pickle
import datetime

from src.models import World
from src.models.elements import Object, Attribute, Setting, Character
import time

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
    orsen = ORSEN()

    for X in response:
        orsen.perform_text_understanding(X)
        emotion = orsen.get_emotion(X)



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
    occ_manager = OCCManager()

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


def print_emotion(expected_emotion, chosen_emotion):
    if chosen_emotion is not None:
        print("EXPECTING: ", expected_emotion, " : ", chosen_emotion.emotion)
    else:
        print("EXPECTING: ", expected_emotion, " : ", chosen_emotion)
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

    user_lat = []
    orsen_lat = []
    user_orsen_lat = []

    f = open(file_path, "r")
    for X in f:
        if "???: " in X:
            user_resp.append(X.split("???: ", 1)[1].replace('\n', ''))
            user_orsen_resp.append(X.split("???: ", 1)[1].replace('\n', ''))
        elif "ORSEN: " in X:
            orsen_resp.append(X.split("ORSEN: ", 1)[1].replace('\n', ''))
            user_orsen_resp.append(X.split("ORSEN: ", 1)[1].replace('\n', ''))
        elif "USER LATENCY TIME (seconds): " in X:
            user_lat.append(float(X.split("USER LATENCY TIME (seconds): ", 1)[1].replace('\n', '')))
            user_orsen_lat.append(float(X.split("USER LATENCY TIME (seconds): ", 1)[1].replace('\n', '')))
        elif "ORSEN LATENCY TIME (seconds): " in X:
            orsen_lat.append(float(X.split("ORSEN LATENCY TIME (seconds): ", 1)[1].replace('\n', '')))
            user_orsen_lat.append(float(X.split("ORSEN LATENCY TIME (seconds): ", 1)[1].replace('\n', '')))

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
    # print("===PRINTING USER ORSEN LATENCY===")
    # print_list(user_orsen_lat)

    return user_resp, orsen_resp, user_orsen_resp, user_lat, orsen_lat
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


main_file_path = '/Users/kylesantos/Desktop/oct 20 testing/'
# file_paths = ['1 zairah/',
#               '2 Renhart/',
#               '3 Maricar/',
#               '4 Jhanness/',
#               '5 Jim/',
#               '6 Shad/',
#               '7 Clarenz/',
#               '8 Harvy/',
#               '9 Lian/',
#               '10 Jhanissa 1/',
#               '10 Jhanissa 2/'
#               ]

file_paths = ['1 James/',
              '2 Abeng/',
              '3 Jim 1/',
              '3 Jim 2/',
              '4 Vincent/',
              '5 Harvy/'
              ]

for X in file_paths:
    print(" === " + X + " === ")
    # user_resp, orsen_resp, user_orsen_resp, user_lat, orsen_lat = extract_convo(main_file_path + X)
    get_time(main_file_path + X)





# print("\n\n=====Zairah=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/1 zairah/")
#
# print("\n\n=====Renhart=====")
# # extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/2 Renhart/")
# #
# print("\n\n=====Maricar=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/3 Maricar/")
# #
# print("\n\n=====Jhanness=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/4 Jhanness/")
#
# print("\n\n=====Jim=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/5 Jim/")
#
# print("\n\n=====Shad=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/6 Shad/")
#
#
# print("\n\n=====Clarenz=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/7 Clarenz/")
#
# print("\n\n=====Harvy=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/8 Harvy/")
#
# print("\n\n=====Lian=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/9 Lian/")
#
# print("\n\n=====Jhanissa 1=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/10 Jhanissa 1/")
#
# print("\n\n=====Jhanissa 2=====")
# extract_emo_class("/Users/kylesantos/Desktop/oct 26 testing/10 Jhanissa 2/")

