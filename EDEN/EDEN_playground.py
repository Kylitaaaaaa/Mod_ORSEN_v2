import spacy
sp = spacy.load('en_core_web_sm')

# sen = sp(u"I like to play football. I hated it in my childhood though")
# print(spacy.explain(sen[7].tag_))

"""
# TODO as oct 10
status for event
https://www.clips.uantwerpen.be/pages/mbsp-tags
https://spacy.io/usage/linguistic-features
 
"""

#
#
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
    #from vaderSentiment import SentimentIntensityAnalyzer

# --- examples -------
sentences = ["the girl cried last night",
             "the girl",
             "cried",
             "last night"

             ]

analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence)
    sent = ""
    if vs['compound'] >= 0.05:
        sent = "POSITIVE"
    elif vs['compound'] <= -0.05:
        sent = "NEGATIVE"
    else:
        sent = "NEUTRAL"
    print("{:-<65} {}".format(sentence, str(vs)), " ---- ", sent)


# import spacy
#
# nlp = spacy.load("en_core_web_sm")
# # doc = nlp("Apple is looking at not buying U.K. startup for $1 billion")
# doc = nlp("The team may not play")
#
# for token in doc:
#     print(token.text, "\t", token.pos_, "\t", token.tag_)
#     # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#     #         token.shape_, token.is_alpha, token.is_stop, "\n")
#
#
# past_verb_tokens = [tok for tok in doc if (tok.tag_ == 'VBD' or tok.tag_ == "VBN")]
# print(past_verb_tokens)
#
#
# negation_tokens = [tok for tok in doc if tok.dep_ == 'neg']
# print(negation_tokens)

