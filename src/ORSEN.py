from src.textunderstanding import InputDecoder
from . import Logger

class ORSEN:

    def __init___(self):
        super().__init__()

    def execute_text_understanding(self, input):
        result = InputDecoder.annotate_input(input)
        print("Printing result")
        print(result)

    def start_conversation(self):
        # Initialize loggers
        Logger.setup_loggers()

        print("Input text")














