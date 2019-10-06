import abc
from abc import ABC, abstractmethod

from src import *



class DialogueTemplate(ABC):
    __metaclass__ = abc.ABCMeta

    def __init__(self, id=-1, dialogue_type='', template=[], relation=[], blanks=[], nodes=[], dependent_nodes=[]):
        self.id = id
        self.dialogue_type = dialogue_type
        self.template = template
        self.relation = relation
        self.blanks = blanks
        self.nodes = nodes
        self.dependent_nodes = dependent_nodes
        self.is_move_usable = False

    def full_string(self):
        my_string = "(%s) %s" % (self.dialogue_type, self.get_string_response())
        my_string = my_string + "TEMPLATE: " + str(self.template) + "\n"
        my_string = my_string + "RELATION: " + str(self.relation) + "\n"
        my_string = my_string + "BLANKS  : " + str(self.blanks) + "\n"
        my_string = my_string + "NODES   : " + str(self.nodes) + "\n"
        my_string = my_string + "DEP NODE: " + str(self.dependent_nodes)

        return my_string
#    def fill_blanks(self, event):
#        #if it does not require any details
#        print("relations are: ")
#        print(self.relation)
#        if self.relation[0][0] is None:
#            return self.template
#
#        print("subject name: ", event.subject.name)
#        print("subject: ", event.subject)
#        response = self.template
#        for i in range (len(self.nodes)):
#            to_insert = ""
#            curr_index = response.index(self.nodes[i])
#            if self.blanks[i] == 'Character':
#                to_insert = event.get_characters_involved()[0].name
#            elif self.blanks[i] == 'Object':
#                to_insert = event.get_objects_involved()[0].name
#            elif self.blanks[i] == 'Event':
#                to_insert = event.subject.name + " " + event.verb + " " +  event.direct_object.name + " " +  event.adverb + " " +  event.preposition + " " +  event.object_of_preposition
#            elif self.blanks[i] == 'Repeat':
#                if event.get_type() == EVENT_ACTION:
#                    to_insert = event.subject.name + " " + event.verb + " " +  event.direct_object.name + " " +  event.adverb + " " +  event.preposition + " " +  event.object_of_preposition
#                elif event.get_type() == EVENT_CREATION:
#                    to_insert = event.subject.name
#                elif event.get_type() == EVENT_DESCRIPTION:
#                    to_insert = event.subject.name + " is "
#                    # for j in range (len(event.get_attributes())):
#                    #     if j == len(event.get_attributes()) - 1:
#                    #         to_insert = to_insert
#                    #     else:
#                    #         to_insert = to_insert + " and "
#
#            response[curr_index] = to_insert
#
#        return response

    def fill_blanks(self, event):
        pass
        
    
    def get_string_response(self):
        return "".join(self.template)

    def __str__(self):
        str = "(%s) %s" % (self.dialogue_type, self.get_string_response())
        return str

    def get_type(self):
        return self.dialogue_type


    def is_usable(self, curr_event):
        # print('CHECKING IS USABLE: ', self.relation[0][1])


        #TODO: UNCOMMENT

        decision = False
        if self.relation[0][0] == 'None':
            decision = True
        else:
            # Requires a relation
            if curr_event is None:
                decision = False
            else:
                if self.is_usable_1_relation(self.relation[0][1], curr_event):
                    decision = True
        self.is_move_usable = decision
        return decision

        ###TODO remove
        # if self.relation[0][0] == 'None':
        #     return False
        # return True

    def is_usable_1_relation(self, relation, curr_event):
        if relation == 'Repeat' or relation == 'Prompt':
            return True
        elif relation == 'Character':
            #check if character exists
            # print("NUM ACTION: ", curr_event.get_characters_involved())
            if len(curr_event.get_characters_involved()) > 0:
                return True
            return False
        elif relation == 'Event':
            #check if action event, if not return false
            if curr_event.get_type() == EVENT_ACTION:
                return True
            return False
        elif relation == 'Object' or relation == 'Item':
            #check if object exists
            # print("NUM OBJECTS: ", curr_event.get_objects_involved())
            if len(curr_event.get_objects_involved()) > 0:
                return True
            return False
        return False

    @staticmethod
    @abstractmethod
    def get_template_to_use(self):
        # check if it has usable templates
        return []
