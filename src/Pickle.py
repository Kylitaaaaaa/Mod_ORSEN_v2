import datetime
import pickle
import self
import numpy as np

class Pickle:

    def __init__(self):
        # self.pickle_filepath = '../logs/user world/'
        # self.filename = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        pass



    @staticmethod
    def pickle_world_wb(pickle_filepath, world):
        with open(pickle_filepath, 'wb') as f:
            pickle.dump(world, f)
            f.close()

    @staticmethod
    def pickle_world_rb(pickle_filepath):
        new_dict = None
        with open(pickle_filepath, 'rb') as f:
            new_dict = pickle.load(f)
            f.close()
        print(new_dict)
        return new_dict


