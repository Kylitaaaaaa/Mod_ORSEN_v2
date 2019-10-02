# from src.dataprocessor import Annotator
# from src.textunderstanding import EizenExtractor
#
# annotator = Annotator()
# annotator.annotate("There was once a boy named James.")
# doc = annotator.get_annotated()
#
# eizen_extractor = EizenExtractor()
# print(doc.text)
# for sent in doc.sents:
#     eizen_extractor.display_tokens(sent)
# from src.dbo.concept import DBOConceptGlobalImpl
# from src.constants import *
# from src.dbo.relation import DBORelation
#
# concept_manager = DBOConceptGlobalImpl()
# attr = 'boy'
# concepts = concept_manager.get_similar_concept(first=attr, relation=IS_A, second='male')
# for concept in concepts:
#     print(concept)
from src.models.elements import Character

