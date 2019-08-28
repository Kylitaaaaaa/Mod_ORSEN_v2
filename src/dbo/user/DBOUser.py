from src.db import SQLExecuter
from src.constants import  *

from pypika import Query, Table, Criterion, Field
import abc
from abc import ABC, abstractmethod

class DBOKidUser(ABC):
    __metaclass__ = abc.ABCMeta

    def __init__(self, table_reference, user_type):
        super().__init__()
        self.table_reference = table_reference
        self.user_type = user_type

    def get_user_by_id(self, id):
        pass