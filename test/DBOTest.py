from src.db import SQLConnector
from src.dbo import DBOConcept, DBOConceptGlobalImpl, DBOConceptLocalImpl
from src.objects.concept import Concept, GlobalConcept, LocalConcept

connection = SQLConnector.get_instance().get_connection()

concept_manager = DBOConceptGlobalImpl()
local_concept_manager = DBOConceptLocalImpl()

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

is_updated = local_concept_manager.update_score(1, 0.5)

