import logging

from random import randint

from flask import Flask, render_template, request, json

from flask_ask import Ask, statement, question, session



app = Flask(__name__)

ask = Ask(app, "/")

#logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():
    print("BOO")
    numbers = [randint(0, 9) for _ in range(3)]

    round_msg = render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse
    
    print(session.attributes['numbers'])

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):
    print("BAKIT AYAW MO")
    print(first)

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)

@ask.intent("searchQuery", convert={'query': str})
def poof(query):
    print(query)
    requestJson = request.get_json()
    print(requestJson['request']['intent']['name'])
    
    if query == None:
        msg = "idk. please repeat what you said"
    else:
        msg = "did you say " + query + "?"

    return question(msg)

@ask.intent("AMAZON.FallbackIntent")
def unknown():
    #requestJson = request.get_json()
    #print(requestJson['request']['intent']['name'])
    
    msg = "I don't understand"

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)