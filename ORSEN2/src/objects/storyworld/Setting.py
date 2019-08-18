class Setting:
    id = ""
    name = ""
    type = ""

    def __init__(self, id="", name="", type=""):
        self.id   = id
        self.name = name
        self.type = type

    def __str__(self):
        return "SETTING ID: %s \n\tName: %s \n\tType: %s\n" % (str(self.id), self.name, self.type)
