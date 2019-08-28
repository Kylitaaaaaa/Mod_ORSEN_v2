from . import DBOConcept
from src.constants import *
from src.db import SQLExecuter
from src.models.concept import GlobalConcept

from pypika import Query, Table, Criterion, Field

"""
    Global implementation of DBO Concept which uses the GlobalConcept object type.
    As of now, I don't think there is anything unique to Global types, making this implementation a bit too empty.
"""
class DBOConceptGlobalImpl(DBOConcept):
    def __init__(self):
        DBOConcept.__init__(self, "concepts", GlobalConcept)

    def add_concept(self, concept):
        q = Query\
            .into(self.table_reference)\
            .columns(
                self.table_reference.first,
                self.table_reference.relation,
                self.table_reference.second)\
            .insert(
                concept.first,
                concept.relation,
                concept.second )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        sql_response = SQLExecuter.execute_write_query(query)

        return sql_response