class Follow_Up:

    def __init__(self, id, template_id , follow_up_template):
        self.id = id
        self.template_id = template_id 
        self.follow_up_template = follow_up_template
    
        self.final_template_list = [] #For follow up, Ex. person can eat
        self.choices_relationID = []
        self.start = 65

        self.final_response = ""
    
    def print(self):
        print("id: ", self.id)
        print("template_id: ", self.template_id)
        print("follow_up_template: ", self.follow_up_template)
    
    def fill_blank_template(self, follow_up_relations, dict_nodes):
        for x in range(len(follow_up_relations)):
            temp = self.follow_up_template[follow_up_relations[x][0]]
            # ADD _1_ is a weather stuff
            if (len(temp) == 2):
                self.final_template_list.append([chr(self.start) + ". ", dict_nodes[temp[0]], temp[1]])
            else:
                self.final_template_list.append([chr(self.start) + ". ", dict_nodes[temp[0]], temp[1], dict_nodes[temp[2]]])
            self.choices_relationID.append([chr(self.start), follow_up_relations[x][1]])

            self.start = self.start + 1
    
    def get_string_template(self):
        for x in range(len(self.final_template_list)):
            for y in range (len(self.final_template_list[x])):
                self.final_response += self.final_template_list[x][y]

            self.final_response += " ||| "
            
            if x == len(self.final_template_list)-1:
                self.final_response += chr(self.start) + ". None of the Above"
        
        return self.final_response

    

                

