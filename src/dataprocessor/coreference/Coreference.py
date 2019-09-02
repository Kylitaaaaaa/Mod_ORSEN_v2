# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 12:27:58 2019

@author: Wisner
"""
import abc
from abc import ABC, abstractmethod


class Coreference(ABC):
    __metaclass__ = abc.ABCMeta
    
    def __init___(self):
        super().__init__()      
        

    @abstractmethod
    def resolve(self):
        pass  