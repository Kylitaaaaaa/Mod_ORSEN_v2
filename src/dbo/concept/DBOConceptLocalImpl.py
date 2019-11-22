from . import DBOConcept
from src.constants import *
from src.db import SQLExecuter
from src.models.concept import LocalConcept, GlobalConcept

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

    def update_score(self, first, relation, second, score):
        q = Query\
            .update(self.table_reference)\
            .set(self.table_reference.score, score)\
            .where(
            (self.table_reference.first == first) & (self.table_reference.relation == relation) & (
                    self.table_reference.second == second)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        sql_response = SQLExecuter.execute_write_query(query)

        return sql_response

    def update_valid(self, first, relation, second, valid):
        q = Query\
            .update(self.table_reference)\
            .set(self.table_reference.valid, valid)\
            .where(
            (self.table_reference.first == first) & (self.table_reference.relation == relation) & (
                    self.table_reference.second == second)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        sql_response = SQLExecuter.execute_write_query(query)

        return sql_response

    def delete_concept(self, first, relation, second):
        q = Query\
            .from_(self.table_reference)\
            .delete()\
            .where(
            (self.table_reference.first == first) & (self.table_reference.relation == relation) & (
                    self.table_reference.second == second)
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        sql_response = SQLExecuter.execute_write_query(query)

        return sql_response

    def migrate_local_to_global(self, id):
        local_concept = self.get_concept_by_id(id)

        global_concept_manager = DBOConceptLocalImpl()
        global_concept = GlobalConcept.convert_local_to_global(local_concept)

        global_concept_manager.add_concept(global_concept)

