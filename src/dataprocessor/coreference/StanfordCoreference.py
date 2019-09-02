# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 12:27:17 2019

@author: Wisner
"""
from . import Coreference

from pycorenlp import StanfordCoreNLP

class StanfordCoreference(Coreference):
    
    def __init__(self):
        super().__init__()
        try:
            print("Connecting")
            self.scn = StanfordCoreNLP('http://localhost:9000')
            print("Connected")
        except:
            print("Connection to Stanford Core NLP at localhost port 9000 is blocked")

        
    def resolve(self, story):
        story = story.replace('“', '"')
        story = story.replace('”', '"')
        corenlp_output= self.scn.annotate(story, properties= {'annotators':'dcoref','outputFormat':'json','ner.useSUTime':'false'})

        """ Transfer the word form of the antecedent to its associated pronominal anaphor(s) """
    #     print(corenlp_output)
        for coref in corenlp_output['corefs']:
            mentions = corenlp_output['corefs'][coref]
            antecedent = mentions[0]  # the antecedent is the first mention in the coreference chain
            for j in range(1, len(mentions)):
                mention = mentions[j]
                if mention['type'] == 'PRONOMINAL':
                    # get the attributes of the target mention in the corresponding sentence
                    target_sentence = mention['sentNum']
                    target_token = mention['startIndex'] - 1
                    # transfer the antecedent's word form to the appropriate token in the sentence
                    corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']
                    
        return self.output_resolved(corenlp_output)
    
    
    def output_resolved(self, corenlp_output):
        """ Print the "resolved" output """
        possessives = ['hers', 'his', 'their', 'theirs']
        output = ""
        for sentence in corenlp_output['sentences']:
            for token in sentence['tokens']:
                output_word = token['word']
                # check lemmas as well as tags for possessive pronouns in case of tagging errors
                if token['lemma'] in possessives or token['pos'] == 'PRP$':
                    output_word += "'s"  # add the possessive morpheme
                output_word += token['after']
    #             print(output_word)
                output += output_word
                
    #     print("Final:", output)
        return output


# text = "Tom and Jane are good friends. They are cool. He knows a lot of things and so does she. His car is red, but hers is blue. It is older than hers. The big cat ate its dinner."
print("Connecting")
scn = StanfordCoreNLP('http://localhost:9000')
print("Connected")

#for i in tnrange(len(file_names)):
#    resolve_and_download(scn, REPOSITORY_PROCESSED_STORIES[GRIMM_FAIRY_TALES], REPOSITORY_RESOLVED_STORIES[GRIMM_FAIRY_TALES], file_names[i])    