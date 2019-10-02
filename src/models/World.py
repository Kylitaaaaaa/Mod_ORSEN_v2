class World:
    # The different object entities in the world
    objects = [] #Object object
    dialogue_move_history = [] #Move history -- number of times each dialogue has been used

    # The different character entities
    characters = []

    # The setting involved.
    settings = []

    # The sequence of events used to store the event frames
    event_chains = []

    curr_event_chain = []

    # The previous sentences used to build the event chains
    sentence_references = []

    def __init__(self, objects=[], characters=[], settings=[], event_chains=[], sentence_references=[], dialogue_move_history=[]):
        self.objects = objects
        self.characters = characters
        self.settings = settings
        self.event_chains = event_chains
        self.sentence_references = sentence_references
        self.dialogue_move_history = dialogue_move_history

    def add_event(self, event, sentence):
        self.event_chains.append(event)
        self.sentence_references.append(event)

    def add_character(self, character):
        self.characters.append(character)

    def get_character(self, character_name):
        for c in self.characters:
            if c.name == character_name:
                return c
