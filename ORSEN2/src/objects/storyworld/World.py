from operator import attrgetter
import numpy

MOVE_FEEDBACK = 1
MOVE_GENERAL_PUMP = 2
MOVE_SPECIFIC_PUMP = 3
MOVE_HINT = 4
MOVE_REQUESTION = 5
MOVE_UNKNOWN = 6
MOVE_PROMPT = 7
MOVE_SUGGESTING = 8
MOVE_FOLLOW_UP1 = 9
MOVE_FOLLOW_UP2 = 10

MOVE_FEEDBACK_GENERAL = 11
MOVE_FEEDBACK_SPECIFIC = 12
MOVE_FEEDBACK_HINT = 13
MOVE_FEEDBACK_SUGGESTING = 14

class World:

    def __init__(self, id="-1"):
        self.id = id

        # WORLD ELEMENTS
        self.characters = {}
        self.objects = {}
        self.relationships = {}
        self.settings = {}
        self.event_chain = []
        self.global_concept_list = []
        self.local_concept_list = []

        # RESPONSE ELEMENTS
        self.responses = [] #List of moves
        self.empty_response = 0
        self.general_response_count = 0

        # For suggestion
        self.continue_suggesting = 0 #1 means yes continue to suggest. #0 means no
        self.suggest_continue_count = 0
        self.subject_suggest = None #[Object, Object - Dog]

        
        #responses count
        self.feedback_count = 0
        self.general_pump_count = 0
        self.specific_pump_count = 0
        self.hint_count = 0
        self.suggest_count = 0
        self.prompt_count = 0
        self.followup1_count = 0
        self.followup2_count = 0

        self.feedback_general_count = 0
        self.feedback_specific_count = 0
        self.feedback_hint_count = 0
        self.feedback_suggest_count = 0

        #yes/ no
        self.yes = 0
        self.no = 0

        #don't like/ wrong
        self.dontLike = 0
        self.wrong = 0

        #inChoices/ none of the above
        self.inChoices = 0
        self.notInChoices = 0


    def add_character(self, char):
        if char.id not in self.objects and char.id not in self.characters:
            self.characters[char.id] = char
            return True
        elif char.id in self.objects and char.id not in self.characters:
            self.objects.pop(char.id)
            self.characters[char.id] = char
            return True
        else:
            return False

    def add_object(self, obj):
        if obj.id not in self.objects:
            self.objects[obj.id] = obj
            return True
        else:
            return False

    def add_relationship(self, relationship):
        if relationship.id not in self.relationships:
            self.relationships[relationship.id] = relationship
            return True
        else:
            return False

    def add_setting(self, setting):
        if setting.id not in self.settings:
            self.settings[setting.id] = setting
            return True
        else:
            return False

    def add_eventframe(self, event):
        event.seq_no = len(self.event_chain)
        self.event_chain.append(event)

    def get_main_character(self, rank=0):
        sorted_list = sorted(self.characters.values(), key=attrgetter('timesMentioned'), reverse=True)
        final = [sorted_list[rank]]

        for item in sorted_list:
            if item.timesMentioned == sorted_list[rank].timesMentioned:
                final.append(item)

        return final

    def get_top_characters(self, num_of_charas=3):
        sorted_list= sorted(self.characters.values(), key=attrgetter('timesMentioned'), reverse=True)

        if len(sorted_list) > num_of_charas:
            num_of_charas = len(sorted_list)

        return sorted_list[:num_of_charas]

    def get_main_object(self, rank=0):
        sorted_list = sorted(self.objects.values(), key=attrgetter('timesMentioned'), reverse=True)
        final = [sorted_list[rank]]

        for item in sorted_list:
            if item.timesMentioned == sorted_list[rank].timesMentioned:
                final.append(item)

        return final

    def get_top_objects(self, num_of_charas=3):
        sorted_list = sorted(self.objects.values(), key=attrgetter('timesMentioned'), reverse=True)

        if len(sorted_list) > num_of_charas:
            num_of_charas = len(sorted_list)

        return sorted_list[:num_of_charas]

    def add_response(self, response):
        self.responses.append(response)
        if response.type_num == MOVE_FEEDBACK or response.type_num == MOVE_GENERAL_PUMP:
            self.general_response_count += 1
        else:
            self.general_response_count = 0
        '''
            self.suggest_continue_count = 0
        elif response.type_num == MOVE_SUGGESTING:
            self.suggest_continue_count +=1
            self.general_response_count = 0
        elif response.type_num != MOVE_SUGGESTING or response.type_num != MOVE_UNKNOWN:
            print("HHHIIII")
            self.general_response_count = 0
            self.suggest_continue_count = 0'''
    
    def add_response_type_count(self, response):
        if response.type_num == MOVE_FEEDBACK:
            self.feedback_count += 1
        elif response.type_num == MOVE_GENERAL_PUMP:
            self.general_pump_count += 1
        elif response.type_num == MOVE_SPECIFIC_PUMP:
            self.specific_pump_count += 1
        elif response.type_num == MOVE_HINT: 
            self.hint_count += 1
        elif response.type_num == MOVE_SUGGESTING:
            self.suggest_count += 1
        elif response.type_num == MOVE_PROMPT: 
            self.prompt_count += 1
        elif response.type_num == MOVE_FOLLOW_UP1:
            self.followup1_count += 1
        elif response.type_num == MOVE_FOLLOW_UP2: 
            self.followup2_count += 1

        # curr_responses = [self.feedback_count, self.general_pump_count, self.specific_pump_count, self.hint_count, self.suggest_count]
        # for i in range (len(curr_responses)):
        #     print(curr_responses[i])

    def add_combination_response_type_count(self, type):
        if type == MOVE_FEEDBACK_GENERAL:
            self.feedback_general_count
        elif type == MOVE_FEEDBACK_SPECIFIC:
            self.feedback_specific_count
        elif type == MOVE_FEEDBACK_HINT:
            self.feedback_hint_count
        elif type == MOVE_FEEDBACK_SUGGESTING:
            self.feedback_suggest_count
        
    def compute_weights_dialogue(self, dm_fileWriter):
        total_responses = 0
        total_responses += self.feedback_count + self.general_pump_count + self.specific_pump_count + self.hint_count + self.suggest_count

        curr_responses = [self.feedback_count, self.general_pump_count, self.specific_pump_count, self.hint_count, self.suggest_count]
        elements = [1, 2, 3, 4, 8]
        weights = []
        for i in range (len(curr_responses)):
            if curr_responses[i] == 0:
                weights.append(0.1)
            else:
                weights.append(curr_responses[i]/total_responses)

        #print("F, GP, SP, H, S")
        #print("Weights", weights)

        weights = numpy.reciprocal(weights)            
        weights = weights / numpy.sum(weights)  
        
        print("F, GP, SP, H, S")
        print("Weights", weights)
        dm_fileWriter.write("Current weights: F, GP, SP, H, S: \n")
        dm_fileWriter.write(str(weights) +"\n")

        return numpy.random.choice(elements, p=weights) 
        
