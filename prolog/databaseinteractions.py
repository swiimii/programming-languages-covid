# pip install pyswip
from pyswip import Prolog, Functor, Variable, Query

# Create prolog object for consulting database
prolog = Prolog()
# Consult database
prolog.consult("data/database.pl")

# Prepare statement names
question = Functor("question", 2)
options = Functor("options", 4)
answer = Functor("answer", 2)

# Set up output variables for Prolog
out1 = Variable()
out2 = Variable()
out3 = Variable()
Y = Variable()

# Gather all the questions into a list
questionsOut = []
query = Query(question(Y, out1))
while query.nextSolution():
    questionsOut.append(out1.value)
query.closeQuery()

# Gather all the options into a list
optionsOut = []
query = Query(options(Y, out1, out2, out3))
while query.nextSolution():
    optionsOut.append([out1.value, out2.value, out3.value])
query.closeQuery()

# Gather all the answers into a list
answersOut = []
query = Query(answer(Y, out1))
while query.nextSolution():
    answersOut.append(out1.value)
query.closeQuery()

#interact with data
for i in range(0,3):
    print(questionsOut[i],"\n")
    for option in optionsOut[i]:
        print("\t", option,"\n")
