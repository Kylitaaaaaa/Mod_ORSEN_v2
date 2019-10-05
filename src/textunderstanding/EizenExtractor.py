# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 04:20:35 2019

@author: Wisner
"""

import spacy
from nltk import Tree

from src.constants import *
from src.dbo.extraction import DBOExtractionTemplate
from src.models.events import ActionEvent
from src.models.nlp import ExtractionTemplate
from src.models.nlp.Relation import Relation
from src.textunderstanding import InputDecoder


class State:
    def __init__(self, sentence):
        self.voice = self.identify_sentence_voice(sentence)

    def identify_sentence_voice(self, sentence):
        for token in sentence:
            if token.dep_ == "nsubjpass":
                return VOICE_PASSIVE
        return VOICE_ACTIVE


class ExtractorState:
    def __init__(self):
        self.subordinate = False


class EizenExtractor(object):
    MODE_LISTING = "list"
    MODE_CONCATENATING = "concatenate"

    def __init__(self, model_to_use="en_core_web_lg"):
        print("Last compatibility version check: %s.\n" % (LAST_CHECK_DATE))

        print("Checking spaCy version: %s" % (spacy.__version__))
        if spacy.__version__ != SPACY_VERSION:
            raise ImportError(
                "spaCy version %s is required for this project to work properly. Details: As of the creation of this system, the latest release, 2.1.4, throws a binary incompatibility with HuggingFace/Neuralcoref. See more at https://github.com/huggingface/neuralcoref/issues/158" % (
                    SPACY_VERSION))

        print("Loading model %s." % (model_to_use))
        self.nlp = spacy.load(model_to_use)
        self.extractor_flags = ExtractorState()

    def split_on_newlines(self, doc):
        for token in doc[:-1]:
            if token.text == "\n":
                doc[token.i + 1].is_sent_start = True
        return doc

    """Check verb type given spacy token. Unused"""
    def check_token(self, token):
        if token.pos_ == 'VERB':
            indirect_object = False
            direct_object = False
            for item in token.children:
                if (item.dep_ == "iobj" or item.dep_ == "pobj"):
                    indirect_object = True
                if (item.dep_ == "dobj" or item.dep_ == "dative"):
                    direct_object = True
            if indirect_object and direct_object:
                return 'DITRANVERB'
            elif direct_object and not indirect_object:
                return 'TRANVERB'
            elif not direct_object and not indirect_object:
                return 'INTRANVERB'
            else:
                return 'VERB'
        else:
            return token.pos_

    """
    Did you really expect an explanation for this?

    EDIT: 
    Actually, I DO need to explain this. There are 3 general types of verbs: ACTION, LINKING, AND HELPING. 

    ACTION
    - Can be subdivided into TRANSITIVE AND INTRANSITIVE VERB
    LINKING
    - Connects a subject to a noun or an adjective
    HELPING
    - Used before ACTION VERBS or LINKING VERBS
    - Generally, I've been seeing 23 instances of these HELPING VERBS
        - link 1: https://www.visualthesaurus.com/cm/dictionary/the-forgotten-helping-verbs/
        - link 2: http://www.softschools.com/language_arts/grammar/helping_verbs/list/
    """
    def is_action_verb(self, token):
        if token.pos_ == "VERB":
            if "aux" in token.dep_ or token.text in HELPING_VERBS:
                return False
            return True
        return False

    """Retrieves the ACTION component of the story"""

    def get_action_verbs(self, sentence):

        action_verbs = []
        for token in sentence:
            # print(token.text)
            if self.is_action_verb(token):
                #            print(token, token.dep_, [child for child in token.children])
                action_verbs.append(token)
        return action_verbs

    def is_future_subordinate_clause(self, action_token):
        for child in action_token.children:
            if child.pos_ == 'ADP' and child.tag_ == 'IN' and child.dep_ == "mark":
                if child.text.lower() == 'if' or child.text.lower() == 'when':
                    return True

        if action_token.dep_ != "ROOT":
            return self.is_future_subordinate_clause(action_token.head)
        else:
            return False

    """Check if the action event given is a part of the subordinate clause by checking for a subordinate conjunction"""
    """If <something> then <another thing> --> something IS REMOVED since it only provides context"""
    """Read more at https://www.grammarly.com/blog/subordinating-conjunctions/"""

    def is_subordinate_clause(self, action_token):
        for child in action_token.children:
            if child.pos_ == 'ADP' and child.tag_ == 'IN' and child.dep_ == "mark":
                return True

        if action_token.dep_ != "ROOT":
            return self.is_subordinate_clause(action_token.head)
        else:
            return False

    """Check if the dependent clause is simply a relative clause, or a clause with the main task of providing more context"""
    """The young shepherd who wished to marry has acquainted the three sisters --> who wished to marry is removed since it only provides context"""
    """Read more at https://www.toppr.com/guides/english/pronoun/relative-pronoun/"""

    def is_relative_clause(self, action_token):
        if 'VB' in action_token.tag_:
            if action_token.dep_ == "relcl":
                # print("\tFor action", action_token.text)
                for child in action_token.children:
                    if child.text.lower() in RELATIVE_PRONOUNS:
                        # print(child.text.lower(), "caused this!!")
                        return True
                if action_token.dep_ != "ROOT":
                    # print("Climbing to", action_token.head)
                    return self.is_relative_clause(action_token.head)
        else:
            if action_token.dep_ != "ROOT":
                # print("Climbing to", action_token.head)
                return self.is_relative_clause(action_token.head)
            else:
                # print("Returning to False")
                return False

    """Checks if a given action is negated via the dependency 'neg' (or negation modifer)"""

    def is_negated(self, action):
        for child in action.children:
            if child.dep_ == 'neg':
                return True
        return False

    """Given a noun, replace it with the full noun chunk (e.g. instead of getting only Potter, also get the preceeding name 'Harry'"""

    def convert_noun_to_noun_chunks(self, noun_chunks, subjects):
        # print("NOUN CHUNK: %s" % (noun_chunks))
        # print("SUBJECTS  : %s" % (subjects))

        for j in range(len(subjects)):
            # print("READING %s" % subjects[j])
            # print(subjects[j])

            try:
                subject_index = subjects[j].i
            except:
                subject_index = subjects[j].start

            for noun_chunk in noun_chunks:
                if noun_chunk.start <= subject_index <= noun_chunk.end:
                    # print("Changed %s to %s!" % ([j], noun_chunk))
                    subjects[j] = noun_chunk

        return subjects

    """Retrieves a token that qualifies in the required POS tag and dependency tag. Connectors are traversed since they are simply connectors."""

    def retrieve_tokens(self, pos_tags, dependencies, token, excluded_tags=[], additional_connecting_tags=[], mode=MODE_LISTING):
        connectors = ["cc", "det", "punct", "agent", "prep"]
        connectors.extend(additional_connecting_tags)
        # print("FINAL RESULING CONNECTIONS:", connectors)
        if mode == self.MODE_CONCATENATING:
            tokens = ""
        elif mode == self.MODE_LISTING:
            tokens = []

        for child in token.children:
            #        print("  child:", child.text)
            if child._.is_traversed == True:
                break

            if child.dep_ in dependencies and child.pos_ in pos_tags:
                if child.tag_ == 'WP' and 'WP' in excluded_tags:
                    if mode == self.MODE_CONCATENATING:
                        tokens = tokens + ' ' + token.head.text
                    elif mode == self.MODE_LISTING:
                        tokens.append(token.head)

                    child._.is_traversed = True
                    tokens = tokens + self.retrieve_tokens(pos_tags, dependencies, token.head, excluded_tags, additional_connecting_tags, mode)
                else:
                    if mode == self.MODE_CONCATENATING:
                        tokens = tokens + ' ' + child.text
                    elif mode == self.MODE_LISTING:
                        tokens.append(child)

                    child._.is_traversed = True
                    tokens = tokens + self.retrieve_tokens(pos_tags, dependencies, child, excluded_tags, additional_connecting_tags, mode)

            elif child.dep_ in connectors:
                if mode == self.MODE_CONCATENATING:
                    tokens = tokens + ' |' + child.text

                #            print("\ttraversing '%s'(child of %s)" % (child.text, token.text))
                child._.is_traversed = True
                tokens = tokens + self.retrieve_tokens(pos_tags, dependencies, child, excluded_tags, additional_connecting_tags, mode)

        #    print("RETURNING:", tokens)
        return tokens

    """Retrieves the ACTOR associated with an action"""

    def get_actors(self, action, sentence_state):
        nsubj = []
        if sentence_state.voice == VOICE_ACTIVE:
            nsubj = self.retrieve_tokens(pos_tags=["NOUN", "PROPN", "ADP", "PRON", "ADJ"],
                                         dependencies=["nsubj", "conj"],
                                         token=action,
                                         excluded_tags=['WP'])
        elif sentence_state.voice == VOICE_PASSIVE:
            nsubj = self.retrieve_tokens(pos_tags=["NOUN", "PROPN", "ADP", "PRON", "ADJ"],
                                         dependencies=["pobj", "conj"],
                                         token=action)
        #    print("All actors of action", action, ":", nsubj)
        return nsubj

    """Retrieves the direct OBJECT associated with a given action"""
    def get_objects(self, action, sentence_state):
        dobj = []
        if sentence_state.voice == VOICE_ACTIVE:
            #        print("\nSEARCH FOR ACTION", action, "START!\n")
            dobj = self.retrieve_tokens(pos_tags=["NOUN", "PROPN", "ADP"],
                                        dependencies=["dobj", "conj"],
                                        token=action)
        elif sentence_state.voice == VOICE_PASSIVE:
            #        print("\nSEARCH FOR ACTION", action, "START!\n")
            dobj = self.retrieve_tokens(pos_tags=["NOUN", "PROPN", "ADP"],
                                        dependencies=["nsubjpass", "conj"],
                                        token=action)
            #        print("\nSEARCH FOR ACTION", action, "END!\n")
        #    print("All direct objects for action", action, ":", dobj)
        return dobj

    """Retrieves the adverbs associated with a given action (specifically, adverb of manner)"""
    def get_adverbs(self, action, sentence_state):
        adv = self.retrieve_tokens(pos_tags=['ADV'],
                                   dependencies=['advmod'],
                                   token=action)

        # print("Adverbs found: ", adv)
        return adv

    def get_preposition(self, action, sentence_state):
        prep = self.retrieve_tokens(pos_tags=['ADP', 'NOUN'],
                                    dependencies=['prep'],
                                    token=action,
                                    additional_connecting_tags=['pobj'],
                                    mode=self.MODE_CONCATENATING)
        split = prep.split(" ")
        while "|" in split[0]:
            split.pop(0)
        while "|" in split[len(split)-1]:
            split.pop(len(split)-1)

        new_prep = ' '.join(split)
        new_prep = new_prep.replace('|', '')

        return new_prep.strip()

    def get_object_of_preposition(self, action, sentence_state, preposition):
        obj_prep = self.retrieve_tokens(pos_tags=['ADP', 'NOUN'],
                                    dependencies=['pobj', 'prep'],
                                    token=action,
                                    mode=self.MODE_CONCATENATING)

        obj_prep = obj_prep.replace(preposition, '')

        split = obj_prep.split(" ")
        while "|" in split[0]:
            split.pop(0)
        while "|" in split[len(split)-1]:
            split.pop(len(split)-1)

        new_obj_prep = ' '.join(split)
        new_obj_prep = new_obj_prep.replace('|', '')

        return new_obj_prep.strip()

    def guess_event_type(self, sentence):
        for token in sentence:
            if token.dep_ == 'expl':
                return EVENT_CREATION

        if len(self.get_action_verbs(sentence)):
            return EVENT_ACTION

        return EVENT_DESCRIPTION

    def extract_event_aao(self, sentence):
        events = []
        #        subjects = [chunk for chunk in sentence.noun_chunks if 'nsubj' in chunk.root.dep_ and chunk.root.ent_type_ == 'PERSON']
        subjects = [chunk for chunk in sentence.noun_chunks]
        # print("Noun chunks:", subjects)

        # for subject in subjects:
        # print(subject.text, subject.start, subject.end)

        sentence_state = State(sentence)
        # print("Voice: %s" % (sentence_state.voice))
        actions = self.get_action_verbs(sentence)
        # print("Actions:", actions)

        actors_state = []

        start = 0
        end = 0

        # print("VOICE PATTERN: %s" % (sentence_state.voice))
        if sentence_state.voice == VOICE_ACTIVE:
            start = 0
            end = len(actions)
            factor = 1
        elif sentence_state.voice == VOICE_PASSIVE:
            # """START THE EXTRACTION IN REVERSE IF PASSIVE VOICE"""
            start = len(actions) - 1
            end = -1
            factor = -1

        # print("all actions:", actions)

        unspliced_events = []
        for i in range(start, end, factor):
            event_action = actions[i]

            event_actors = self.get_actors(event_action, sentence_state)
            # print("Actors: ", event_actors)
            for token in sentence:
                token._.is_traversed = False

            event_objects = self.get_objects(event_action, sentence_state)
            # event_objects = self.convert_noun_to_noun_chunks(subjects, event_objects)
            for token in sentence:
                token._.is_traversed = False

            event_adverbs = self.get_adverbs(event_action, sentence_state)
            for token in sentence:
                token._.is_traversed = False

            event_prepositions = self.get_preposition(event_action, sentence_state)
            for token in sentence:
                token._.is_traversed = False

            event_obj_prepositions = self.get_object_of_preposition(event_action, sentence_state, event_prepositions)
            for token in sentence:
                token._.is_traversed = False



            if not event_actors:
                event_actors = actors_state
                event_actors = self.convert_noun_to_noun_chunks(subjects, event_actors)
            else:
                # print()
                actors_state = event_actors

            event = [event_actors, event_action, event_objects, event_adverbs, event_prepositions, event_obj_prepositions]
            print("RESULT:", event)
            unspliced_events.append(event)

        if sentence_state.voice == VOICE_PASSIVE:
            unspliced_events.reverse()

        pre_partial = []
        for unspliced_event in unspliced_events:
            event_actors = unspliced_event[ACTOR]
            for a in event_actors:
                event = [a] + unspliced_event[ACTION:]
                pre_partial.append(event)
        # print(partial)

        print("PREPARTIAL IS", pre_partial)
        partial = pre_partial

        for event in partial:
            event_objects = event[DIRECT_OBJECT]

            if len(event_objects) > 0:
                for o in event_objects:
                    event = event[:ACTION + 1] + [o] + event[ADVERB:]
                    print('NEW EVENT TO GO IN: ', event)
                    events.append(event)
            else:
                event = event[:ACTION + 1] + [None] + event[ADVERB:]
                events.append(event)

        print("FINAL EVENT LISTING IS:")
        for e in events:
            print(e)
        return events

    def extract_event_creation(self, s):
        print("Sentence I am working with: %s" % (s))
        events = []

        event = []
        for token in s:
            if token.dep_ == 'attr':
                event.append(token)
        events.append(event)
        print("CREATED CREATION EVENT: ", events)
        return events

    def extract_keyword_connected_relation(self, template, token):
        first_pass = False
        second_pass = False
        third_pass = False
        if template.third.strip() == "":
            third_pass = True

        relation = Relation()
        relation.keyword = template.keyword
        relation.keyword_type = template.keyword_type
        relation.relation = template.relation
        relation.is_flipped = template.is_flipped

        for child in token.children:
            if child.dep_ == 'neg':
                relation.is_negated = True

            if template.is_flipped == False:
                if template.first == child.dep_ or first_pass == True:
                    # print("In first with token %s(%s):" % (child, child.dep_))

                    if template.second == child.dep_ or second_pass == True:
                        # print("In second with token %s(%s):" % (child, child.dep_))

                        if template.third.strip is not "":
                            if template.third == child.dep_:

                                if third_pass == False:
                                    third_pass = True
                                    relation.third_token = child

                        if second_pass == False:
                            second_pass = True
                            relation.second_token = child

                    if first_pass == False:
                        first_pass = True
                        relation.first_token = child

        if first_pass and second_pass and third_pass:
            return relation
        else:
            return None

    def extract_keywordless_relation(self, template, token):
        # print("Checking %s against %s (dep_ of %s)" % (template.first, token.text, token.dep_))
        if template.first == token.dep_:

            second_pass = False
            third_pass = False
            if template.third.strip() == "":
                third_pass = True

            relation = Relation()
            relation.keyword = template.keyword
            relation.keyword_type = template.keyword_type
            relation.relation = template.relation
            relation.is_flipped = template.is_flipped

            relation.first_token = token

            for child in token.children:

                if template.second == child.dep_ or second_pass == True:
                    # print("In second with token %s(%s):" % (child, child.dep_))

                    if template.third.strip is not "":
                        if template.third == child.dep_:

                            if third_pass == False:
                                third_pass = True
                                relation.third_token = child

                    if second_pass == False:
                        second_pass = True
                        relation.second_token = child

            if second_pass and third_pass:
                return relation

        return None

    def extract_relation_via_template(self, template, token):

        unflipped = ExtractionTemplate.create_unflipped_template(template)
        # if template.is_flipped:
        #     print("\t", str(unflipped))

        # return self.extract_keyword_connected_relation(unflipped, token)
        if template.keyword.strip() == "":
            # print(">>> Keyword-less approach")
            return self.extract_keywordless_relation(unflipped, token)
        else:
            # print(">>> Keyword-connected approach")
            return self.extract_keyword_connected_relation(unflipped, token)


    def get_relations_from_sentence(self, event_type, template, token):
        relations = []
        if event_type == EVENT_DESCRIPTION:
            if template.relation in [IS_A, HAS_PROPERTY, HAS_A, CAPABLE_OF]:
                # print("CHECKING IF THIS RELATION IS POSSIBLE TO WORK WITH")
                extracted = self.extract_relation_via_template(template, token)
                if extracted is not None:
                    # print("Appending", extracted)
                    relations.append(extracted)

        return relations



    def extract_event_attribute(self, sentence, event_type_flag):
        # If event type flag is True, then the passed sentence has a smaller chance of containing a description type thing.
        # Otherwise, if the flag is False, it is more likely to be a Description event.

        extraction_manager = DBOExtractionTemplate("extraction_templates")
        relations = []
        for token in sentence:
            # print("==========================")
            # print("=", token.text)
            # print("==========================")

            extraction_templates = extraction_manager.get_extraction_templates_by_keyword(token.lemma_, token.dep_)
            # extraction_templates.extend(extraction_manager.get_extraction_templates_by_keyword(token.dep_))

            for i in range(len(extraction_templates)):
                # print("\n\nExtraction Template %d: %s" % (i, extraction_templates[i]))
                # print(extraction_templates[i])
                extracted_relations = self.get_relations_from_sentence(EVENT_DESCRIPTION, extraction_templates[i], token)
                if extracted_relations is not None:
                    relations.extend(extracted_relations)

        return relations
        # events = []
        # if relations:
        #     for relation in relations:
        #         if relations is not None:
        #             event = []
        #             event.append(relation.first_token)
        #             event.append(relation.relation)
        #             event.append(relation.keyword)
        #             event.append(relation.second_token)
        #             event.append(relation.third_token)
        #             event.append(relation.is_negated)
        #
        #             events.append(event)
        #
        # return events




    def parse_user_input(self, content, world):
        self.doc = self.nlp(content)

        old_sentence = ""
        for s in world.sentence_references:
            old_sentence = old_sentence + ' ' + str(s)

        sentence = old_sentence + content

        print("\n\n")
        print("Sentence before coref: %s" % (sentence))
        print("\n\n")
        resolved = InputDecoder.get_instance().coref_resolve(sentence)

        print("\n\n")
        print("Sentence after coref: %s" % (resolved))
        print("\n\n")

        print("Sentence to delete: %s" % (old_sentence))
        resolved = resolved.replace(old_sentence, "")
        resolved = resolved.strip()

        print("\n\n")
        print("Final processed sentence: %s" % (resolved))
        print("\n\n")

        self.doc = self.nlp(resolved)

        event_entities = []
        sentence_entities = []
        for s in self.doc.sents:
            # print("Sentence: %s " % (s.text.strip()))
            type = self.guess_event_type(s)

            # Used to check if the passed sentence is already one of the events in the if-else case (either action event or creation event)
            event_type_flag = False

            if type == EVENT_ACTION:
                event_type_flag = True

                events = self.extract_event_aao(s)
                for event in events:
                    # print(event)
                    event_entity = [EVENT_ACTION,
                                    event[ACTOR],
                                    event[ACTION],
                                    event[DIRECT_OBJECT],
                                    event[ADVERB],
                                    event[PREPOSITION],
                                    event[OBJ_PREPOSITION]]

                    # world.add_event(event_entity, s.text)
                    event_entities.append(event_entity)
                    sentence_entities.append(s)

            elif type == EVENT_CREATION:
                event_type_flag = True

                events = self.extract_event_creation(s)
                for event in events:
                    event_entity = [EVENT_CREATION,
                                    event[SUBJECT]]

                    event_entities.append(event_entity)
                    sentence_entities.append(s)

            events = self.extract_event_attribute(s, event_type_flag)
            for event in events:
                event_entity = [EVENT_DESCRIPTION, event]
                event_entities.append(event_entity)
                sentence_entities.append(s)

            self.display_tokens(s)

        return event_entities, sentence_entities

    def append_and_empty_list(self, partial_prepend, partial):
        partial_prepend.extend(partial)
        return partial_prepend, []


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

# parser = InfoExtractor()

# parser.parse_story("The boy killed the girl")

# From Clever Elsie
# parser.parse_story("Oh, the mother can see the wind coming up the street, and hear the flies coughing.")

# Pre-made examples
# text = "Mary had gathered, and chopped the onions, and Ann fried the onions."
# text = "Mary had a little lamb"
# text = "Mary had gathered, and chopped the onions, Ann fried the onions, and James prepared them."
# text = "Mary had gathered, chopped the onions, and fried the onions."
# text = "Mary and Ann had gathered, chopped, and fried the onions and the garlic."
# text = "Mary gathered, chopped, and fried the onions."
# text = "After dear Hans had gone away, Elsie cooked Elsie some good broth and took some good broth into the field with Elsie."
# text = "Mary gathered, and chopped the onions."
# text = "Mary the maid gathered, chopped, and fried the onions."
# text = "It was Mary who gathered, chopped, and fried the onions."
# text = "Mary is playing and running with the dogs in the field"
# text = "Mary went to the pool.\nMary swam."
# parser.parse_story(text)
