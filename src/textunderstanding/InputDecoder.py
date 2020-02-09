from nltk import Tree

from src.dataprocessor import Annotator
from src.dataprocessor.coreference import SpacyCoreference
from src import Logger

import spacy
# I changed it to sm for testing only
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


    def __get_named_entities(self, doc):
        named_entities = []
        for ent in doc.ents:
            named_entities.append(ent)

        return named_entities

    def __get_noun_chunks(self, doc):
        chunk_list = []
        for chunk in doc.noun_chunks:
            chunk_list.append(chunk)
        return chunk_list


    def coref_resolve(self, raw_text):
        self.annotator.annotate(raw_text)
        crf = SpacyCoreference(self.annotator)
        resolved = crf.resolve()
        return resolved._.coref_resolved


    # def perform_input_decoding(self, text, current_world=None):
    #     print("---------Perform Input Decoding---------")
    #     #categorization ###probs add intents here TODO
    #
    #     """ COREFERENCE RESOLUTION """
    #     Logger.log_information_extraction('Starting coreference resolution')
    #     # TODO: context checking (as in, get the previous inputs (from user) and outputs (from ORSEN) to use as
    #     #  context for the resolution of the text.
    #     # if len(world.content) == 0:
    #     #   resolved = InputDecoder.get_instance().coref_resolve()
    #     # else:
    #     resolved = self.coref_resolve(text)
    #     print(resolved)
    #     Logger.log_information_extraction('Done with coreference resolution')
    #
    #
    #     self.annotator.annotate(resolved)
    #     doc = self.annotator.get_annotated()
    #
    #
    #     """ NAMED ENTITY RECOGNITION """
    #     Logger.log_information_extraction('Starting NER parsing')
    #     named_entities = self.__get_named_entities(doc)
    #     print(named_entities)
    #     Logger.log_information_extraction('Done with NER parsing')
    #
    #     """ NOUN CHUNKS """
    #     Logger.log_information_extraction('Starting noun chunk extraction')
    #     noun_chunks = self.__get_noun_chunks(doc)
    #
    #     """ SENTENCE DISAMBIGUATION """
    #     for sent in doc.sents:
    #
    #         """ DEPENDENCY PARSING """
    #         # https://spacy.io/usage/linguistic-features
    #         Logger.log_information_extraction('Starting dependency parsing ')
    #         self.extract_details(sent, current_world)
    #
    #         Logger.log_information_extraction('Done dependency parsing')
    #
    #     print("---------Done with Input Decoding---------")


    def extract_details(self, sent, world, subj="", neg="", text=""):
        subject= subj
        direct_object = ""
        dative = ""

        curr_index = -1
        token_list = list(sent)
        for i in range(len(token_list)):
            curr_token = token_list[i]
            print(curr_token)


    def decode(self, text, current_world):
        if text == "Hello!":
            pass
        else:
            text = self.coref_resolve(text)

        return text

    def to_nltk_tree(self, node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(node.orth_, [self.to_nltk_tree(child) for child in node.children])
        else:
            return node.orth_

    def display_tokens(self, sentence):
        print("TEXT\tPoS\tTag\tStop?\tDep\tDep-Meaning")
        for token in sentence:
            print(token.text, "\t",
                  token.pos_, "\t",
                  token.tag_, "\t",
                  token.is_stop, "\t",
                  #                      token.ent_type_, "\t",
                  token.dep_, "\t",
                  spacy.explain(token.dep_), "\t",
                  # token.head.text, "\t",
                  # token.head.pos_, "\t",
                  #   [child for child in token.children]
                  )
        self.to_nltk_tree(sentence.root).pretty_print()



