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
        print("TESTING")

        print("---------Perform Input Decoding---------")
        #categorization ###probs add intents here TODO


        #coreference resolving thru spacy
        print("*Starting Coreferencing*")
        # Winfred's code
        referenced_text = InputDecoder.coref_resolve(self, text)
        print(referenced_text)
        print("*Done Coreferencing* \n")

        #dependency parsing thru spacy
        # https://spacy.io/usage/linguistic-features
        print("*Starting Dependency Parsing*")
        parsed_doc = nlp(referenced_text)
        print(parsed_doc)
        print("*Done Dependency Parsing* \n")

        #named entity recognition
        print("*Starting Entity Recognition*")
        named_entities = InputDecoder.get_named_entities(self, parsed_doc)
        print(named_entities)
        print("*Done With Entity Recognition* \n")

        print("---------Done with Input Decoding---------")

    def get_named_entities(self, doc):
        named_entities = []
        for X in doc.ents:
            named_entities.append(X)
            # print(X.text, X.label_)
            # named_entities.push(X.text, X.label_)

        return named_entities


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

        return text







