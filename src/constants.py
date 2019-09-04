""" FOR LOGS """
CONVERSATION_LOG = "conversation"
INFORMATION_EXTRACTION_LOG = "information_extraction"
DIALOGUE_MODEL_LOG = "dialogue_model"

""" PACKAGE VERSIONING CONTROL """
SPACY_VERSION = '2.1.0'
NEURALCOREF_VERSION = '4.0.0'
LAST_CHECK_DATE = "July 26, 2019"

""" DATABASE CREDENTIALS """
LOCATION = "localhost"
USERNAME = "root"
PASSWORD = "password"
SCHEMA = "orsen_kb"

""" SQL COMMANDS """
FETCH_ONE = 1
FETCH_ALL = 2

####################################################
# RELATIONS ########################################
####################################################
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
