import numpy as np

from src import DEFAULT_SEED
from src.constants import DIALOGUE_TYPE_KNOWLEDGE_ACQUISITION_PUMPING #[Celina]
from src.Logger import Logger


class ContentDetermination:

    def __init__(self):
        super().__init__()
        self.move_to_execute = ""
        self.curr_event = []
        np.random.seed(DEFAULT_SEED)

    def set_state(self, move_to_execute, curr_event, usable_template_list):
        self.move_to_execute = move_to_execute
        self.curr_event = curr_event
        self.usable_template_list = usable_template_list

    def reset_state(self):
        self.move_to_execute = ""
        self.curr_event = []
        self.usable_template_list = []

    def perform_content_determination(self, dialogue_history):
        Logger.log_dialogue_model("Filling up the template")
        print("FETCHING: ", self.move_to_execute)

        #choose template
        chosen_template = self.choose_template()
        print("CHOSEN TEMPLATE IS: ", chosen_template)

        #fill template to use
        # if template has no fillable blanks, enter this particular if statement
        if len(chosen_template.template) == 1:
            response = chosen_template.template[0]
            
        # [CELINA] Added the dialogue history for this part
        elif self.move_to_execute == DIALOGUE_TYPE_KNOWLEDGE_ACQUISITION_PUMPING:
            response = chosen_template.fill_blanks(dialogue_history)

        else:
            print("=============")
            print(self.curr_event)
            print("=============")
            print(chosen_template.dependent_nodes)
            print("=============")
            response = chosen_template.fill_blanks(self.curr_event)

        # if response type is not a string (as in, pag template/list siya), join stuff idk
        if type(response) is not type("dump"):
            print(response)
            str_response = ' '.join(response)
            # TODO replace multiple occurences of spaces with only one space.
        else:
            str_response = response
        print("RESPONSE IS: ", str_response)

        self.reset_state()
        return str_response, chosen_template

    def choose_template(self):
        print("templates:")
        print(self.usable_template_list)
        
        if (len(self.usable_template_list) > 0):
            return np.random.choice(self.usable_template_list)
        else:
            # return empty list lang? di ko sure if tama :(
            return self.usable_template_list



