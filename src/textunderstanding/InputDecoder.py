from src.dataprocessor import Annotator
from src.dataprocessor.coreference import SpacyCoreference

class InputDecoder:
    __instance = None

    @staticmethod
    def get_instance():
        if InputDecoder.__instance == None:
            InputDecoder()
        return InputDecoder.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if InputDecoder.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            InputDecoder.__instance = self
            self.annotator = Annotator()


    def coref_resolve(self, raw_text):
        self.annotator.annotate(raw_text)
        crf = SpacyCoreference(self.annotator)
        resolved = crf.resolve()
        return resolved._.coref_resolved


    def decode(text, current_world):
        if text == "Hello!":
            pass
        else:
            text = InputDecoder.coref_resolve(text)



