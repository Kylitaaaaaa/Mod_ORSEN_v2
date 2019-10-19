from EDEN.constants import *
from EDEN.db import DBOEmotion

import spacy

from EDEN.models import Emotion
from src.dbo.concept import DBOConcept, DBOConceptGlobalImpl
from src.models.elements import Character
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src import Logger

nlp = spacy.load("en_core_web_sm")

class OCCManager():
    def __init__(self, af="", de="", of="", oa="", sr ="", sp ="", op="", pros="", stat="", unexp=False, sa="", vr=False, ed="", eoa="", edev="", ef=""):
        super().__init__()
        self.curr_action_event = None
        self.response = ""
        self.dbo_concept = DBOConceptGlobalImpl()

        self.emotion = None

        # setup OCC Values
        """Agent-Based"""
        self.af = af
        self.de = de

        """Object-Based"""
        self.of = of
        self.oa = oa

        """Event-Based"""
        self.sr = sr
        self.sp = sp
        self.op = op
        self.pros = pros
        self.stat = stat
        self.unexp = unexp
        self.sa = sa
        self.vr = vr

        """Intensity"""
        self.ed = ed
        self.eoa = eoa
        self.edev = edev
        self.ef = ef

    def reset_occ(self):
        """Agent-Based"""
        self.af = ""
        self.de = ""

        """Object-Based"""
        self.of = ""
        self.oa = ""

        """Event-Based"""
        self.sr = ""
        self.sp = ""
        self.op = ""
        self.pros = ""
        self.stat = ""
        self.unexp = False
        self.sa = ""
        self.vr = False

        """Intensity"""
        self.ed = ""
        self.eoa = ""
        self.edev = ""
        self.ef = ""

    def set_values(self, af="", de="", of="", oa="", sr ="", sp ="", op="", pros="", stat="", unexp=False, sa="", vr=False, ed="", eoa="", edev="", ef=""):
        """Agent-Based"""
        self.af = af
        self.de = de

        """Object-Based"""
        self.of = of
        self.oa = oa

        """Event-Based"""
        self.sr = sr
        self.sp = sp
        self.op = op
        self.pros = pros
        self.stat = stat
        self.unexp = unexp
        self.sa = sa
        self.vr = vr

        """Intensity"""
        self.ed = ed
        self.eoa = eoa
        self.edev = edev
        self.ef = ef

    def get_occ_emotion(self, curr_action_event, response):
        # setup event to evaluate
        self.curr_action_event = curr_action_event

        # setup response
        self.response = response

        print("CHECKING AT OCC: ", curr_action_event.sequence_number)
        # setup emotion
        self.emotion = self.get_emotion(str(curr_action_event.verb.lemma_))


        if self.emotion is None:
            Logger.log_occ_values(
                "EVALUATING: " + str(curr_action_event.sequence_number) + " : " + self.get_vader_event_string())
            Logger.log_occ_values("NO EMOTION FOUND")
            return None

        self.set_state()

        return self.choose_emotion(curr_action_event, self.get_event_valence())

    def choose_emotion(self, curr_action_event=None, event_valence=None):
        curr_emotions = []

        # Logger.log_occ_values(
        #     "EVALUATING: " + str(curr_action_event.sequence_number) + " : " + self.get_vader_event_string())
        # Logger.log_occ_values(self.print_occ_values())

        # self.print_occ_values()

        chosen_emotion = None
        if self.vr:
            if self.sr == SR_DISPLEASED:
                if self.de == DE_OTHERS:
                    if self.sp == SP_UNDESIRABLE and self.of == OF_NOT_LIKED and self.oa == OA_NOT_ATTRACTIVE and event_valence == VADER_NEGATIVE:
                        curr_emotions.append(OCC_HATE)
                    if self.op == OP_UNDESIRABLE and self.af == AF_LIKED:
                        curr_emotions.append(OCC_SORRY_FOR)
                    if self.op == OP_DESIRABLE and self.af == AF_NOT_LIKED:
                        curr_emotions.append(OCC_RESENTMENT)
                    if self.sa == SA_BLAME and self.op == OP_UNDESIRABLE:
                        # curr_emotions.append(OCC_REPROACH)
                        curr_emotions.append(OCC_ANGER)

                if self.de == DE_SELF:
                    if self.sp == SP_UNDESIRABLE:
                        curr_emotions.append(OCC_DISTRESS)
                    if self.pros == PROS_NEGATIVE and self.sp == SP_UNDESIRABLE and self.stat == STAT_UNCONFIRMED:
                        curr_emotions.append(OCC_FEAR)
                        # curr_emotions.append(OCC_FEARS_CONFIRMED)
                    if self.pros == PROS_NEGATIVE and self.sp == SP_UNDESIRABLE and self.stat == STAT_CONFIRMED:
                        curr_emotions.append(OCC_FEARS_CONFIRMED)
                    if self.sa == SA_BLAME and self.sp == SP_UNDESIRABLE:
                        curr_emotions.append(OCC_SHAME)
                        # curr_emotions.append(OCC_ANGER)
                    if self.pros == PROS_POSITIVE and self.sp == SP_DESIRABLE and self.stat == STAT_DISCONFIRMED:
                        curr_emotions.append(OCC_DISAPPOINTMENT)

            if self.sr == SR_PLEASED:
                if self.sp == SP_DESIRABLE:
                    curr_emotions.append(OCC_JOY)

                if self.de == DE_OTHERS:
                    # if self.op == OP_UNDESIRABLE and self.af == AF_NOT_LIKED:
                    #     curr_emotions.append(OCC_GLOATING)
                    if self.sa == SA_PRAISE and self.op == OP_DESIRABLE:
                        curr_emotions.append(OCC_ADMIRATION)
                        # curr_emotions.append(OCC_GRATITUDE)
                    if self.sp == SP_DESIRABLE and self.of == OF_LIKED and self.oa == OA_ATTRACTIVE and event_valence == VADER_POSITIVE:
                        curr_emotions.append(OCC_LOVE)

                if self.de == DE_SELF:
                    if self.pros == PROS_POSITIVE and self.sp == SP_DESIRABLE and self.stat == STAT_UNCONFIRMED:
                        curr_emotions.append(OCC_HOPE)
                        # curr_emotions.append(OCC_SATISFACTION)
                    if self.pros == PROS_POSITIVE and self.sp == SP_DESIRABLE and self.stat == STAT_CONFIRMED:
                        curr_emotions.append(OCC_SATISFACTION)
                    if self.pros == PROS_NEGATIVE and self.sp == SP_UNDESIRABLE and self.stat == STAT_DISCONFIRMED:
                        curr_emotions.append(OCC_RELIEF)
                    if self.sa == SA_PRAISE and self.sp == SP_DESIRABLE:
                        curr_emotions.append(OCC_PRIDE)
                        # curr_emotions.append(OCC_GRATITUDE)

            if OCC_JOY in curr_emotions and OCC_PRIDE in curr_emotions:
                curr_emotions.append(OCC_GRATIFICATION)
            if OCC_DISTRESS in curr_emotions and OCC_SHAME in curr_emotions:
                curr_emotions.append(OCC_REMORSE)
            if OCC_JOY in curr_emotions and OCC_ADMIRATION in curr_emotions:
                curr_emotions.append(OCC_GRATITUDE)
            # if OCC_DISTRESS in curr_emotions and OCC_REPROACH in curr_emotions:
            #     curr_emotions.append(OCC_ANGER)

            if OCC_DISTRESS in curr_emotions and self.unexp:
                curr_emotions.append(OCC_SHOCK)
            if OCC_JOY in curr_emotions and self.unexp:
                curr_emotions.append(OCC_SURPRISE)

            # if (
            #         OCC_FEARS_CONFIRMED in curr_emotions or OCC_FEAR in curr_emotions) and OCC_SATISFACTION in curr_emotions:
            #     chosen_emotion = OCC_RELIEF
            # if OCC_HOPE in curr_emotions and (OCC_FEARS_CONFIRMED in curr_emotions or OCC_FEAR in curr_emotions):
            #     chosen_emotion = OCC_DISAPPOINTMENT
            # if OCC_ANGER in curr_emotions and (OCC_GRATIFICATION in curr_emotions or OCC_GRATITUDE in curr_emotions):
            #     chosen_emotion = OCC_GRATITUDE
            # if OCC_REMORSE in curr_emotions and (OCC_GRATIFICATION in curr_emotions or OCC_GRATITUDE in curr_emotions):
            #     chosen_emotion = OCC_GRATITUDE
            # if OCC_GRATIFICATION and (OCC_REMORSE in curr_emotions or OCC_ANGER in curr_emotions):
            #     chosen_emotion = OCC_ANGER
            # if OCC_GRATITUDE in curr_emotions and (OCC_REMORSE in curr_emotions or OCC_ANGER in curr_emotions):
            #     chosen_emotion = OCC_ANGER


            if len(curr_emotions) > 0:
                listToStr = ' '.join([str(curr_emotion) for curr_emotion in curr_emotions])
                print("EMOTIONS FOUND: " + listToStr)
                Logger.log_occ_values("EMOTIONS FOUND: " + listToStr)
                if chosen_emotion is None:
                    chosen_emotion = curr_emotions[0]

        # print("CHOSEN EMOTION IS: ", chosen_emotion)
        if chosen_emotion is not None:
            Logger.log_occ_values("CHOSEN EMOTION: " + chosen_emotion)
            return Emotion(curr_action_event,
                           emotion=chosen_emotion,
                           af=self.af,
                           de=self.de,
                           of=self.of,
                           oa=self.oa,
                           sp=self.sp,
                           sr=self.sr,
                           op=self.op,
                           pros=self.pros,
                           stat=self.stat,
                           unexp=self.unexp,
                           sa=self.sa,
                           vr=self.vr,
                           ed=self.ed,
                           eoa=self.eoa,
                           edev=self.edev,
                           ef=self.ef)
        else:
            Logger.log_occ_values("NO EMOTION FOUND")
        return None

    def set_state(self):


        """Get OCC Values"""
        """Agent-Based"""
        self.af, self.of = self.get_af_of()
        self.de = self.get_de()

        """Object-Based"""
        self.oa = self.get_oa()

        """Event-Based"""
        self.sp, self.sr = self.get_sp_sr()
        self.op = self.get_op()
        self.pros = self.get_pros()
        self.stat = self.get_stat()
        self.unexp = self.get_unexp()
        self.sa = self.get_sa()
        self.vr = self.get_vr()

        """Intensity"""
        self.ed = self.get_ed()
        self.eoa = self.get_eoa()
        self.edev = self.get_edev()
        self.ef = self.get_ef()

    def print_occ_values(self):
        Logger.log_occ_values_basic(self.af + " , " + self.de + " , " +
                                    self.of + " , " + self.oa + " , " +
                                    self.sp + " , " + self.sr + " , " + self.op + " , " + self.pros + " , " + self.stat + " , " + str(self.unexp) + " , " +   self.sa + " , " +   str(self.vr) + " , " +
                                    self.ed + " , " + self.eoa + " , " + self.edev + " , " + self.ef)


        # Logger.log_occ_values_basic("OCC VALUES:")
        # Logger.log_occ_values_basic("Agent:")
        # Logger.log_occ_values_basic( "AF: " + self.af)
        # Logger.log_occ_values_basic("DE: " + self.de)
        #
        # Logger.log_occ_values_basic("Object:")
        # Logger.log_occ_values_basic("OF: " + self.of)
        # Logger.log_occ_values_basic("OA: " + self.oa)
        #
        # Logger.log_occ_values_basic("Event:")
        # Logger.log_occ_values_basic("SP: " + self.sp)
        # Logger.log_occ_values_basic("SR: " + self.sr)
        # Logger.log_occ_values_basic("OP: " + self.op)
        # Logger.log_occ_values_basic("PROS: " + self.pros)
        # Logger.log_occ_values_basic("STAT: " + self.stat)
        # Logger.log_occ_values_basic("UNEXP: " + str(self.unexp))
        # Logger.log_occ_values_basic("SA: " + self.sa)
        # Logger.log_occ_values_basic("VR: " + str(self.vr))
        #
        # Logger.log_occ_values_basic("Intensity:")
        # Logger.log_occ_values_basic("ED: " + self.ed)
        # Logger.log_occ_values_basic("EOA: " + self.eoa)
        # Logger.log_occ_values_basic("EDEV: " + self.edev)
        # Logger.log_occ_values_basic("EF: " + self.ef)


    def get_emotion(self, term):
        dbo_emotion = DBOEmotion('nrc_emotion')

        curr_term = dbo_emotion.get_term(term)

        if curr_term is None:
            print("======= NO EMOTION FROM DATABASE: ", term)
            return None
        curr_term.compute_occ_values()
        print(curr_term)
        return curr_term

    """Agent-Based"""
    """
    Agent/Object Fondness (af/of)
        Check whether the subject (Character or Object) of the event's Valence (Vader). 
        
        Valence can be: Positive, Negative
        
        If Negative Valence --> Not Liked
        Else --> Liked
    
        Ex:
            Thief --> Negative Valence
            Hero --> Positive Valence
    """
    def get_af_of(self):
        sentiment = self.get_vader_sentiment(self.curr_action_event.subject.name)
        if sentiment == VADER_NEGATIVE:
            return AF_NOT_LIKED, OF_NOT_LIKED
        return AF_LIKED, AF_NOT_LIKED

    """
    Direction of Emotion (de)
        Check whether the agent reacts towards consequences of events for self or others

        If direct object is a person (Character) --> others
        Else --> self    
    """
    def get_de(self):
        if self.curr_action_event.direct_object is not None:
            if type(self.curr_action_event.direct_object) == Character:
                return DE_OTHERS
        return DE_SELF

    """OBJECT"""
    """
    Object Appealing (oa)
        Check whether object is attractive or not attractive based on Object Valence (Vader) and Familiarity (ORSEN Commonsense Ontology)
        
        Valence can be: Positive, Negative, Neutral
        Familiarity can be: True (Common), False (Uncommon)
        
        If Uncommon, Negative Valence --> Not Attractive
        If Uncommon, Positive Valence --> Attractive
        If Common, Negative Valence --> Not Attractive
        If Common, Positive Valence --> Neutral
        
        Ex:
            Restaurant --> Common, Positive ---> Neutral
            Thief --> Common, Negative --> Not Attractive 
    """
    def get_oa(self):
        for X in self.curr_action_event.get_objects_involved():
            sentiment = self.get_vader_sentiment(X.name)
            if self.is_familiar(X.name):
                if sentiment == VADER_NEGATIVE:
                    return OA_NOT_ATTRACTIVE
                elif sentiment == VADER_POSITIVE:
                    return OA_NEUTRAL
            else:
                if sentiment == VADER_NEGATIVE:
                    return OA_NOT_ATTRACTIVE
                return OA_ATTRACTIVE
        return OA_ATTRACTIVE

    """EVENT"""
    """
    Self Presumption (sp) and Self Reaction (sr)
        Checks how desirable and pleasing the event (verb + direct object) is using Valence (Vader).
            
        Valence can be: Positive, Negative, Neutral
            
        If Negative Valence --> Undesirable (sp), Displeased (sr)
        If Positive Valence --> Desirable (sp), Pleased (sr)

        Ex:
            kill innocent people --> Negative Valence --> Undesirable (sp), Displeased (sr)
            like romantic movies --> Positive Valence --> Desirable (sp), Pleased (sr)
            like horror movies --> Negative Valence --> Undesirable (sp), Displeased (sr)
    """
    def get_sp_sr(self):
        sentiment = self.get_vader_sentiment(self.get_vader_event_string())
        print("SENTIMENT FROM VADER IS: ", sentiment)
        if sentiment == VADER_NEGATIVE:
            return SP_UNDESIRABLE, SR_DISPLEASED
        return SP_DESIRABLE, SR_PLEASED

    """
    Others Presumption (op)
        Assess the event from the eyes of the subject (Character) based on subject (Character) and event (verb, direct object)

        Valence can be: Positive, Negative, Neutral

        If Positive Valence (Agent) and Positive Valence (Event) --> Desirable
        If Positive Valence (Agent) and Negative Valence (Event) --> Undesirable
        If Negative Valence (Agent) and Positive Valence (Event) --> Undesirable
        If Negative Valence (Agent) and Negative Valence (Event) --> Undesirable
            
        Ex:
            Teacher punished boy for breaking the rules --> Positive Valence (Agent) and Negative Valence (Event) --> Undesirable
            The criminal loved a girl --> Negative Valence (Agent) and Positive Valence (Event) --> Undesirable
        """
    def get_op(self):
        subj_val = ""
        verb_obj_val = ""

        #check subject
        subj_val = self.get_vader_sentiment(self.curr_action_event.subject.name)

        #check verb and object
        verb_obj_val = self.get_vader_sentiment(self.get_vader_event_string())

        if subj_val == VADER_NEGATIVE or verb_obj_val == VADER_NEGATIVE:
            return OP_UNDESIRABLE
        return OP_DESIRABLE

    """
    Prospect (pros)
        Checks whether an event involves a conscious expectation that it will occur in the future (Verb Emotion -- Prospect Polarity)
        
        Threshold = 3.5
    """
    def get_pros(self):
        if self.emotion.prospect_polarity >= 3.5:
            return PROS_POSITIVE
        elif self.emotion.prospect_polarity <= -3.5:
            return PROS_NEGATIVE
        else:
            return PROS_NEUTRAL

    """
    Status (stat)
        Checks the tense of the verb whether it has already happened.
        
        If Present, Future --> Unconfirmed
        If Past without negation --> Confirmed
        If Past with negation --> Disconfirmed

        Ex:
            He will come --> Unconfirmed
            The team played well --> Confirmed
            The team did not play well --> Disconfirmed
        """
    def get_stat(self):
        doc = nlp(self.response)

        #check if input has past verb tense
        past_verb_tokens = [tok for tok in doc if (tok.tag_ == 'VBD' or tok.tag_ == "VBN")]
        print(past_verb_tokens)

        #check if input has negation
        negation_tokens = [tok for tok in doc if tok.dep_ == 'neg']
        print(negation_tokens)

        if len(past_verb_tokens) > 0:
            if len(negation_tokens) > 0:
                return STAT_DISCONFIRMED
            else:
                return STAT_CONFIRMED
        return STAT_UNCONFIRMED

    """
    Unexpectedness (unexp)
        Checks if the event is described in an abrupt or sudden manner. 
        
        If keyword is found in UNEXP_LIST --> True
        Else --> False
    """
    def get_unexp(self):
        for X in UNEXP_LIST:
            if X in self.response:
                return True
        return False

    """
    Self Appraisal (sa)
        Checks if the event is praiseworthy or blameworthy based on the verb emotion (Prior Valence and Prospective Value)
        
        Threshold = 4.5
    """
    def get_sa(self):
        if self.emotion.praiseworthy_value >= 4.5:
            return SA_PRAISE
        elif self.emotion.praiseworthy_value <= -4.5:
            return SA_BLAME
        else:
            return SA_NEUTRAL

    """
    Valenced Reaction (vr)
        Checks the emotions are present in the sentence using Valence (Vader).
        
        If Neutral Valence --> False
        Else --> True 
    """
    def get_vr(self):
        """VADER: https://github.com/cjhutto/vaderSentiment"""

        # sentiment, score = self.get_vader_sentiment(self.response)
        sentiment = self.get_vader_sentiment(self.response)
        if sentiment == VADER_NEUTRAL:
            return False
        return True

    """INTENSITY"""
    """
    Event Deservingness (ed)
        Checks if the doer of the action thinks that the event is deserving for self or others based on Valence (Vader) of event (verb + direct object).
        
        If Positive Valence --> High
        Else --> Low
    """
    def get_ed(self):
        sentiment = self.get_vader_sentiment(self.get_vader_event_string())
        if sentiment == VADER_POSITIVE:
            return ED_HIGH
        return ED_LOW

    """
    Effort of Action (eoa)
        Checks if effort has been invested. 
        
        If adverb is present and not in EXC_ADVERB_LIST (Exceptional Adverbs) --> Obvious
        If objects have attributes and not negated --> Obvious
        Else --> Not Obvious 
    """
    def get_eoa(self):
        #check if has adverb and not exceptional adverb
        if self.curr_action_event.adverb is not None:
            if str(self.curr_action_event.adverb.lemma_) not in EXC_ADVERB_LIST:
                return EOA_OBVIOUS
        elif len(self.curr_action_event.get_objects_involved()) > 0:
            for object in self.curr_action_event.get_objects_involved():
                print(object.attribute)
                for attribute in object.attribute:
                    if attribute.is_negated:
                        return EOA_NOT_OBVIOUS
            return EOA_OBVIOUS
        return EOA_NOT_OBVIOUS

    """
    Expected Deviation (edev)
        Checks if the subject and event (verb) is presumably expected by the subject. Checks ORSEN's Commonsense Ontology if relation exists or not.
        
        If relation exists --> Low
        Else --> High
        
        Ex:
            A student invented a theory --> High
            Scientist invented the theory --> Low
    """
    def get_edev(self):
        concepts = self.dbo_concept.get_specific_concept(self.curr_action_event.subject.name, 'CapableOf', str(self.curr_action_event.verb.lemma_))
        if concepts is not None:
            return EDEV_LOW
        return EDEV_HIGH

    """
    Event Familiarity
        Checks whether action and object are common based on ORSEN's Commonsense Ontology.
        
        If do is None --> Common
        If verb exists, do exists --> Common
        If verb exists, do does not exists --> Uncommon
        If verb does not exists, do does not exists --> Uncommon  
    """
    def get_ef(self):
        if self.curr_action_event.direct_object is None:
            return EF_COMMON

        if len(self.dbo_concept.get_concept_by_word(str(self.curr_action_event.verb.lemma_))) > 0:
            if len(self.dbo_concept.get_concept_by_word(self.curr_action_event.direct_object.name)) > 0:
                return EF_COMMON
        return EF_UNCOMMON

    """VADER FUNCTIONS"""

    def get_vader_event_string(self):

        final_string = str(self.curr_action_event.verb.lemma_)
        if self.curr_action_event.direct_object is not None:
            final_string = final_string + " " + self.curr_action_event.direct_object.name

        print("THIS IS THE FINAL STRING: ", final_string)
        final_string = str(final_string)
        return final_string


    def get_vader_sentiment(self, to_eval_str):

        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(to_eval_str)
        if vs['compound'] >= 0.05:
            sent = VADER_POSITIVE
        elif vs['compound'] <= -0.05:
            sent = VADER_NEGATIVE
        else:
            sent = VADER_NEUTRAL

        # return sent, vs['compound']
        return sent

    """DATABASE FUNCTIONS"""
    def is_familiar(self, word):
        if len(self.dbo_concept.get_concept_by_word(word)) > 0:
            return True
        return False

    def get_event_valence(self):
        return self.get_vader_sentiment(self.get_vader_event_string())
