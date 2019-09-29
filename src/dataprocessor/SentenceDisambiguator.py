# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 05:48:18 2019

@author: Wisner
"""
from src.constants import *

import numpy as np

class SentenceDisambiguator(object):
    
    def __init__(self, annotator):
        self.annotator = annotator
        
            
    def get_loc(self, line, char):
        try:
            return line.find(char)
        except:
            return -1
    
    def split_quotes(self, line):
    #    print("Traversing %s" % (line))
        line = line.strip()
        quotes_len = len(OPENING_QUOTES)
        
        if OPENING_QUOTES in line or CLOSING_QUOTES in line:
            
            opening = self.get_loc(line, OPENING_QUOTES)
            closing = self.get_loc(line, CLOSING_QUOTES)
            loc = np.array([opening, closing])
            loc = loc[loc > -1]
            
            split_loc = loc.min()
            
            before = line[0:split_loc]
            mid = line[split_loc:split_loc+quotes_len]
            after = line[split_loc+ quotes_len: len(line)]
            
    #        print("\t%s" % before)
    #        print("\t%s" % mid)
    #        
    #        print("going back")
            
            append_list = []
            if before.strip():
                append_list.append(before)
            append_list.append(mid)
            
            return append_list + (self.split_quotes(after))
        else:
    #        print("\t%s" % line)
    #        print("start of going back")
            if line.strip():
                return [line]
            return []
        
    def split(self):
        doc = self.annotator.get_annotated()
        
        splits = []
        for s in doc.sents:
            splits.extend(self.split_quotes(s.text))    
        
        return splits;
