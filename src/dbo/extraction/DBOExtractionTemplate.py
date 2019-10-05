from src.db import SQLExecuter
from src.constants import *
from src import DialogueTemplateBuilder

from pypika import Query, Table, Criterion, Field

from src.models.nlp import ExtractionTemplate


class DBOExtractionTemplate():

    def __init__(self, table_reference):
        super().__init__()
        self.table_reference = Table(table_reference)

    def get_all_extraction_templates(self):

        q = Query \
            .from_(self.table_reference).select("*")

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        extraction_templates = []
        for r in result:
            extraction_templates.append(ExtractionTemplate(*r))

        return extraction_templates

    def get_extraction_templates_by_keyword(self, keyword_lemma, keyword_dep, include_blanks=True):
        if include_blanks:
            q = Query \
                .from_(self.table_reference) \
                .select("*") \
                .where(
                    (self.table_reference.keywords == keyword_lemma) | (self.table_reference.keywords == keyword_dep) | (self.table_reference.keywords == "")
            )

        else:
            q = Query \
                .from_(self.table_reference) \
                .select("*") \
                .where(
                    (self.table_reference.keywords == keyword_lemma) | (self.table_reference.keywords == keyword_dep)
            )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ALL)
        if result is None: return None

        extraction_templates = []
        for r in result:
            extraction_templates.append(ExtractionTemplate(*r))

        return extraction_templates

