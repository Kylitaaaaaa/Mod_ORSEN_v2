from src.db import SQLExecuter
from src.constants import *

from pypika import Query, Table, Criterion, Field
from EDEN.models import NRC_Emotion

"""
    id - the term id
    term - word to evaluate
    Emotions can either be 1 or 0
    anger, anticip, trust, surprise, positive, negative, sadness, disgust, joy
    synonym - up to 3 synonyms
"""

class DBOEmotion:
    def __init__(self, table_reference):
        self.table_reference = Table(table_reference)
        self.table_name = table_reference


    def get_term(self, term):
        # q = Query \
        #     .from_(self.table_reference) \
        #     .select("*") \
        #     .where( (self.table_reference.term == term) | (self.table_reference.synonym_1 == term) | (self.table_reference.synonym_2 == term) | (self.table_reference.synonym_3 == term) )
        #
        # query = q.get_sql()
        # query = query.replace("\"", "")

        query = 'SELECT * FROM %s WHERE term = "%s" OR synonym_1 = "%s" OR synonym_2 = "%s" OR synonym_3 = "%s" LIMIT 20' % (self.table_name, term, term, term, term)
        print(query)

        results = SQLExecuter.execute_read_query(query, FETCH_ALL)



        if results is None:
            return None

        if len(results) ==0:
            return None
        #
        # curr_term = Emotion(term=term)

        curr_term = NRC_Emotion(term=term)

        print("Printing dbo results: ", type(results))
        print(results)
        for X in results:
            curr_term.add_values(X)
            print(X)
        print("DOne Printing dbo results")

        return curr_term


    def get_all_terms(self):
        # q = Query \
        #     .from_(self.table_reference) \
        #     .select("*") \
        #     .where( (self.table_reference.term == term) | (self.table_reference.synonym_1 == term) | (self.table_reference.synonym_2 == term) | (self.table_reference.synonym_3 == term) )
        #
        # query = q.get_sql()
        # query = query.replace("\"", "")

        query = 'SELECT * FROM %s' % self.table_name
        print(query)

        results = SQLExecuter.execute_read_query(query, FETCH_ALL)



        if results is None:
            return None

        if len(results) ==0:
            return None

        for X in results:
            self.get_term()
            print(X[1])

        #
        # curr_term = Emotion(term=term)

        # curr_term = NRC_Emotion(term=term)
        #
        # print("Printing dbo results: ", type(results))
        # print(results)
        # for X in results:
        #     curr_term.add_values(X)
        #     print(X)
        # print("DOne Printing dbo results")
        #
        # return curr_term
