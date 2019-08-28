from src.dbo import DBOConcept
from src.constants import *
from src.db import SQLExecuter
from src.objects.concept import LocalConcept

from pypika import Query, Table, Criterion, Field

"""
    Local implementation of DBO Concept which uses the LocalConcept object type.
    Parsing is HEAVILY BASED on the order of the objects in the database. For the code to 
        function properly, the items must be arranged in the order based on constructor:
        
        id - the concept id
        first - the first word in the concept
        relation - the connection between "first" and "second"
        second - the second word 
        userid - the id of the user who first(?) suggested the relation in the concept
        scoore - score of the current concept
        valid - validity of the current concept
"""
class DBOConceptLocalImpl(DBOConcept):
    def __init__(self):
        DBOConcept.__init__(self, "local_concepts", LocalConcept)

    def add_concept(self, concept):
        q = Query\
            .into(self.table_reference)\
            .columns(
                self.table_reference.relation,
                self.table_reference.first,
                self.table_reference.second,
                self.table_reference.userid,
                self.table_reference.score,
                self.table_reference.valid)\
            .insert(
                concept.relation,
                concept.first,
                concept.second,
                concept.user_id,
                concept.score,
                concept.valid)

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        sql_response = SQLExecuter.execute_write_query(query)

        return sql_response

    def update_score(self, id, score):
        q = Query\
            .update(self.table_reference)\
            .set(self.table_reference.score, score)\
            .where(self.table_reference.id == id)

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        sql_response = SQLExecuter.execute_write_query(query)

        return sql_response

    def update_valid(self, id, valid):
        q = Query\
            .update(self.table_reference)\
            .set(self.table_reference.valid, valid)\
            .where(self.table_reference.id == id)

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        sql_response = SQLExecuter.execute_write_query(query)

        return sql_response

