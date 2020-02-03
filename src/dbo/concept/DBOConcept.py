from src.db import SQLExecuter
from src.constants import *

from pypika import Query, Table, Criterion, Field
import abc
from abc import ABC, abstractmethod
import sys

"""
    Hi. Kung sino man makakabasa nito xD
    
    State of the code: 
        Parsing is HEAVILY BASED on the order of the objects in the database. For the code to 
        function properly, the items must be arranged in the order based on constructor:
        
        id - the concept id
        first - the first word in the concept
        relation - the connection between "first" and "second"
        second - the second word 
        etc* - other elements defined in their specific implementations
"""


class DBOConcept(ABC):
    __metaclass__ = abc.ABCMeta

    """
        table_reference - table where the concepts are taken
        concept_type - type of concept (e.g. global, local) that will be used. Takes the class type to be used for 
        initialization of concept objects in latter parts of the code
    """

    def __init__(self, table_reference, concept_type):
        super().__init__()
        self.table_reference = Table(table_reference)
        self.concept_type = concept_type

    """
        General code for getting all fields of all concepts in the database. Converts database rows into objects
        by using the object type defined in concept_type
        
        Input:  N/A
        Output: LIST of concept object based on concept_type
    """

    def get_all_concepts(self):
        q = Query \
            .from_(self.table_reference).select("*")

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts

    """
        General code to get a concept based on the word-relation-word pairing in a given concept. 

        Input:  first word, relation, second word
        Output: Concept object based on concept type
    """

    def get_specific_concept(self, first, relation, second):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            (self.table_reference.first == first) & (self.table_reference.relation == relation) & (
                    self.table_reference.second == second)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ONE)
        print("RESULT IS THIS:", result)
        if result is None or not result: return None

        concept = self.concept_type(*result)

        return concept

    """
        General code to get a concept using its concept id "id". Converts database rows into objects by using 
        the object type defined in concept_type
                        
        Input:  concept_id
        Output: Concept object based on concept_type
    """

    def get_concept_by_id(self, id):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            self.table_reference.id == id
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ONE)
        if result is None: return None

        concept = self.concept_type(*result)

        return concept

    """
        General code to get a concept based on a given word (regardless of its relation or the word it's connected to)
                
        Input:  word
        Output: LIST of concept object based on concept_type
    """

    def get_concept_by_word(self, word):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            (self.table_reference.first == word) | (self.table_reference.second == word)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts

    """
        General code to get a concept based on a given relation (e.g. isA, capableOf)
        
        Input:  relation
        Output: LIST of concept object based on concept type
    """

    def get_concept_by_relation(self, word, relation):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            ((self.table_reference.first == word) | (self.table_reference.second == word)) & (
                        self.table_reference.relation == relation)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts
    
    """
            General code to get a concept based on a first word and relation (e.g. isA, capableOf)

            Input:  first, relation
            Output: LIST of concept object based on concept type
    """

    def get_concept_by_first_relation(self, first, relation):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            ((self.table_reference.first == first)) & (
                    self.table_reference.relation == relation)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts

    """
            General code to get a concept based on a second word and relation (e.g. isA, capableOf)

            Input:  second, relation
            Output: LIST of concept object based on concept type
        """

    def get_concept_by_second_relation(self, second, relation):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            ((self.table_reference.second == second)) & (
                    self.table_reference.relation == relation)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts

    """
        Similar to get_specific_concept, except it searches for relations with specified words as substrings instead 
        of only getting exact matches.
        
        Input: relation, *first-word used to check similarity, *second-word used to check similarity
                * - optional values
        Output: LIST of concept object based on concept type
    """

    def get_similar_concept(self, relation, first="", second=""):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            (self.table_reference.first.like('%' + first + '%')) &
            (self.table_reference.second.like('%' + second + '%')) &
            (self.table_reference.relation == relation)
        )
        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        concepts = []
        for r in result:
            concepts.append(self.concept_type(*r))
        return concepts

    """
            General code to get a concept based on the word-word pairing in a given concept. 

            Input:  first word, second word
            Output: Concept object based on concept type
        """

    def get_related_concepts(self, first, second):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            (self.table_reference.first == first) & (
                    self.table_reference.second == second)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ONE)
        print("RESULT IS THIS:", result)
        if result is None or not result: return None

        concept = self.concept_type(*result)

        return concept


    @abstractmethod
    def add_concept(self, concept):
        pass

    def get_random_concept(self):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .orderby('rand()') \
            .limit(1)

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ONE)
        if result is None: return None

        concept = self.concept_type(*result)

        return concept
