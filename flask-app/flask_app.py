from flask import Flask, render_template, request
import datetime

from prolog.databaseinteractions import GetQuestionAndOptions, GetAnswer


app = Flask(__name__)

PROLOG_PATH = 'prolog/data/database.pl'

# Global dict generated from Prolog database
Q_A_PAIRS = {}
for question in range(1, 4):
    prolog_data = GetQuestionAndOptions(question, PROLOG_PATH)
    Q_A_PAIRS[prolog_data[0]] = prolog_data[1]


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
    "return" Q_A_PAIRS: our question and answers dict. The html form will generate
                        the quiz by iterating through the keys and supplying the
                        answers based on the dict's value at each key. see lines
                        4 and 6 in quiz.html
    '''
    key_list = list(Q_A_PAIRS.keys())

    # psuedo randomize the key value pairs using modulu time
    for key in Q_A_PAIRS.keys():
        pos = key_list.index(key) if key_list.index(key) else 1
        new_pos = datetime.datetime.now().second % pos

        if new_pos > len(key_list):
            new_pos = len(key_list) - 1

        key_list.insert(new_pos, key_list.pop(key_list.index(key)))

    return render_template('quiz.html', questions=key_list, answer_options=Q_A_PAIRS)


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
    if len(request.form.to_dict()) != len(Q_A_PAIRS):
        return '<a href="http://127.0.0.1:5000/quiz"><h1>Please try again. Not all questions answered</h1></a>'

    post_dict = {}
    key_list = list(Q_A_PAIRS.keys())
    user_answers_dict = request.form.to_dict()
    prolog_answer_key = {'A':0, 'B':1, 'C':2}

    for i in range(len(Q_A_PAIRS)):
        prolog_ans_letter = GetAnswer(i+1, PROLOG_PATH)
        correct_answer = Q_A_PAIRS[key_list[i+1]][prolog_answer_key[prolog_ans_letter]]
        ''' NOTE(s):
        -Sam's database starts at 1 instead of 0 because "question 1"
        -accessing user_answers_dict in this janky way cause of prolog and sam's
            current GetAnswers()
        -need to index q_a_pairs with the correct key at the correct position
            in order to string compare
        '''
        # Save the q number as the key and True if they answered correctly
        if user_answers_dict[key_list[i+1]] == correct_answer:
            post_dict[i+1] = True
        else:
            post_dict[i+1] = False

    # They've filled everything out, so lets send off the form dict to C++ for cookin
    return '<h1>Answers: <u>'+str(post_dict)+'</u></h1>'

if __name__ == '__main__':
    app.run(debug=True)