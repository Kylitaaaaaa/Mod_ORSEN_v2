from src.db.SqlConnector import SqlConnConcepts
from .Move import Move

TYPE_FEEDBACK = "feedback"
TYPE_GENERAL_PUMP = "general"
TYPE_SPECIFIC_PUMP = "specific"
TYPE_HINT = "hinting"
TYPE_REQUESTION = ""
TYPE_SUGGESTING = "suggesting"

#This function is not being used
def get_specific_template(id):
    sql = "SELECT idtemplates, " \
          "response_type," \
          "template," \
          "blank_types " \
          "FROM templates " \
          "WHERE idtemplates = %d;" % id

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
        response    = row[1]
        template       = row[2]
        blank      = row[3]

        template_split = str(template).split("_")
        template_blanked = str(template).split(" ")
        blanks = str(blank).split(",")

        blank_index = []

        for i in range(0, len(template_split)):
            is_found = False

            item = template_split[i]

            for blanked in template_blanked:
                test = "_"+item+"_"

                if (not is_found) and (test in blanked):
                    blank_index.append(i)
                    is_found = True

        resulting = Move(id, response, template_split,blanks, blank_index)

    except:
        print("Error MOVES: unable to fetch template #%d" % id)

    conn.close()
    return resulting

def get_templates_of_type(type):

    sql = "SELECT idtemplates, " \
          "response_type, " \
          "template, " \
          "relations, " \
          "blank_types, " \
          "nodes, " \
          "dependent_nodes " \
          "FROM templates " \
          "WHERE response_type = '%s';" % type

    conn = SqlConnConcepts.get_connection()
    cursor = conn.cursor()

    resulting = []

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        result = cursor.fetchall()

        for row in result:
            id          = row[0]
            response    = row[1]
            template    = row[2]
            relations   = row[3]
            blank_types = row[4]
            nodes       = row[5]
            dependent_nodes = row[6]
            
            template = str(template).split("_")
            relations_split = str(relations).split(",")
            blanks = str(blank_types).split(",")
            nodes = str(nodes).split(",")
            dependent_nodes = str(dependent_nodes).split(",")  

            relations = []
            for i in range(len(relations_split)):
                x = relations_split[i].split(" ")
                x[:] = (value for value in x if value != "")
                relations.append(x)

            dict_nodes = {}
            for i in nodes:
                dict_nodes[i] = ""

            resulting.append(Move(id, response, template, relations, blanks, nodes, dependent_nodes, dict_nodes))

    except:
        print("Error Moves: unable to fetch data of type %s" % type)

    conn.close()
    return resulting