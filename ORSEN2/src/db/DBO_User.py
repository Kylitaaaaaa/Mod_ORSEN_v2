from src.db.SqlConnector import SqlConnConcepts
from src.db.User import User

def get_user_by_id(id):
    sql = "SELECT iduser, " \
          "name, " \
          "code " \
          "FROM users " \
          "WHERE iduser = %d;" % id

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = None

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        row = cursor.fetchone()
        
        id          = row[0]
        name        = row[1]
        code        = row[2]

        resulting = User(id, name, code)

    except:
        print("Error User: unable to fetch data of user #%d" % id)

    conn.close()
    return resulting


def get_all_users():
    sql = "SELECT iduser, " \
          "name, " \
          "code " \
          "FROM users " \

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            id          = row[0]
            name        = row[1]
            code        = row[2]

            resulting.append(User(id, name, code))

    except:
        print("Error User: unable to fetch all data")

    conn.close()
    return resulting

def get_user_specified(name, code):
    sql = "SELECT iduser, " \
          "name, " \
          "code " \
          "FROM users " \
          "WHERE name = %s AND code = %s"

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = None

    try:
        # Execute the SQL command
        cursor.execute(sql, (name, code,))
        # Fetch all the rows in a list of lists.
        row = cursor.fetchone()
        id          = row[0]
        name        = row[1]
        code        = row[2]

        resulting = User(id, name, code)

    except:
        print("Error User: unable to fetch data for name "+ name)

    conn.close()
    return resulting

def get_user_id(name, code):
    sql = "SELECT iduser " \
          "FROM users " \
          "WHERE name = %s AND code = %s"

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    try:
        # Execute the SQL command
        cursor.execute(sql, (name, code,))
        # Fetch all the rows in a list of lists.
        row = cursor.fetchone()
        return row[0]

    except:
        print("Error User: unable to fetch data for name "+ name + " " + code)

    conn.close()
    return -1

def add_user(user):
    sql = "INSERT INTO users " \
          "(name, " \
          "code) " \
          "VALUES " \
          "(%s, " \
          " %s);"

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (user.name, user.code,))
        conn.commit()
        conn.close()
        return True

    except:
        print("Error User: unable to insert data "+ user.__str__())
        conn.close()
        return False