
class StoryWorldExtraction:

    def __init__(self):
        pass

    def extract_events(self):
        pass

    def extract_details(self, sent, world, current_node, subj="", neg="", text=""):
        num = -1

        subject = subj
        dative = ""
        direct_object = ""

        if text == "":
            if current_node._.is_traversed == False:
                current_node._.is_traversed = True

        else:
            if current_node._.is_traversed == False and current_node.text == text:
                current_node._.is_traversed = True

            if current_node.dep_ == "ROOT" and current_node.pos_ in ['NOUN', 'PROPN']:
                self.add_objects(sent, current_node)
        # add_objects(sent, str(subject), sent.dep[num], sent.lemma[i], world)


        is_negative = neg
        if is_negative == "":
            is_negative = False

    # def add_objects(self, sent, current_node):



