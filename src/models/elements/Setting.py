class Setting:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return self.type + ": " + self.value