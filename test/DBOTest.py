from src.db import SQLConnector
from src.dbo.concept import DBOConcept, DBOConceptGlobalImpl, DBOConceptLocalImpl
from src.dbo.dialogue import DBODialogueTemplate
from src.dbo.user import DBOUser
from src.models.concept import Concept, GlobalConcept, LocalConcept
from src.models.user import User

connection = SQLConnector.get_instance().get_connection()

concept_manager = DBOConceptGlobalImpl()
local_concept_manager = DBOConceptLocalImpl()
user_manager = DBOUser("users", User)
dialogue_manager = DBODialogueTemplate("templates", DBODialogueTemplate)
# concept = concept_manager.get_concept_by_id(4000)
# concept = local_concept_manager.get_concept_by_id(1)
# print(concept)

# concepts = concept_manager.get_concept_by_word('xd')
# for concept in concepts:
#     print(concept)

# concepts = concept_manager.get_concept_by_relation('life', 'isA')
# for concept in concepts:
#     print(concept)

# concept = concept_manager.get_specific_concept('apple', 'isA', 'healthy treat')
# print(concept)

# concepts = concept_manager.get_similar_concept(first='apple', relation='IsA', second='apple')
# for concept in concepts:
#     print(concept)

# concept = GlobalConcept(-1, 'apple', 'isA', 'good treat')
# is_added = concept_manager.add_concept(concept)
# print("IS CONCEPT ADDED:",is_added)

# local_concept = LocalConcept(-1, 'apple', 'isA', 'good treat', 1, 0, 0)
# is_added = local_concept_manager.add_concept(local_concept)
# print("IS CONCEPT ADDED:",is_added)

# is_updated = local_concept_manager.update_score(1, 0.5)

# user = user_manager.get_user_by_id(1)
# print(user)

# user = user_manager.get_specific_user('celina', 'dog')
# print(user)
# for concept in concepts:
#     print(concept)

# user = User(-1, "wisner", "xd")
# is_added = user_manager.add_user(user)
# print("IS CONCEPT ADDED:",is_added)

template = dialogue_manager.get_specific_template(1)
print(template)