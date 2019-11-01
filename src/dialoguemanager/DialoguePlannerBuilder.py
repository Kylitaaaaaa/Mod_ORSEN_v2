from src.constants import *
from src.dialoguemanager import EDENDialoguePlanner
from src.dialoguemanager import ORSEN2DialoguePlanner

class DialoguePlannerBuilder:

   @staticmethod
   def build(orsen_type):
        planner = None

        if orsen_type == ORSEN2:
            planner = ORSEN2DialoguePlanner()

        elif orsen_type == EDEN:
            planner = EDENDialoguePlanner()

        return planner
