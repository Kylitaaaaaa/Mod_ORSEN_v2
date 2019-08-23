from . import SQLConnector
from src.constants import FETCH_ONE,FETCH_ALL

import sys

class SQLExecuter:
    @staticmethod
    def execute_query(query, fetch_mode):
        result = []
        try:
            # Open connection to MySQL
            conn = SQLConnector.get_instance().get_connection()
            cursor = conn.cursor()

            # Execute above sql statement and fetch all resulting rows
            cursor.execute(query)
            if fetch_mode == FETCH_ONE:
                result = cursor.fetchone()
            elif fetch_mode == FETCH_ALL:
                result = cursor.fetchall()

        except Exception as e:
            print(e, file=sys.stderr)
        finally:
            conn.close()

        return result
