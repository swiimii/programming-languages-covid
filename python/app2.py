from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

# NOTE: do not include number in question name since we're going to shuffle lol
q_a_pairs = {'1: ' : ['a1', 'a2', 'a3', 'a4'],
             '2: ' : ['a1', 'a2', 'a3', 'a4'],
             '3: ' : ['a1', 'a2', 'a3', 'a4']}

@app.route('/')
def home():
    return render_template('trial_site.html')


@app.route('/quiz')
def quiz():
    key_list = list(q_a_pairs.keys())

    # psuedo randomize the key value pairs using modulu time
    for key in q_a_pairs.keys():
        pos = key_list.index(key) if key_list.index(key) else 1
        new_pos = datetime.datetime.now().second % pos

        if new_pos > len(key_list):
            new_pos = len(key_list) - 1

        key_list.insert(new_pos, key_list.pop(key_list.index(key)))

    return render_template('main.html', questions=key_list, answer_options=q_a_pairs)


@app.route('/quiz', methods=['POST'])
def quiz_answers():
    # NOTE: request.form just gets the info filled out; doesn't disallow not answering
    if len(request.form.to_dict()) != len(q_a_pairs):
        return '<a href="http://127.0.0.1:5000/quiz"><h1>Please try again. Not all questions answered</h1></a>'
    # They've filled everything out, so lets send off the form dict to C++ for cookin
    return '<h1>Answers: <u>'+str(request.form.to_dict())+'</u></h1>'

if __name__ == '__main__':
    app.run(debug=True)