from EDEN.constants import *
from src.models.events import ActionEvent, Event
from src import Logger, EVENT_ACTION, EVENT_DESCRIPTION
from src.models.pickles.PickleObject import PickleObject


class EmotionActionEvent(ActionEvent):

    def __init__(self, event, emotion =[], af="", de="", of="", oa="", sp="", sr="", op="", pros="", stat="", unexp=False, sa="", vr=False, ed="", eoa="", edev="", ef=""):
        if event is not None:
            super().__init__(sequence_number = event.sequence_number, subject=event.subject, verb=event.verb, direct_object=event.direct_object, adverb=event.adverb, preposition=event.preposition, object_of_preposition=event.object_of_preposition)

        self.event = event
        self.emotion = emotion
        self.af = af
        self.de = de
        self.of = of
        self.oa = oa
        self.sp = sp
        self.sr = sr
        self.op = op
        self.pros = pros
        self.stat = stat
        self.unexp = unexp
        self.sa = sa
        self.vr = vr
        self.ed = ed
        self.eoa = eoa
        self.edev = edev
        self.ef = ef
        self.type = EVENT_EMOTION

    def get_emotion_type(self):
        if self.emotion in NEGATIVE_EMOTIONS:
            return EMOTION_TYPE_NEGATIVE
        return EMOTION_TYPE_POSITIVE


    def print_occ_values(self):
        Logger.log_occ_values(self.af + " , " + self.de + " , " +
                                    self.of + " , " + self.oa + " , " +
                                    self.sp + " , " + self.sr + " , " + self.op + " , " + self.pros + " , " + self.stat + " , " + str(
                                    self.unexp) + " , " + self.sa + " , " + str(self.vr) + " , " +
                                    self.ed + " , " + self.eoa + " , " + self.edev + " , " + self.ef)


    def get_pickled_emotion_event(self):
        pickled_event = self.get_pickled_event()
        pickled_event.af = self.af
        pickled_event.de = self.de
        pickled_event.of = self.of
        pickled_event.oa = self.oa
        pickled_event.sp = self.sp
        pickled_event.sr = self.sr
        pickled_event.op = self.op
        pickled_event.pros = self.pros
        pickled_event.stat = self.stat
        pickled_event.unexp = self.unexp
        pickled_event.sa = self.sa
        pickled_event.vr = self.vr
        pickled_event.ed = self.ed
        pickled_event.eoa = self.eoa
        pickled_event.edev = self.edev
        pickled_event.ef = self.ef

        return pickled_event


    def __str__(self):
        temp_str = "========== ACTION EMOTION EVENT FOUND ========== \n Event Seq No: " + str(self.event.sequence_number) + "\nEmotion: " + self.emotion
        return temp_str