
# def print_return(n):
#     print('returned from js: ', n)

# @eel.expose
# def py_what_yr():
#     import datetime
#     return "the year is " + str(datetime.datetime.now().year)

# # Example of python function callable by js
# # @eel.expose
# # def my_python_method(p1, p2):
# #     print(p1, p2)

# # example of js function callable in python; function defined in main.html
# eel.my_js_function('Hello ', 'JS World')

# # example of using a callback from the js function to do something in python
# eel.js_what_yr()(print_return)
import eel, random

@eel.expose
def start_quiz():
    eel.start('trial_site.html', block=True, mode='chrome-app')

# Create Questions
questions = {
 'Taj Mahal':['Agra','New Delhi','Mumbai','Chennai'],
 'Great Wall of China':['China','Beijing','Shanghai','Tianjin'],
 'Petra':['Ma\'an Governorate','Amman','Zarqa','Jerash']
}

# Shuffle Question order for fun; NOTE: probs should do manually
keys = list(questions.keys())
random.shuffle(keys)




eel.init('../javascript')
eel.start('site.html', block=True, mode='chrome-app')
