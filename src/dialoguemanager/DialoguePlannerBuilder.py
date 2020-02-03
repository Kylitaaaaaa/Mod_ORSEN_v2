from src import ORSEN2, EDEN
from src.dialoguemanager.EDENDIaloguePlanner import EDENDialoguePlanner
from src.dialoguemanager.ORSEN2DialoguePlanner import ORSEN2DialoguePlanner


class DialoguePlannerBuilder:

   @staticmethod
   def build(orsen_type):
      if orsen_type == ORSEN2:
          return ORSEN2DialoguePlanner()

      elif orsen_type == EDEN:
          return EDENDialoguePlanner()
