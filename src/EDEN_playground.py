from EDEN.OCC import OCCManager
from EDEN.constants import *
from src.ORSEN import ORSEN
from src import Logger
import pickle
import datetime


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

def test_read_pickle(date, dogs_dict):
    with open('../logs/user world/' + date, 'rb') as f:
        new_dict = pickle.load(f)
        f.close()

    # infile = open(filename, 'rb')
    # new_dict = pickle.load(infile)
    # infile.close()

    print(new_dict)
    print(new_dict == dogs_dict)
    print(type(new_dict))

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

test_occ_model()