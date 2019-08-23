from src.constants import *
import pymysql
import sys

"""
    Singleton impelementation of DB connector
"""
class SQLConnector:

    __instance = None

    @staticmethod
    def get_instance():
        if SQLConnector.__instance == None:
            SQLConnector()
        return SQLConnector.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SQLConnector.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SQLConnector.__instance = self

    def get_connection(self):
        assert LOCATION != "", "MySQL location is not set. Set them via set_connection_details"
        assert USERNAME != "", "MySQL username is not set. Set them via set_connection_details"
        assert PASSWORD != "", "MySQL password is not set. Set them via set_connection_details"

        try:
            return pymysql.connect(LOCATION, USERNAME, PASSWORD, SCHEMA)
        except Exception as e:
            print(e, file=sys.stderr)

