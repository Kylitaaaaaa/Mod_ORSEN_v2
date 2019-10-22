"""
EVENT TYPES
"""
EVENT_EMOTION = "EMOTION_EVENT"

"""
VADER VALUES
"""
VADER_POSITIVE = "POSITIVE"
VADER_NEGATIVE = "NEGATIVE"
VADER_NEUTRAL = "NEUTRAL"

"""
LANGUAGE STUFF
"""
EXC_ADVERB_LIST = ["hardly", "rarely"]

"""
OCC VALUES 
    Can be Agent-based, Object-based, Event-based, Intensity
"""

"""Agent-Based"""
# Agent Fondness (AF)
AF_LIKED = "LIKED"
AF_NOT_LIKED = "NOT LIKED"

# Direction of Emotion (DE)
DE_SELF ="SELF"
DE_OTHERS ="OTHER"

"""Object-Based"""
# Object Fondness (OF)
OF_LIKED = "LIKED"
OF_NOT_LIKED = "NOT LIKED"

# Object Appealing(OA)
OA_ATTRACTIVE = "ATTRACTIVE"
OA_NOT_ATTRACTIVE = "NOT ATTRACTIVE"
OA_NEUTRAL = "NEUTRAL"

"""Event-Based"""
# Self Reaction (SR)
SR_PLEASED = "PLEASED"
SR_DISPLEASED = "DISPLEASED"

# Self Presumption (SP)
SP_DESIRABLE = "DESIRABLE"
SP_UNDESIRABLE = "UNDESIRABLE"
POS_AFFECTIVE_VERBS_LIST =["like"]
NEG_AFFECTIVE_VERBS_LIST =["hate"]

# Other Presumption (OP)
OP_DESIRABLE = "DESIRABLE"
OP_UNDESIRABLE = "UNDESIRABLE"

# Prospect (PROS)
PROS_POSITIVE = "POSITIVE"
PROS_NEGATIVE = "NEGATIVE"
PROS_NEUTRAL = "NEUTRAL"

# Status (STAT)
STAT_CONFIRMED = "CONFIRMED"
STAT_UNCONFIRMED = "UNCONFIRMED"
STAT_DISCONFIRMED = "DISCONFIRMED"

# Unexpectedness (UNEXP)EDEV
UNEXP_TRUE = True
UNEXP_FALSE = False
UNEXP_LIST = ["abruptly", "unexpectedly", "immediately", "instantaneously", "promptly", "swiftly", "instantly", "short", "unaware", "unawares", "without warning", "unanticipatedly", "at once", "straight away", "forthwith", "sudden", "straight off", "asudden", "all at once", "quickly", "without notice", "in a flash", "in a trice", "in an instant", "in two shakes", "all of a sudden", "like a shot", "out of the blue", "on spur of moment", "before you can say knife", "before you can say Jack Robinson", "on the spur of the moment"]

# Self Appraisal (SA)
SA_PRAISE = "PRAISEWORTHY"
SA_BLAME = "BLAMEWORTHY"
SA_NEUTRAL = "NEUTRAL"

# Valenced Reaction (VR)
VR_TRUE = True
VR_FALSE = False

"""Intensity"""
# Event Deservingness (ED)
ED_HIGH = "HIGH"
ED_LOW = "LOW"
# ED_NEUTRAL = "NEUTRAL"

# Effort of Action (EOA)
EOA_OBVIOUS = "OBVIOUS"
EOA_NOT_OBVIOUS = "NOT OBVIOUS"

# Expected Deviation (EDEV)
EDEV_HIGH = "HIGH"
EDEV_LOW = "LOW"
# ED_NEUTRAL = "NEUTRAL"

# Event Familiarity (EF)
EF_COMMON = "COMMON"
EF_UNCOMMON = "UNCOMMON"


"""OCC EMOTIONS"""
OCC_DISTRESS = "DISTRESS"
OCC_SORRY_FOR = "SORRY FOR"
OCC_RESENTMENT = "RESENTMENT"
# OCC_GLOATING = "GLOATING"
OCC_HOPE = "HOPE"
OCC_FEAR = "FEAR"
OCC_SATISFACTION = "SATISFACTION"
OCC_FEARS_CONFIRMED = "FEARS CONFIRMED"
OCC_RELIEF = "RELIEF"
OCC_DISAPPOINTMENT = "DISAPPOINTMENT"
OCC_PRIDE = "PRIDE"
OCC_SHAME = "SHAME"
OCC_ADMIRATION = "ADMIRATION"
# OCC_REPROACH = "REPROACH"
# OCC_REPROACH = "DISGRACE"
OCC_LOVE = "LOVE"
OCC_HATE = "HATE"
OCC_GRATIFICATION = "GRATIFICATION"
OCC_REMORSE = "REMORSE"
# OCC_REMORSE = "GUILT"
OCC_GRATITUDE = "GRATITUDE"
OCC_ANGER = "ANGER"
OCC_SHOCK = "SHOCK"
OCC_SURPRISE = "SURPRISE"
OCC_JOY = "JOY"

"""SIMPLIFIED EMOTIONS"""
OCC_SIMPLIFY_ANGER = [OCC_SHAME, OCC_REMORSE, OCC_ANGER]
OCC_SIMPLIFY_FEAR_CONFIRMED = [OCC_FEARS_CONFIRMED, OCC_FEAR]
OCC_SIMPLIFY_GRATITUDE = [OCC_PRIDE, OCC_ADMIRATION, OCC_GRATIFICATION, OCC_GRATITUDE]
OCC_SIMPLIFY_SATISFACTION = [OCC_HOPE, OCC_SATISFACTION]

#change to disciplinary emotions
DISCIPLINARY_EMOTIONS = [OCC_HATE,
                         OCC_DISTRESS]

# NEGATIVE_EMOTIONS = [OCC_DISTRESS,
#                      OCC_SORRY_FOR,
#                      OCC_RESENTMENT,
#                      OCC_FEAR,
#                      OCC_FEARS_CONFIRMED,
#                      OCC_DISAPPOINTMENT,
#                      OCC_SHAME,
#                      OCC_HATE,
#                      OCC_REMORSE,
#                      OCC_ANGER,
#                      OCC_SHOCK]

NEGATIVE_EMOTIONS = [OCC_SORRY_FOR,
                     OCC_RESENTMENT,
                     OCC_FEAR,
                     OCC_FEARS_CONFIRMED,
                     OCC_DISAPPOINTMENT,
                     OCC_SHAME,
                     OCC_HATE,
                     OCC_REMORSE,
                     OCC_ANGER,
                     OCC_SHOCK]

POSITIVE_EMOTIONS = [OCC_HOPE,
                     OCC_SATISFACTION,
                     OCC_RELIEF,
                     OCC_PRIDE,
                     OCC_ADMIRATION,
                     OCC_LOVE,
                     OCC_GRATIFICATION,
                     OCC_GRATITUDE,
                     OCC_SURPRISE,
                     OCC_JOY]

EMOTION_TYPE_POSITIVE = "POSITIVE"
EMOTION_TYPE_NEGATIVE = "NEGATIVE"

