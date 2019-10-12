class DialogueHistoryTemplate:

    def __init__(self, dialogue_type='', template_id=-1, template="", word_relation=None):
        self.dialogue_type = dialogue_type
        self.template_id = template_id
        self.template = template
        self.word_relation = word_relation

    def set_template_details(self, chosen_template):
        self.template_id = chosen_template.id
        self.template = chosen_template.template




