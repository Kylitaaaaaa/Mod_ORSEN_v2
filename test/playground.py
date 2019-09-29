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

from src.textunderstanding import InputDecoder
InputDecoder.get_instance().perform_input_decoding("Matthew used the drink that he got from from the vending machine.")