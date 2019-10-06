from src.models.user import User


class UserHandler:
    __instance = None

    @staticmethod
    def get_instance():
        if UserHandler.__instance == None:
            UserHandler()
        return UserHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if UserHandler.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            UserHandler.__instance = self
            self.curr_user = User(id=-1,
                                  name="???",
                                  code="???")

    def set_global_curr_user(self, user):
        self.curr_user = user
