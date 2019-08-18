class Move:

    def __init__(self, 
                move_id=-1, response_type="", template=[], relations =[], blanks=[], nodes=[], dependent_nodes=[], dict_nodes = {},
                blank_index=[], type_num=-1, 
                subject=None, concept_id=-1, dbtype = ""):
        self.move_id = move_id #ID template
        self.response_type = response_type
        self.template = template #response "I see, what happened next? etc" Naka list siya, hinahati by _start_
        self.relations = relations
        self.blanks = blanks
        self.nodes = nodes
        self.dependent_nodes = dependent_nodes
        self.dict_nodes = dict_nodes

        self.subject_type_list = [] #Appends the type of the subject
        self.follow_up_relations = [] #Which local id was used + at which curr_blank
        self.subjects_for_suggestion = [] #Appends all charas objects used

        self.choices_relationID = []


        #self.type = type
        self.blank_index = blank_index
        self.type_num = type_num #What type of dialogue move
        self.subject = subject
        self.dbtype = dbtype #local or global?   Di ko ginagamit?  

    '''
    def fill_blank(self, fill):
        for i in range(0, len(fill)):
            self.template[self.blank_index[i]] = fill[i]'''
    
    def fill_blank_prompt(self, fill):
        for i in range(len(self.template)):
            for j in range(len(self.nodes)):
                if self.template[i] == self.nodes[j]:
                    self.template[i] = fill

    def get_string_response(self):
        string = ""

        for s in self.template:
            string += str(s)

        return string

    def __str__(self):
        string = "MOVE:" + self.response_type +"\n"+ str(self.template) +\
                "\n" + str(self.blanks) + "\n" + str(self.blank_index)+"\n"
        if self.subject is not None:
            string += str(self.subject.name)+" : "+repr(self.subject)
        else:
            string += "No subject."
        
        string += "\n -----"

        return string