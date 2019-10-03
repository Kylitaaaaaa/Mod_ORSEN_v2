from src import *


class World:
    # The different object entities in the world
    objects = [] #Object object

    # The different character entities
    characters = []

    # The setting involved.
    settings = []

    # The sequence of events used to store the event frames
    event_chains = []

    # The temporary event chain that contains the events from the last dialogue entered by the user.
    curr_event = []

    # The previous sentences used to build the event chains
    sentence_references = []

    def __init__(self, objects=[], characters=[], settings=[], event_chains=[], sentence_references=[], dialogue_move_history=[]):
        print("IM AT WORLD")
        self.objects = objects
        self.characters = characters
        self.settings = settings
        self.event_chains = event_chains
        self.sentence_references = sentence_references
        self.dialogue_move_history = dialogue_move_history

    def add_event(self, event, sentence):
        event.sequence_number = len(self.event_chains) + 1

        self.event_chains.append(event)
        self.sentence_references.append(sentence)

        self.curr_event = event

    def add_character(self, character):
        self.characters.append(character)

    def get_character(self, character_name):
        for c in self.characters:
            if c.name == character_name:
                return c
