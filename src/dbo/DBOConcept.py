from src.db import SQLConnector, SQLExecuter
from src.constants import  *

from pypika import Query, Table, Criterion, Field
import abc
from abc import ABC, abstractmethod
import sys

class DBOConcept(ABC):
    __metaclass__ = abc.ABCMeta

    """
        table_reference - table where the concepts are taken
        concept_type - type of concept (e.g. global, local) that will be used. Takes the class type to be used for 
        initialization of concept objects in latter parts of the code
    """
    def __init__(self, table_reference, concept_type):
        super().__init__()
        self.table_reference = Table('concepts')
        self.concept_type = concept_type

    """
        General code for getting all fields of all concepts in the database. Converts database rows into objects
        by using the object type defined in concept_type
    """
    def get_all_concepts(self):
        q = Query.from_(self.table_reference).select("*")

        query = q.get_sql()
        query = query.replace("\"","")

        result = SQLExecuter.execute_query(query, FETCH_ALL)

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts

    def get_concept_by_id(self, id):
        q = Query.from_(self.table_reference)\
            .select("*")\
            .where(
                self.table_reference.idconcepts == id
            )

        query = q.get_sql()
        query = query.replace("\"","")

        result = SQLExecuter.execute_query(query, FETCH_ONE)
        concept = self.concept_type(*result)

        return concept


    def get_concept_by_word(self, word):
        q = Query.from_(self.table_reference)\
            .select("*")\
            .where(
                (self.table_reference.first == word) | (self.table_reference.second == word)
            )

        query = q.get_sql()
        query = query.replace("\"","")
        print(query)

        result = SQLExecuter.execute_query(query, FETCH_ALL)

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts

    def get_concept_by_relation(self, word, relation):
        q = Query.from_(self.table_reference)\
            .select("*")\
            .where(
                ((self.table_reference.first == word) | (self.table_reference.second == word)) & (self.table_reference.relation == relation)
            )

        query = q.get_sql()
        query = query.replace("\"","")
        print(query)

        result = SQLExecuter.execute_query(query, FETCH_ALL)

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts
