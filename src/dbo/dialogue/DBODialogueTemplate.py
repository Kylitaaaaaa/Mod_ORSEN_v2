from src.db import SQLExecuter
from src.constants import *
from src import DialogueTemplateBuilder

from pypika import Query, Table

class DBODialogueTemplate():

    def __init__(self, table_reference):
        self.table_reference = Table(table_reference)

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

        dialogue_template = DialogueTemplateBuilder.build(*result)

        return dialogue_template

    def get_templates_of_type(self, dialogue_type):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            self.table_reference.response_type == dialogue_type
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        dialogue_templates = []
        for r in result:
            print("result is: ", r)
            dialogue_templates.append(DialogueTemplateBuilder.build(*r))

        return dialogue_templates

