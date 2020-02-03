# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 05:52:05 2019

@author: Wisner
"""
from src.constants import *

import spacy
import neuralcoref
from spacy.tokens import Token

class Annotator(object):
    def __init__(self, model_to_use = "en_core_web_sm"):
        print("Last compatibility version check: %s.\n" % (LAST_CHECK_DATE))
                
        print("Checking spaCy version: %s" % (spacy.__version__))
        if spacy.__version__ != SPACY_VERSION:
            raise ImportError("spaCy version %s is required for this project to work properly. Details: As of the creation of this system, the latest release, 2.1.4, throws a binary incompatibility with HuggingFace/Neuralcoref. See more at https://github.com/huggingface/neuralcoref/issues/158" % (SPACY_VERSION))   
                
        print("Checking neuralcoref version: %s" % (neuralcoref.__version__))
        if neuralcoref.__version__ != NEURALCOREF_VERSION:
            raise ImportError("This project has worked with version %s. For compatibility reasons, better use this version instead of other versions." % (NEURALCOREF_VERSION))   
                
        print("Loading model %s." % (model_to_use))
        self.nlp = spacy.load(model_to_use)
                
        print("Loading neuralcoref pipe to model.")
        neuralcoref.add_to_pipe(self.nlp, 
            greedyness = 0.50,
            max_dist = 50, 
            blacklist = True)
        
        print("Done initializing coreference resolution module.")

        try:
            Token.set_extension("is_traversed", default=False)

        except ValueError:
            print("Field is_traversed is already existing on Token type")

        
    def annotate(self, content):
        self.content = content
        self.doc = self.nlp(content)
    
    def get_annotated(self):
        return self.doc
        
