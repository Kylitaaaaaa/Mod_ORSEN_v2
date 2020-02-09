from src import *
from src import Logger


class World:
    # The different object entities in the world
    objects = []  # Object object

    # The different character entities
    characters = []

    # The setting involved.
    settings = []

    # The sequence of events used to store the event frames
    event_chains = []

    # List of emotional events
    emotion_events = []

    # The temporary event that contains the last event from the last dialogue entered by the user.
    curr_event = []  # I changed this from curr_event = None

    #EDEN: Temporary event with emotions
    curr_emotion_event = None

    # The temporary event chain that contains the events from the last dialogue entered by the user
    last_fetched = []

    # The previous sentences used to build the event chains
    sentence_references = []

    def __init__(self, objects=[], characters=[], settings=[], event_chains=[], sentence_references=[],
                 dialogue_move_history=[], emotion_events = []):
        print("IM AT WORLD")
        self.objects = objects
        self.characters = characters
        self.settings = settings
        self.event_chains = event_chains
        self.sentence_references = sentence_references
        self.dialogue_move_history = dialogue_move_history
        self.curr_event = []
        self.curr_emotion_event = None
        self.last_fetched = []
        self.emotion_events = []

    def reset_world(self):
        self.objects = []
        self.characters = []
        self.settings = []
        self.event_chains = []
        self.sentence_references = []
        self.dialogue_move_history = []
        self.curr_event = []
        self.curr_emotion_event = None
        self.last_fetched = []
        self.emotion_events = []

    def add_event(self, event, sentence):
        event.sequence_number = len(self.event_chains) + 1

        self.event_chains.append(event)
        self.sentence_references.append(sentence)

        self.curr_event = event

    def add_emotion_event(self, event):
        self.emotion_events.append(event)
        # self.emotion_events.extend(event)

        self.curr_emotion_event = event


    def add_character(self, character):
        self.characters.append(character)

    def get_character(self, character_name):
        for c in self.characters:
            if c.name == character_name:
                return c
        return None

    def add_object(self, object):
        self.objects.append(object)

    def get_object(self, object_name):
        for o in self.objects:
            if o.name == object_name:
                return o
        return None

    def remove_object(self, object):

        return self.objects.remove(object)

    def add_setting(self, setting):
        self.settings.append(setting)

    def get_num_action_events(self):
        count = 0
        for X in self.event_chains:
            if X.type == EVENT_ACTION:
                count = count + 1
        return count

    def get_pickled_world(self):
        pickled_world = []

        #pickle objects
        pickled_objects = []
        try:
            for X in self.objects:
                pickled_objects.append(X.get_pickled_object())
        except Exception as e:
            Logger.log_conversation("ERROR: " + str(e))

        # pickle characters
        pickled_characters = []
        try:
            for X in self.characters:
                pickled_characters.append(X.get_pickled_character())
        except Exception as e:
            Logger.log_conversation("ERROR: " + str(e))

        # pickle setting
        pickled_settings = []
        try:
            for X in self.settings:
                pickled_settings.append(X.get_pickled_setting())
        except Exception as e:
            Logger.log_conversation("ERROR: " + str(e))

        # pickle event
        pickled_event_chain = []
        try:
            for X in self.event_chains:
                pickled_event_chain.append(X.get_pickled_event())
        except Exception as e:
            Logger.log_conversation("ERROR: " + str(e))

        # pickle emotion event
        pickled_emotion_event = []
        try:
            for X in self.emotion_events:
                pickled_emotion_event.append(X.get_pickled_emotion_event())
        except Exception as e:
            Logger.log_conversation("ERROR: " + str(e))

        pickled_world.append(pickled_objects)
        pickled_world.append(pickled_characters)
        pickled_world.append(pickled_settings)
        pickled_world.append(pickled_event_chain)
        pickled_world.append(pickled_emotion_event)
        return pickled_world


    def __str__(self):
        my_string = "" \
                    "============================\n" \
                    "= WORLD \t============\n" \
                    "============================\n\n" \
                    "============== OBJECTS ==============\n"


        # objects
        for object in self.objects:
            my_string = my_string + str(object)

        return my_string.strip()



