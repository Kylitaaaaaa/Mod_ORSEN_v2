class StoryInstance:

    id = -1

    eventchain = []

    object_list = []
    relationship_list = []
    setting = None

    def __init__(self, id):
        self.id = id;

    def add_object(self, object):
        self.object_list.append(object)

    def add_relationship(self, relationship):
        self.relationship_list.append(relationship)

    def set_setting(self, setting):
        self.setting = setting