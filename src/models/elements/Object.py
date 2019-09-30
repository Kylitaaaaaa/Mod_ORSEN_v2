class Object:

    def __init__(self, id="", name="", type="", attribute=[], in_setting="", mention_count=0):
        self.id = id
        self.name = name
        self.type = type
        self.attribute = attribute
        self.in_setting = in_setting
        self.mention_count = mention_count

    def __str__(self):
        return self.name + ' (' + self.id + ')'