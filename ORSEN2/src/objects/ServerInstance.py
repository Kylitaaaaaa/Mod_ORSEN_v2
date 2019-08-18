from src.objects.storyworld.World import World


class ServerInstance(object):
    class __ServerInstance:

        def __init__(self):
            self.worlds = {}

        def __str__(self):
            return repr(self)

        def new_world(self, new_id):
            if self.worlds.get(new_id) is None:
                self.worlds[new_id] = World(new_id)
                return True
            else:
                return False

        def add_world(self, world):
            if self.worlds.get(world.id) is None:
                self.worlds[world.id] = world
                return True
            else:
                return False

        def get_world(self, id):
            return self.worlds.get(id)

    instance = None

    def __init__(self):
        if not ServerInstance.instance:
            ServerInstance.instance = ServerInstance.__ServerInstance()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __new__(cls):  # __new__ always a classmethod
        if not ServerInstance.instance:
            ServerInstance.instance = ServerInstance.__ServerInstance()
        return ServerInstance.instance
