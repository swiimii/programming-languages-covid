import datetime
from flask import Flask, render_template, request
from pyswip import Prolog
from subprocess import run

from prolog.databaseinteractions import getDBInfo


app = Flask(__name__)

PROLOG_PATH = 'prolog/data/database.pl'
PROLOG_OBJ = Prolog()
PROLOG_OBJ.consult(PROLOG_PATH)


# Global dicts generated from Prolog database
Q_ALL_ANS = {}
Q_A_PAIRS = {}

for questionNum in range(1, 4):
    prolog_data = getDBInfo(questionNum)
    Q_ALL_ANS[prolog_data[0]] = prolog_data[1]
    Q_A_PAIRS[prolog_data[0]] = prolog_data[2]


@app.route('/')
def home():
    ''' Renders the home page
    '''
    return render_template('site.html')


@app.route('/quiz')
def quiz():
    ''' Method to launch/render the blank quiz page. Randomizes the order of
    the questions just to do some Imperative stuff lol and you know, for science
    (incase order impacts answers or something).

    "return" key_list: list of keys (strings) in a randomized order
    "return" Q_ALL_ANS: our question and answers dict. The html form will generate
                        the quiz by iterating through the keys and supplying the
                        answers based on the dict's value at each key. see lines
                        4 and 6 in quiz.html
    '''
    key_list = list(Q_ALL_ANS.keys())

    # psuedo randomize the key value pairs using modulu time
    for key in Q_ALL_ANS.keys():
        pos = key_list.index(key) if key_list.index(key) else 1
        new_pos = datetime.datetime.now().second % pos

        if new_pos > len(key_list):
            new_pos = len(key_list) - 1

        key_list.insert(new_pos, key_list.pop(key_list.index(key)))

    return render_template('quiz.html', questions=key_list, answer_options=Q_ALL_ANS)


@app.route('/quiz', methods=['POST'])
def quiz_answers():
    ''' Method for posting the filled out form data. Does a quick check to see
    it was filled out and redirects the user to the quiz if not. If it was, will
    check answers using prolog.GetAnswers. Will then send the "post_dict_ to C++
    for global comparison

    NOTE: the app.route is the same as the above so that when you POST using the
    submit button, we collect and send the data. Will have to return another page
    after we get C++ going in it.

    "return" post_dict: dict where keys are the question number in the prolog db
                        and the value is a bool of whether or not they were correct
    '''
    # NOTE: request.form just gets the info filled out; doesn't disallow not answering
    if len(request.form.to_dict()) != len(Q_ALL_ANS):
        return '<a href="http://127.0.0.1:5000/quiz"><h1>Please try again. Not all questions answered</h1></a>'

    post_dict = {}
    key_list = list(Q_ALL_ANS.keys())
    user_answers_dict = request.form.to_dict()

    # NOTE: Sam's database starts at 1 instead of 0 because "question 1"
    for i in range(len(Q_A_PAIRS)):
        iteration_key = key_list[i]
        # Save the q number, i+1, as the key and True if they answered correctly
        if user_answers_dict[iteration_key] == Q_A_PAIRS[iteration_key]:
            post_dict[str(i+1)] = True
        else:
            post_dict[str(i+1)] = False

    # They've filled everything out, so lets send off the form dict to C++ for cookin
    # run("cpp/main.cpp");
    statsFile = open("cpp/statsfile.txt", "r")
    statsList = statsFile.readlines()
    # statsFormatted = "<h1>Answers:</h1>"
    # for i in range(len(stats)):
    #    if i % 2 == 0:
    #        statsFormatted += "<h2>" + stats[i] + "</h2>"
    #    else:
    #        statsFormatted += "<p>" + stats[i] + "</p>"
    return render_template('results.html', stats = statsList, len = len(statsList))
    # return '<h1>Answers: <u>'+str(post_dict)+'</u></h1>'

if __name__ == '__main__':
    app.run(debug=True)