from EDEN.models import EmotionActionEvent, EmotionDescriptionEvent
from src.knowledgeacquisition.followup.SuggestingDialogueTemplate import SuggestingDialogueTemplate
from src.models.dialogue import *
from src.constants import *


class EmotionEventTemplateBuilder:


   # def build(event, emotion =[], af="", de="", of="", oa="", sp="", sr="", op="", pros="", stat="", unexp=False, sa="", vr=False, ed="", eoa="", edev="", ef=""):
   @staticmethod
   def build(event=None, emotion="", af="", de="", of="", oa="", sp="", sr="", op="", pros="", stat="", unexp=False,
                 sa="", vr=False, ed="", eoa="", edev="", ef=""):
      if event.type == EVENT_ACTION:
          return EmotionActionEvent(event, emotion, af, de, of, oa, sp, sr, op, pros, stat, unexp, sa, vr, ed, eoa, edev, ef)
      elif event.type == EVENT_DESCRIPTION:
          return EmotionDescriptionEvent(event, emotion, af, de, of, oa, sp, sr, op, pros, stat, unexp, sa, vr, ed, eoa, edev, ef)
      # return EmotionActionEvent(event, emotion, af, de, of, oa, sp, sr, op, pros, stat, unexp, sa, vr, ed, eoa, edev,
      #                           ef)
