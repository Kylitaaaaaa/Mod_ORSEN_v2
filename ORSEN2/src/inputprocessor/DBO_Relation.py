from src.db.SqlConnector import SqlConnConcepts
from src.inputprocessor.Relation import Relation

def get_all_extraction_templates():
    sql = "SELECT idextraction, " \
          "relation, " \
          "first, " \
          "keywords, " \
          "second, " \
          "third, " \
          "keyword_type, " \
          "is_flipped " \
          "FROM extraction_templates "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            id          = row[0]
            relation    = row[1]
            first       = row[2]
            keywords    = row[3]
            second      = row[4]
            third       = row[5]
            keyword_type = row[6]
            is_flipped  = row[7]

            resulting.append(Relation(id, relation, first, keywords, second, third, keyword_type, is_flipped))

    except:
        print("Error Relations Templates: unable to fetch all data")

    conn.close()
    return resulting

def get_unique_first():
    sql = "SELECT DISTINCT first " \
          "FROM extraction_templates"

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()

        for row in result:
            first      = row[0]

            resulting.append(first)

    except:
        print("Error Relation: unable to fetch data for unique firsts")

    conn.close()
    return resulting

def get_second_where_first(first):
    sql = "SELECT DISTINCT second " \
          "FROM extraction_templates " \
          "WHERE first = %s "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        # Execute the SQL command
        cursor.execute(sql, (first,))
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()

        for row in result:
            second      = row[0]

            resulting.append(second)

    except:
        print("Error Relation: unable to fetch data for second where first is " + first)

    conn.close()
    return resulting

def get_keywords(first, second):
    sql = "SELECT keywords " \
          "FROM extraction_templates " \
          "WHERE first = %s AND second = %s "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        # Execute the SQL command
        cursor.execute(sql, (first, second,))
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()

        for row in result:
            keywords      = row[0]

            resulting.append(keywords)

    except:
        print("Error Relation: unable to fetch data for keywords where first is " + first + " second is " + second)

    conn.close()
    return resulting

def get_keyword_type(first, second):
    sql = "SELECT keyword_type " \
          "FROM extraction_templates " \
          "WHERE first = %s AND second = %s "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        # Execute the SQL command
        cursor.execute(sql, (first, second,))
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()

        for row in result:
            keyword_type      = row[0]

            resulting.append(keyword_type)

    except:
        print("Error Relation: unable to fetch data for keyword type where first is " + first + " second is " + second)

    conn.close()
    return resulting

def get_matching_relation_pattern(first, keywords, second):
    sql = "SELECT idextraction, " \
          "relation, " \
          "third, " \
          "keyword_type, " \
          "is_flipped " \
          "FROM extraction_templates " \
          "WHERE first = %s AND second = %s AND keywords = %s "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = None

    try:
        # Execute the SQL command
        cursor.execute(sql, (first, second, keywords,))
        # Fetch all the rows in a list of lists.
        result = cursor.fetchone()

        if result != None:
            id          = result[0]
            relation    = result[1]
            third       = result[2]
            keyword_type = result[3]
            is_flipped  = result[4]

            resulting = (Relation(id, relation, first, keywords, second, third, keyword_type, is_flipped))

    except:
        print("Error Relation: unable to fetch data for first is " + first + ", second is " + second + " and third is " + third)

    conn.close()
    return resulting