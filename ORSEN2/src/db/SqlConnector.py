import pymysql


class SqlConnector:
    'Connector for ORSEN\'s schema and the server'

    location = "localhost"
    username = "root"
    password = "1qw23er45"
    schema   = ""

    def __init__(self, schema):
        self.schema     = schema

    @staticmethod
    def get_connection():
        return None

    @staticmethod
    def close(db_connection):
        db_connection.close()

# -------------------------------------------------

class SqlConnConcepts(SqlConnector):
    'Connector for ORSEN\'s event chain database'

    schema = "orsen_kb"

    @staticmethod
    def get_connection():
        return pymysql.connect(SqlConnConcepts.location,
                               SqlConnConcepts.username,
                               SqlConnConcepts.password,
                               SqlConnConcepts.schema)

# -------------------------------------------------
