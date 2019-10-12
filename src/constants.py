""" FOR LOGS """
CONVERSATION_LOG = "conversation"
INFORMATION_EXTRACTION_LOG = "information_extraction"
DIALOGUE_MODEL_LOG = "dialogue_model"
EVENT_CHAIN_LOG = "event chain"

""" PACKAGE VERSIONING CONTROL """
SPACY_VERSION = '2.1.0'
NEURALCOREF_VERSION = '4.0.0'
LAST_CHECK_DATE = "July 26, 2019"

""" DATABASE CREDENTIALS """
LOCATION = "localhost"
USERNAME = "root"
PASSWORD = "1234"
SCHEMA = "orsen_kb"

""" SQL COMMANDS """
FETCH_ONE = 1
FETCH_ALL = 2

""" GENERIC RESPONSES """
IS_AFFIRM = ['yes', 'yes.', 'yeah', 'yeah.', 'sure', 'sure.', 'yup', 'yup.']
IS_DENY = ['no', 'no.', 'nope', 'nope.']
IS_END = ['bye', 'bye.', 'the end', 'the end.']

""" CONSTANT VALUES CONTROL """

# EVENT TYPES #
EVENT_ACTION = "ACTION_EVENT"
EVENT_CREATION = "CREATION_EVENT"
EVENT_DESCRIPTION = "DESCRIPTION_EVENT"

SETTING_PLACE = 'PLACE'
SETTING_DATE = 'DATE'
SETTING_TIME = 'TIME'

""" ARRAY INDICES """

# ACTION EVENT #
ACTOR = 0
ACTION = 1
DIRECT_OBJECT = 2
ADVERB = 3
PREPOSITION = 4
OBJ_PREPOSITION = 5
# NEGATED = 3 # NOT USED

# CREATION EVENT #
SUBJECT = 0

# DESCRIPTION EVENT #
FIRST_TOKEN = 0
RELATION = 1
KEYWORD = 2
SECOND_TOKEN = 3
THIRD_TOKEN = 4
DESCRIPTION_NEGATED = 5

""" DIALOGUE MOVES """
#BASIC ORSEN
DIALOGUE_TYPE_FEEDBACK = "feedback"
DIALOGUE_TYPE_HINTING = "hinting"
DIALOGUE_TYPE_PROMPT = "prompt"
DIALOGUE_TYPE_PUMPING_GENERAL = "general"
DIALOGUE_TYPE_PUMPING_SPECIFIC = "specific"
THE_END = "end"

#JUVEYANCE
DIALOGUE_TYPE_FOLLOW_UP_CONFIRM = "FOLLOW_UP_CONFIRM"
DIALOGUE_TYPE_FOLLOW_UP_ASK = "FOLLOW_UP_ASK"
DIALOGUE_TYPE_FOLLOW_UP_UNKNOWN = "FOLLOW_UP_???"
DIALOGUE_TYPE_SUGGESTING = "SUGGESTING"

DIALOGUE_TYPE_INPUT_MISHEARD = "INPUT_MISHEARD"
DIALOGUE_TYPE_UNKNOWN = "UNKNOWN"

""" CONSTANTS BASED ON ENGLISH CONCEPTS """

VOICE_PASSIVE = "PASSIVE"
VOICE_ACTIVE = "ACTIVE"

# 23 TOTAL HELPING VERBS
HELPING_VERBS = ["am", "are", "is", "was", "were", "be", "being", "been", "have", "has", "had", "shall", "will", "do", "does", "did", "may", "must", "might", "can", "could", "would", "should"]
RELATIVE_PRONOUNS = ["who", " whom", " whose", " which", " that", " whoever", " what", " whomever", " whatever", " whichever"]


""" RELATIONS """

IS_A = "IsA"
PART_OF = "PartOf"
AT_LOCATION = "AtLocation"
HAS_PREREQ = "HasPrerequisite"
CREATED_BY = "CreatedBy"
USED_FOR = "UsedFor"
CAUSES = "Causes"
DESIRES = "Desires"
CAPABLE_OF = "CapableOf"
HAS_PROPERTY = "HasProperty"
HAS_A = "HasA"
RECEIVES_ACTION = "ReceivesAction"

LOCATED_NEAR = "LocatedNear"

RELATIONS = [IS_A, PART_OF, AT_LOCATION, HAS_PREREQ, CREATED_BY, USED_FOR, CAUSES, DESIRES, CAPABLE_OF, HAS_PROPERTY,
             HAS_A, RECEIVES_ACTION]

""" QUOTES """

OPENING_QUOTES_STANDARD = "\""
CLOSING_QUOTES_STANDARD = "\""

OPENING_QUOTES_SPACY = "“"
CLOSING_QUOTES_SPACY = "”"

OPENING_QUOTES_STANFORD = "``"
CLOSING_QUOTES_STANFORD = "''"

OPENING_QUOTES = OPENING_QUOTES_STANDARD
CLOSING_QUOTES = CLOSING_QUOTES_STANDARD

""" DIALOGUE TRIGGERS """

PROMPT_TRIGGER = ["help me start.",
                  "help me start"]
PUMPING_TRIGGER = ["give me an idea.", "what should i talk about?", "help me.", "i'm stuck.",
                   "give me an idea", "what should i talk about", "help me", "i'm stuck",
                   "orsen + suggest"]
HINTING_TRIGGER = ["what's next?", "give me a hint.",
                   "what's next", "give me a hint",
                   "orsen + hint"]

""" KNOWLEDGE ACQUISITION RELATED """
MIGRATION_SCORE_THRESHOLD = 5