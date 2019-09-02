class Object:
    name = ""
    type = ""
    attribute = [] #Attribute object
    in_setting = ""
    mentioned = ""

    def __init__(self, name, type, attribute, in_setting, mentioned):
        self.name = name
        self.type = type
        self.attribute = attribute
        self.inSetting = in_setting
        self.mentioned = mentioned

    def __str__(self):
        return str(self.id) + " " + self.name