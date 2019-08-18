from ..SqlConnector import SqlConnConcepts
from src.objects.concepts.Local_Concept import Local_Concept

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

LOCATED_NEAR = "LocatedNear"

RELATIONS = [IS_A, PART_OF, AT_LOCATION, HAS_PREREQ, CREATED_BY, USED_FOR, CAUSES, DESIRES, CAPABLE_OF, HAS_PROPERTY,
             HAS_A, RECEIVES_ACTION]

def get_concept_by_id(id):
    sql = "SELECT idlocal, " \
          "userid," \
          "relation," \
          "first," \
          "second, " \
          "score, " \
          "valid " \
          "FROM local_concepts " \
          "WHERE idlocal = %d;" % id

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = None

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        row = cursor.fetchone()
        
        id          = row[0]
        userid      = row[1]
        relation    = row[2]
        first       = row[3]
        second      = row[4]
        score       = row[5]
        valid       = row[6]

        resulting = Local_Concept(id, userid, first, relation, second, score, valid)

    except:
        print("Error Concepts: unable to fetch data of character #%d" % id)

    conn.close()
    return resulting


def get_all_concepts():
    sql = "SELECT idlocal, " \
          "userid," \
          "relation," \
          "first," \
          "second, " \
          "score, " \
          "valid " \
          "FROM local_concepts " \

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            id          = row[0]
            userid      = row[1]
            relation    = row[2]
            first       = row[3]
            second      = row[4]
            score       = row[5]
            valid       = row[6]

            resulting.append(Local_Concept(id, userid, first, relation, second, score, valid))

    except:
        print("Error Concepts: unable to fetch all data")

    conn.close()
    return resulting


def get_word_concept(word):
    sql = "SELECT idlocal, " \
          "userid," \
          "relation," \
          "first," \
          "second, " \
          "score, " \
          "valid " \
          "FROM local_concepts " \
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
            userid      = row[1]
            relation    = row[2]
            first       = row[3]
            second      = row[4]
            score       = row[5]
            valid       = row[6]

            resulting.append(Local_Concept(id, userid, first, relation, second, score, valid))

    except:
        print("Error Concept: unable to fetch data for word "+word)

    conn.close()
    return resulting


def get_concept(word, relation):
    sql = "SELECT idlocal, " \
          "userid," \
          "relation," \
          "first," \
          "second, " \
          "score, " \
          "valid " \
          "FROM local_concepts " \
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
            userid      = row[1]
            relation    = row[2]
            first       = row[3]
            second      = row[4]
            score       = row[5]
            valid       = row[6]

            resulting.append(Local_Concept(id, userid, first, relation, second, score, valid))

    except:
        print("Error Concept: unable to fetch data for word "+word)

    conn.close()
    return resulting


def get_concept_specified(first, relation, second):
    sql = "SELECT idlocal, " \
          "userid," \
          "relation," \
          "first," \
          "second, " \
          "score, " \
          "valid " \
          "FROM local_concepts " \
          "WHERE first = %s AND second = %s AND relation = %s "

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = None

    try:
        # Execute the SQL command
        cursor.execute(sql, (first, second, relation,))
        # Fetch all the rows in a list of lists.
        row = cursor.fetchone()

        id          = row[0]
        userid      = row[1]
        relation    = row[2]
        first       = row[3]
        second      = row[4]
        score       = row[5]
        valid       = row[6]

        resulting = Local_Concept(id, userid, first, relation, second, score, valid)

    except:
        print("Error Concept: unable to fetch data for word "+first+" and "+second)

    conn.close()
    return resulting


def get_concept_like(relation, first="", second=""):
    sql = "SELECT idlocal, " \
          "userid," \
          "relation," \
          "first," \
          "second, " \
          "score, " \
          "valid " \
          "FROM local_concepts " \
          "WHERE first LIKE '%\%s%' AND second LIKE '%\%s%' AND relation = '\%s' AND valid = \%s"

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        cursor.execute(sql, (first, second, relation,str(1),))
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()
        print("LOCAL, LENGTH OF RESULT:", len(result))

        for row in result:
            id          = row[0]
            userid      = row[1]
            relation    = row[2]
            first       = row[3]
            second      = row[4]
            score       = row[5]
            valid       = row[6]

            resulting.append(Local_Concept(id, userid, first, relation, second, score, valid))

    except:
        print("Error Concept: unable to fetch like data")

    conn.close()
    return resulting


def add_concept(concept):
    sql = "INSERT INTO local_concepts " \
          "(userid, " \
          "relation, " \
          "first, " \
          "second, " \
          "score, " \
          "valid) " \
          "VALUES " \
          "(%s, " \
          " %s, " \
          " %s, " \
          " %s, " \
          " %s, " \
          " %s);"

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (concept.userid, concept.relation, concept.first, concept.second, concept.score, concept.valid,))
        conn.commit()
        conn.close()
        return True

    except:
        print("Error Concept: unable to insert data "+concept.__str__())
        conn.close()
        return False

def update_score(id, score):
    sql = "UPDATE local_concepts " \
          "SET score = %s " \
          "WHERE idlocal = %s;" 

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (str(score), str(id)))
        conn.commit()
        conn.close()
        return True

    except:
        print("Error Concept: unable to update score of id "+ str(id))
        conn.close()
        return False

def update_valid(id, valid):
    sql = "UPDATE local_concepts " \
          "SET valid = %s " \
          "WHERE idlocal = %s;" 

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (str(valid), str(id)))
        conn.commit()
        conn.close()
        return True

    except:
        print("Error Concept: unable to update validity of id "+ str(id))
        conn.close()
        return False