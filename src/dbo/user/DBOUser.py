from src.db import SQLExecuter
from src.constants import  *

from pypika import Query, Table, Criterion, Field
import abc
from abc import ABC, abstractmethod

class DBOUser(ABC):
    __metaclass__ = abc.ABCMeta

    def __init__(self, table_reference, user_type):
        super().__init__()
        self.table_reference = Table(table_reference)
        self.user_type = user_type

    def get_specific_user(self, name, code):
        q = Query\
            .from_(self.table_reference)\
            .select("*")\
            .where(
                (self.table_reference.name == name) & (self.table_reference.code == code)
            )

        query = q.get_sql()
        query = query.replace("\"","")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ONE)
        if result is None: return None

        user = self.user_type(*result)

        return user

    def get_user_by_name(self, name):
        q = Query\
            .from_(self.table_reference)\
            .select("*")\
            .where(
                (self.table_reference.name == name)
            )

        query = q.get_sql()
        query = query.replace("\"","")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ONE)
        if result is None: return None

        users = []
        for r in result:
            users.append(self.user_type(*r))

        return users

    def get_user_by_id(self, id):
        q = Query \
            .from_(self.table_reference) \
            .select("*") \
            .where(
            self.table_reference.iduser == id
        )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        result = SQLExecuter.execute_read_query(query, FETCH_ONE)
        if result is None: return None

        user = self.user_type(*result)

        return user

    def add_user(self, user):
        q = Query\
            .into(self.table_reference)\
            .columns(
                self.table_reference.name,
                self.table_reference.code)\
            .insert(
                user.name,
                user.code )

        query = q.get_sql()
        query = query.replace("\"", "")
        print(query)

        sql_response = SQLExecuter.execute_write_query(query)

        if sql_response is not None:
            user.id = sql_response

        return user