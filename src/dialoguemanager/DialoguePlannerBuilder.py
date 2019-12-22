from src import ORSEN2, EDEN, ORSEN
from src.dialoguemanager.EDENDIaloguePlanner import EDENDialoguePlanner
from src.dialoguemanager.ORSENDialoguePlanner import ORSENDialoguePlanner
from src.dialoguemanager.ORSEN2DialoguePlanner import ORSEN2DialoguePlanner


class DialoguePlannerBuilder:

   @staticmethod
   def build(orsen_type):
      if orsen_type == ORSEN:
          return ORSENDialoguePlanner()
      elif orsen_type == ORSEN2:
          return ORSEN2DialoguePlanner()

      elif orsen_type == EDEN:
          return EDENDialoguePlanner()
