from EDEN.constants import *
from src.models.events import ActionEvent


class Emotion(ActionEvent):

    def __init__(self, event, emotion =""):
        print("event is")
        print(event)
        super().__init__(sequence_number = event.sequence_number, subject=event.subject, verb=event.verb, direct_object=event.direct_object, adverb=event.adverb, preposition=event.preposition, object_of_preposition=event.object_of_preposition)
        self.event = event
        self.emotion = emotion

    def get_emotion_type(self):
        if self.emotion in NEGATIVE_EMOTIONS:
            return EMOTION_TYPE_NEGATIVE
        return EMOTION_TYPE_POSITIVE