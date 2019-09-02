# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 01:36:52 2019

@author: Wisner
"""
from . import Coreference

class SpacyCoreference(Coreference):
    
    def __init__(self, annotator):
        super().__init__()
        self.annotator = annotator

    def resolve(self):
        doc = self.annotator.get_annotated()
#        doc._.coref_resolved
        return doc;

