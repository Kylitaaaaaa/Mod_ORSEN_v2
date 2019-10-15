"""
Original lexicon: http://sentiment.nrc.ca/lexicons-for-research/
Supporting research: https://www.researchgate.net/publication/331256216_Using_sentiment_analysis_to_detect_affect_in_children's_and_adolescents'_poetry
"""

#ORIG FILE CAN BE SEEN IN: http://sentiment.nrc.ca/lexicons-for-research/

import csv



def write_data(tabs):
    with open('nrc_emotion_lexicon.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(tabs)
    csvFile.close()

def read_data():
    path = 'NRC-Emotion-Lexicon-Senselevel-v0.92.txt'
    days_file = open(path, 'r')
    contents = days_file.read()

    splitted = contents.split('\n')

    del splitted[-1]

    Y = []
    for X in splitted:
        parsed = X.split('--')
        Y.append(parsed)

    tabs = []
    for X in Y:
        curr = []
        curr.append(X[0])

        curr_result_tabs = X[1].split('\t')

        curr.append(curr_result_tabs[1])
        curr.append(int(curr_result_tabs[2]))

        curr_result_comma = curr_result_tabs[0].split(', ')

        for i in curr_result_comma:
            curr.append(i)

        tabs.append(curr)

    return tabs

def format_data(retrieved_data):
    new_format = []
    new_format.append(['term', 'fear', 'anger', 'anticip', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy', 'synonym_1', 'synonym_2', 'synonym_3'])
    curr_row = []
    curr_row.append(retrieved_data[0][0])
    for i in range(len(retrieved_data)):
        if i%10 == 0 and not i==0:
            for j in range (3, len(retrieved_data[i-1])):
                curr_row.append(retrieved_data[i-1][j])

            new_format.append(curr_row)
            curr_row = []
            curr_row.append(retrieved_data[i][0])
        curr_row.append(retrieved_data[i][2])

    return new_format



print("start")
retrieved_data = read_data()

new_format = format_data(retrieved_data)

write_data(new_format)

print("done")
