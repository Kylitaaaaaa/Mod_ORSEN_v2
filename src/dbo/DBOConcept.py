from pypika import Query, Table, Field

from src.db import SQLConnector
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

        conn = SQLConnector.get_instance().get_connection()
        cursor = conn.cursor()

        resulting = []
        try:
            cursor.execute(query)
            result = cursor.fetchall()

            for row in result:

                resulting.append(self.concept_type(*row))

        except Exception as e:

            print(e, file=sys.stderr)

        conn.close()
        return resulting