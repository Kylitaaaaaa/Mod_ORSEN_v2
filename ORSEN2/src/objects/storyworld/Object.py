class Object:

    id = ""
    name = ""
    type = []
    inSetting = {}
    timesMentioned = 0
    attributes = []

    def __init__(self, id="", name="", type=[], inSetting=0, times=1, attr=[]):
        self.id   = id
        self.name       = name
        self.type       = type
        self.inSetting  = inSetting
        self.timesMentioned = times
        self.attributes = attr

    def __str__(self):
        return "OBJECT ID \"%s\": \n\tName: %s \n\tType: %s \n\tSetting: %s \n\tmentioned: %s\n" \
               % (str(self.id), self.name, self.type, self.inSetting, str(self.timesMentioned))\
               + "\tattributes: " + str(self.attributes)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
