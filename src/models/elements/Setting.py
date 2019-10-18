from src.models.pickles.PickleObject import PickleObject


class Setting:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return self.type + ": " + self.value

    def get_pickled_setting(self):
        pickled_setting = PickleObject()
        pickled_setting.type = str(self.type)
        pickled_setting.value = str(self.value)
        return pickled_setting