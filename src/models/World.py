class Object:
    objects = [] #Object object
    characters = [] #Character object
    settings = [] #Setting object
    event_chains = [] #Event object

    def __init__(self, objects, characters, settings, event_chains):
        self.objects = objects
        self.characters = characters
        self.settings = settings
        self.event_chains = event_chains