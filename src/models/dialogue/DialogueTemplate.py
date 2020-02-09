import abc
from abc import ABC, abstractmethod
from src.dbo.concept import DBOConceptGlobalImpl, DBOConceptLocalImpl

from src import *
from src.Logger import Logger
from src.models.elements import Character, Object
from src.models.nlp import Relation
from src.models.concept import GlobalConcept, LocalConcept
import numpy as np


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


        if dialogue_type == DIALOGUE_TYPE_SUGGESTING:
            self.dbo_concept = DBOConceptLocalImpl()
        else:
            self.dbo_concept = DBOConceptGlobalImpl()
        self.relations_blanks = []

    def full_string(self):
        my_string = "(%s) %s" % (self.dialogue_type, self.get_string_response())
        my_string = my_string + "TEMPLATE: " + str(self.template) + "\n"
        my_string = my_string + "RELATION: " + str(self.relation) + "\n"
        my_string = my_string + "BLANKS  : " + str(self.blanks) + "\n"
        my_string = my_string + "NODES   : " + str(self.nodes) + "\n"
        my_string = my_string + "DEP NODE: " + str(self.dependent_nodes)

        return my_string

    def fill_blanks(self, event):
        pass

    def get_string_response(self):
        return "".join(self.template)

    def __str__(self):
        str = "(%s) %s" % (self.dialogue_type, self.get_string_response())
        return str

    def get_type(self):
        return self.dialogue_type

    def is_usable(self, curr_event, num_usage):
        decision = False
        if self.relation[0][0] == 'None':
            decision = True
        else:
            # Requires a relation
            if curr_event is None:
                decision = False
            else:
                if len(self.blanks) == 0:
                    return True
                elif len(self.blanks) == 1:
                    if self.is_usable_1_relation(curr_event):
                        decision = True
                else:
                    #if > 1 relation
                    decision = self.is_usable_relation(curr_event)
        self.is_move_usable = decision
        return decision


    def is_usable_relation(self, curr_event, suggesting_first_try = True):
        blank_list = []

        for i in range (len(self.blanks)):
            temp_list = []
            Logger.log_dialogue_model_basic("Current Blank: " + str(self.blanks[i]))

            if self.blanks[i] == 'Character' or self.blanks[i] == 'Object':
                # check <index> <Character>
                # check <index> <Object>
                temp_list = self.get_element_list(self.blanks[i], curr_event)
            elif self.blanks[i] == 'IsA':
                # check <index> <isA> weekday
                # TODO randomizer should not be here, will fix this pa
                temp_list = self.dbo_concept.get_concept_by_second_relation(self.relation[i][2], self.relation[i][1])
                Logger.log_dialogue_model_basic_example("List of Valid Relations: ")
                for x in range(len(temp_list)):
                    Logger.log_dialogue_model_basic_example(str(temp_list[x]))
                
                updated_list =[]
                if (len(temp_list) > 0):
                    updated_list.append(np.random.choice(temp_list))
                    Logger.log_dialogue_model_basic_example("Chosen Relation: ")
                    Logger.log_dialogue_model_basic_example(str(updated_list[0]))

                temp_list = updated_list
            else:
                #check <index> <relation> <index>
                temp_list = self.get_rel_list(blank_list, self.relation[i])
            
            if len(temp_list) > 0:
                blank_list = self.update_list(blank_list, temp_list)

            else:
                print("NO RELATIONS FOUND")
                Logger.log_dialogue_model_basic_example("NO RELATIONS FOUND")
                return False

        if len(blank_list) > 0:
            # TODO: Randomizer should not be here, relations_blanks for suggesting and hinting
            self.relations_blanks = blank_list
            return True
        else:
            print("NO RELATIONS FOUND")
            Logger.log_dialogue_model_basic_example("NO RELATIONS FOUND")
        return False

    def update_list(self, init_list, to_add_list):
        final_list = []
        #CELINA NOTES: Why may "[]" yun X? [X]
        # TODO: Randomizer should not be here

        #if first input
        if len(init_list) == 0:
            for X in to_add_list:
                final_list.append([X])
            return final_list

        print("Init List: ", init_list)
        print("To Add List: ", to_add_list)

        for X in init_list:
            for Y in to_add_list:
                print(type(Y))
                if type(Y) == Object or type(Y) == Character:
                    temp_list = []
                    temp_list.extend(X)
                    temp_list.append(Y)
                    final_list.append(temp_list)
                elif type(Y) == list:
                    if len(Y) > 0:
                        temp_list = []
                        temp_list.extend(X)
                        temp_list.extend(Y)
                        final_list.append(temp_list)
                # IDK If this will work
                else:
                    temp_list = []
                    temp_list.extend(X)
                    temp_list.append(Y)
                    final_list.append(temp_list)
        
        return final_list

        # print("NEW")
        # for x in final_list:
        #     print(x)
        # print("FF", final_list)
        # return final_list

    def get_element_list(self, element_type, curr_event):
        # editted this code kasi all characters, objects ang nasasama? We only need one.
        # TODO: Fix the code such that it gets all possible objects and characters sa suggesting/hinting DT pa pipili which one
        # Randomizer should not be here
        element_list = []
        temp_list = []
        
        if element_type == 'Character':
            element_list = curr_event.get_characters_involved()
        elif element_type == 'Object':
            element_list = curr_event.get_objects_involved()

        Logger.log_dialogue_model_basic_example("List of Valid Objects and Characters 1: ")
        for x in range(len(element_list)):
            Logger.log_dialogue_model_basic_example(str(element_list[x]))

        updated_list = []
        if len(element_list) != 0:
            print("Element List: ", element_list)

            # idk if dapat may randomizer dito
            temp_list.append(np.random.choice(element_list))

            for X in element_list:
                concept_list = []
                concept_list = self.dbo_concept.get_specific_concept(X.name, 'IsA', element_type)
                if concept_list is not None:
                    temp_list.append(X)

        Logger.log_dialogue_model_basic_example("List of Valid Objects and Characters 2: ")
        for x in range(len(temp_list)):
            Logger.log_dialogue_model_basic_example(str(temp_list[x]))

        # idk if dapat may randomizer dito
        if len(temp_list) != 0:
            updated_list.append(np.random.choice(temp_list))

        # Original code below
        # updated_list = []
        # for X in element_list:
        #     concept_list = []
        #     concept_list = self.dbo_concept.get_specific_concept(X.name, 'IsA', element_type)
        #     if concept_list is not None:
        #         updated_list.append(X)

        # Logger.log_dialogue_model_basic_example("List of Valid Objects and Characters: ")
        # for x in range(len(updated_list)):
        #     Logger.log_dialogue_model_basic_example(str(updated_list[x]))

        if len(updated_list) != 0:
            Logger.log_dialogue_model_basic_example("Chosen Object Character: ")
            Logger.log_dialogue_model_basic_example(str(updated_list[0]))

        return updated_list

    def get_rel_list(self, init_list, relation):
        # TODO: Randomizer should not be here
        temp_list =[]
        for X in init_list:
            if len(X) > int(relation[0]) - 1:
                print("X len is: ", len(X))
                curr_refer = X[int(relation[0]) - 1]

                # idk if dapat may randomizer dito
                # curr_refer = np.random.choice(curr_refer_list)

                if type(curr_refer) == Character or type(curr_refer) == Object:
                    print("testing: ", curr_refer.name)
                    temp_list.append(self.dbo_concept.get_concept_by_first_relation(curr_refer.name, relation[1]))
                else:
                    print("testing: ", curr_refer.first)
                    temp_list.append(self.dbo_concept.get_concept_by_first_relation(curr_refer.first, relation[1])) 
            else:
                for items in range(len(X)):
                    if isinstance(X[items], LocalConcept):
                        curr_refer = X[items]
                        print("testing: ", curr_refer.second)
                        temp_list.append(self.dbo_concept.get_concept_by_second_relation(curr_refer.second, relation[1])) 
        
        Logger.log_dialogue_model_basic_example("List of all Valid Relations: ")
        if (len(temp_list)) > 0:
            for x in range(len(temp_list[0])):
                Logger.log_dialogue_model_basic_example(str(temp_list[0][x]))
               
        updated_list =[]
        if (len(temp_list)) > 0:
            if(len(temp_list[0])) > 0:
                updated_list.append(np.random.choice(temp_list[0]))
                Logger.log_dialogue_model_basic_example("Chosen Relation: ")
                Logger.log_dialogue_model_basic_example(str(updated_list[0]))

        return updated_list

    def is_usable_1_relation(self, curr_event):
        blank_type = self.blanks[0]
        if blank_type == 'Repeat' or blank_type == 'Prompt':
            return True
        elif blank_type == 'Character':
            # check if character exists
            if len(curr_event.get_characters_involved()) > 0:
                return True
            return False
        elif blank_type == 'Event':
            # check if action event, if not return false
            if curr_event.get_type() == EVENT_ACTION:
                return True
            return False
        elif blank_type == 'Object' or blank_type == 'Item':
            # check if object exists
            if len(curr_event.get_objects_involved()) > 0:
                return True
            return False
        elif blank_type == 'Emotion':
            # if len(curr_event) > 0:
            #     if curr_event
            print("EMOTION IS PRESENT: ", curr_event.emotion)
            if curr_event is not "":
                return True
        return False

    def get_word_relations(self):
        word_rel = []
        if len(self.relations_blanks) > 0:
            for X in self.relation:
                #get first val
                if type(self.relations_blanks[0][int(X[0])-1]) == Character or type(self.relations_blanks[0][int(X[0])-1]) == Object:
                    first_val = self.relations_blanks[0][int(X[0])-1].name
                else:
                    first_val = self.relations_blanks[0][int(X[0])-1].first

                if X[1] == 'Object':
                    word_rel.append(Relation(first = first_val, relation = 'IsA', second = 'object'))
                elif X[1] == 'Character':
                    word_rel.append(Relation(first=first_val, relation='IsA', second='character'))
                elif X[1] == 'IsA':
                    word_rel.append(Relation(first=first_val, relation='IsA', second=X[2]))
                else:
                    # get second val
                    if type(self.relations_blanks[0][int(X[2])-1]) == Character or type(self.relations_blanks[0][int(X[2])-1]) == Object:
                        second_val = self.relations_blanks[0][int(X[2])-1].name
                    else:
                        #I changed the .first to .second
                        second_val = self.relations_blanks[0][int(X[2])-1].second

                    word_rel.append(Relation(first=first_val, relation=X[1], second=second_val))

        return word_rel

    def check_subject(self, subj_to_check):
        subj_to_check = subj_to_check.lower()

        if subj_to_check == 'i' or subj_to_check == 'we' or subj_to_check == 'us':
            return 'you'
        elif subj_to_check == 'my':
            return 'your'
        return subj_to_check

    @staticmethod
    @abstractmethod
    def get_template_to_use(self):
        # check if it has usable templates
        return []


