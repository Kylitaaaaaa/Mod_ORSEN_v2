from ..SqlConnector import SqlConnConcepts
from src.objects.concepts.Concept import Concept

IS_A = "IsA"
PART_OF = "PartOf"
AT_LOCATION = "AtLocation"
HAS_PREREQ = "HasPrerequisite"
CREATED_BY = "CreatedBy"
USED_FOR = "UsedFor"
CAUSES = "Causes"
DESIRES = "Desires"
CAPABLE_OF = "CapableOf"
HAS_PROPERTY = "HasProperty"
HAS_A = "HasA"
RECEIVES_ACTION = "ReceivesAction"

RELATIONS = [IS_A, PART_OF, AT_LOCATION, HAS_PREREQ, CREATED_BY, USED_FOR, CAUSES, DESIRES, CAPABLE_OF, HAS_PROPERTY,
             HAS_A, RECEIVES_ACTION]


def get_specific_concept(id):
    sql = "SELECT idconcepts, " \
          "relation," \
          "first," \
          "second " \
          "FROM concepts " \
          "WHERE idconcepts = %d;" % id

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = None

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        result = cursor.fetchone()
        row = result
        id          = row[0]
        relation    = row[1]
        first       = row[2]
        second      = row[3]

        resulting = Concept(id, first, relation, second)

    except:
        print("Error Concepts: unable to fetch data of character #%d" % id)

    conn.close()
    return resulting


def get_all_concepts():
    sql = "SELECT idconcepts, " \
          "relation," \
          "first," \
          "second " \
          "FROM concepts "

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
            second      = row[3]

            resulting.append(Concept(id, first, relation, second))

    except:
        print("Error Concepts: unable to fetch all data")

    conn.close()
    return resulting


def get_word_concept(word):
    sql = "SELECT idconcepts, " \
          "relation," \
          "first," \
          "second " \
          "FROM concepts " \
          "WHERE first = %s OR second = %s "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        cursor.execute(sql, (word, word,))
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()

        for row in result:
            id          = row[0]
            relation    = row[1]
            first       = row[2]
            second      = row[3]

            resulting.append(Concept(id, first, relation, second))

    except:
        print("Error Concept: unable to fetch data for word "+word)

    conn.close()
    return resulting


def get_concept(word, relation):
    sql = "SELECT idconcepts, " \
          "relation," \
          "first," \
          "second " \
          "FROM concepts " \
          "WHERE (first = %s OR second = %s) AND relation = %s "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        # Execute the SQL command
        cursor.execute(sql, (word, word, relation,))
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()

        for row in result:
            id          = row[0]
            relation    = row[1]
            first       = row[2]
            second      = row[3]

            resulting.append(Concept(id, first, relation, second))

    except:
        print("Error Concept: unable to fetch data for word "+word)

    conn.close()
    return resulting


def get_concept_specified(first, relation, second):
    sql = "SELECT idconcepts, " \
          "relation," \
          "first," \
          "second " \
          "FROM concepts " \
          "WHERE first = %s AND second = %s AND relation = %s "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = None

    try:
        # Execute the SQL command
        cursor.execute(sql, (first, second, relation,))
        # Fetch all the rows in a list of lists.
        result = cursor.fetchone()

        if result != None:
            id          = result[0]
            relation    = result[1]
            first       = result[2]
            second      = result[3]

            resulting = (Concept(id, first, relation, second))

    except:
        print("Error Concept: unable to fetch data for word " + first + " and " + second + " relation: " + relation)

    conn.close()
    return resulting


def get_concept_like(relation, first="", second=""):
    sql = "SELECT idconcepts, " \
          "relation," \
          "first," \
          "second " \
          "FROM concepts " \
          "WHERE first LIKE '%"+first+"%' AND second LIKE '%"+second+"%' AND relation = '"+relation+"'"

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()
        print("GLOBAL, LENGTH OF RESULT:", len(result))

        id = -1
        relation = ""
        first = ""
        second = ""

        for row in result:
            id          = row[0]
            relation    = row[1]
            first       = row[2]
            second      = row[3]

            resulting.append(Concept(id, first, relation, second))

    except:
        print("Error Concept: unable to fetch like data")

    conn.close()
    return resulting


def add_concept(concept):
    sql = "INSERT INTO concepts " \
          "(relation, " \
          "first, " \
          "second) " \
          "VALUES " \
          "(%s, " \
          " %s, " \
          " %s);"

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (concept.relation, concept.first, concept.second,))
        conn.commit()
        conn.close()
        return True

    except:
        print("Error Concept: unable to insert data "+concept.__str__())
        conn.close()
    return False