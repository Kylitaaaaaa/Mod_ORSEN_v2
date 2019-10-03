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

    def fill_blanks(self, event):
        #if it does not require any details
        if len(self.relation) == 0:
            return self.template

        response = self.template
        for i in range (len(self.nodes)):
            to_insert = ""
            curr_index = response.index(self.nodes[i])
            if self.blanks[i] == 'Character':
                to_insert = event.get_characters_involved()[0]
            elif self.blanks[i] == 'Object':
                to_insert = event.get_objects_involved()[0]
            elif self.blanks[i] == 'Event':
                to_insert = event.get_subject() + " " + event.get_verb() + " " +  event.get_direct_object() + " " +  event.get_adverb() + " " +  event.get_preposition() + " " +  event.get_object_of_preposition()
            elif self.blanks[i] == 'Repeat':
                if event.get_type() == EVENT_ACTION:
                    to_insert = event.get_subject() + " " + event.get_verb() + " " + event.get_direct_object() + " " + event.get_adverb() + " " + event.get_preposition() + " " + event.get_object_of_preposition()
                elif event.get_type() == EVENT_CREATION:
                    to_insert = event.get_subject()
                elif event.get_type() == EVENT_DESCRIPTION:
                    to_insert = event.get_subject() + " is "
                    for j in range (len(event.get_attributes())):
                        if j == len(event.get_attributes()) - 1:
                            to_insert = to_insert
                        else:
                            to_insert = to_insert + " and "

            response[curr_index] = to_insert

        return response

    def get_string_response(self):
        return "".join(self.template)

    def __str__(self):
        str = "(%s) %s" % (self.dialogue_type, self.get_string_response())
        return str

    def get_type(self):
        return self.dialogue_type


    def is_usable(self, curr_event):
        # print('CHECKING IS USABLE: ', self.relation[0][1])
        decision = False
        # Requires a relation
        if self.relation[0][0] == 'None':
            decision = True
        else:
            if curr_event is None:
                decision = False
            else:
                if self.is_usable_1_relation(self.relation[0][1], curr_event):
                    decision = True
            # if len(curr_event) == 0:
            #     return False
            # else:
            #     #if only 1 relation
            #     if len(self.relation) == 1:
            #         for X in curr_event:
            #             if self.is_usable_1_relation(self.relation[0][1], X):
            #                 return True

        self.is_move_usable = decision
        return decision

    def is_usable_1_relation(self, relation, curr_event):
        if relation == 'Repeat':
            return True
        elif relation == 'Character':
            #check if character exists
            print("NUM ACTION: ", curr_event.get_characters_involved())
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
            print("NUM OBJECTS: ", curr_event.get_objects_involved())
            if len(curr_event.get_objects_involved()) > 0:
                return True
            return False
        return False

    @staticmethod
    @abstractmethod
    def get_template_to_use(self):
        # check if it has usable templates
        return []
