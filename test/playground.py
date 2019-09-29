# relation_string = "1 Object, 1 HasProperty 2"
#
# relations_split = relation_string.split(",")
#
# relations = []
# # for r in relations_split:
# #     r = r.strip()
# #     pattern = r.split(" ")
# #     print(pattern)
#
# [relations.append(r.strip().split(" ")) for r in relations_split]
# print(relations)
# xd = ' '.join(relations[1])
# print(xd)

from src import Logger

# Logger.setup_loggers()
#
# Logger.log_conversation("I HAD A PUPPY")
# Logger.log_dialogue_model("IT WAS SAD")
# Logger.log_conversation("THE PUPPY DIEID")
from src.models import World

from src.textunderstanding import InputDecoder, EizenExtractor
from src.dataprocessor import Annotator
# InputDecoder.get_instance().perform_input_decoding("Matthew used the drink that he got from from the vending machine.")

annotator = Annotator()
# annotator.annotate("Hansel chopped the garlic, Mary killed the bees and flew to the moon, and Susan fried the onions and peeled the potatoes.")
# annotator.annotate("Pepper is barking at the delivery man angrily.")
# annotator.annotate("The delivery man was hastily approached by the young man.")
annotator.annotate("Pepper is angrily barking at the delivery man")
# annotator.annotate("Phillip sings rather enormously too loudly.")
story = "Pepper is angrily barking at the delivery man."
annotator.annotate(story)

doc = annotator.get_annotated()
for sent in doc.sents:
    InputDecoder.get_instance().display_tokens(sent)

extractor = EizenExtractor()
print(extractor.parse_user_input(story, World()))

