from src.dataprocessor import Annotator
from src.dataprocessor.coreference import SpacyCoreference

import spacy
nlp = spacy.load('en_core_web_sm')

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

    def perform_input_decoding(self, text):
        print("---------Perform Input Decoding---------")
        #categorization


        #coreference resolving thru spacy
        # Winfred's code
        referenced_text = InputDecoder.coref_resolve(self, text)
        print("Coreferenced Text: ", referenced_text)

        #dependency parsing thru spacy
        # https://spacy.io/usage/linguistic-features
        parsed_doc = nlp(referenced_text)
        print("Parsed: ", parsed_doc)

        #named entity recognition
        print("Named Entities")
        # for X in parsed_doc.ents:

        print([(X.text, X.label_) for X in parsed_doc.ents])
        print("---------Done with Input Decoding---------")

    def get_named_entities(self, dec):
        # named_entities = []
        # for X in doc.ents:
        return None


    def coref_resolve(self, raw_text):
        self.annotator.annotate(raw_text)
        crf = SpacyCoreference(self.annotator)
        resolved = crf.resolve()
        print("Printing resolved text")
        print(resolved.text)
        return resolved._.coref_resolved


    def decode(text, current_world):
        if text == "Hello!":
            pass
        else:
            text = InputDecoder.coref_resolve(text)

        return text







