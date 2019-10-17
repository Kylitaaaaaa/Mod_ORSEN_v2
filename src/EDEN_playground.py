from src.ORSEN import ORSEN
from src import Logger

response = ["I loved you too much to let you die, dear sister, but your heart was failing you, so I gave you mine.",
            # "He started worrying if he was important and decided he wanted to ask the people he knew if they thought he was important",
            # "They all ignored him and he was very confused on why this was happening.",
            # "As people gathered ’round him, singing loudly, shining bright lights everywhere, he kept his eyes on the light blue horizon.",
            # "Smile, after all, it is Christmas and you have no reason to not smile on Christmas.",
            # "Breathing heavily, Arabella lurched forwards, bearing her sword.",
            # "I must congratulate you on your victory",
            # "You think that I am his true love?",
            # "I will do my best to save our Prince.",
            # "She cried out as the sword flew from her grasp.",
            # "I have broken our promise and cannot help you anymore.",
            # "As soon as I saw him I knew it was a match made in heaven.",
            "Hansel got angry with Gretel",
            "I fought, endured, and cried my way to my degree."]

Logger.setup_loggers()
orsen = ORSEN()

for X in response:
    orsen.perform_text_understanding(X)
    emotion = orsen.get_emotion(X)

    Logger.dump_log("=======================================")

print("DONE CHECKING")