from src.db import SQLExecuter

from pypika import Query, Table, Criterion, Field
import abc
from abc import ABC, abstractmethod

class DBOUser(ABC):
    def __init__(self, table_reference):
        self.table_reference = Table(table_reference)

    def get_user_by_id(self, id):
        pass