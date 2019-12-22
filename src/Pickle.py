import datetime
import pickle
# import self
import numpy as np



class Pickle:

    def __init__(self):
        # self.pickle_filepath = '../logs/user world/'
        # self.filename = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        pass



    @staticmethod
    def pickle_world_wb(pickle_filepath, world):
        to_pickle = []

        try:
            new_dict = None
            with open(pickle_filepath, 'rb') as f:
                new_dict = pickle.load(f)
                f.close()
        except Exception as e:
            new_dict = None
            print("Error in reading pickle file: ", str(e))

            if new_dict is not None:
                to_pickle = new_dict

            to_pickle.append(world)

        try:
            with open(pickle_filepath, 'wb') as f:
                pickle.dump(to_pickle, f)
                f.close()
        except Exception as e:
            print("Error in writing pickle file:  ", str(e))

    @staticmethod
    def pickle_world_rb(pickle_filepath):
        try:
            new_dict = None
            with open(pickle_filepath, 'rb') as f:
                new_dict = pickle.load(f)
                f.close()
            print(new_dict)
            return new_dict
        except:
          print("Something went wrong when reading to the file")
        finally:
          return None


