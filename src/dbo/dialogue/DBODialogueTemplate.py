from src.db import SQLExecuter
from src.constants import *
from src.dialogue import DialogueTemplate

from pypika import Query, Table, Criterion, Field
import abc
from abc import ABC, abstractmethod
import sys

class DBODialogueTemplate(ABC):
    __metaclass__ = abc.ABCMeta

    def __init__(self, table_reference, dialogue_template_type):
        super().__init__()
        self.table_reference = Table(table_reference)
        self.dialogue_template_type = dialogue_template_type

    def get_specific_template(self, id):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            self.table_reference.idtemplates == id
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ONE)
        if result is None: return None

        dialogue_template = DialogueTemplate.build(*result)

        return dialogue_template
