class Sentence:
    words = ""              # Actual sentence input
    text_token = []         # Tokenized version of input
    head_text = []
    lemma = []              # base of word
    pos = []                # part of speech
    tag = []                # part of speech acronym
    dep = []                # dependency
    children = []           # 
    ner = []

    text_ent = []
    label = []

    text_chunk = []         # subject/topic(?)
    dep_root = []           # dependency of the connector
    dep_root_head = []      # word that connects the subject

    finished_nodes = []

    location = {}

    def __init__(self):
        self.words = ""
        self.text_token = []
        self.head_text = []
        self.lemma = []
        self.pos = []
        self.tag = []
        self.dep = []
        self.children = []

        self.text_ent = []
        self.label = []

        self.text_chunk = []
        self.dep_root = []
        self.dep_root_head = []

        self.finished_nodes = []
        self.location = {}
