# pip install pyswip
from pyswip import Prolog, Functor, Variable, Query

'''
This function should be called once on program startup, to initialize variables used across
other library functions.
'''
def InitializeProlog(databasePath = "data/database.pl"):
    # Create prolog object for consulting database
    prolog = Prolog()
    # Consult database
    prolog.consult(databasePath)

    # Prepare statement names
    question = Functor("question", 2)
    options = Functor("options", 4)
    answer = Functor("answer", 2)

    # Set up output variables for Prolog
    out1 = Variable()
    out2 = Variable()
    out3 = Variable()
    Y = Variable()

'''
This function queries the prolog database and returns both a question and its options
'''
def GetQuestionAndOptions(questionNumber):
    question = ""
    options = []

    query = Query(question(questionNumber, out1))
    if(query.nextSolution()):
        question = out1.value
    query.closeQuery()

    query = Query(options(questionNumber, out1, out2, out3))
    if(query.nextSolution()):
        options = [out1.value, out2.value, out3.value]
    query.closeQuery()

    return [question, options] # ['What color is the sky', ['Blue', 'Red', 'Green']]

'''
This function returns the one-letter answer to the question number provided to its argument
'''
def GetAnswer(questionNumber):
    returnValue = ""
    query = Query(answer(number, out1))
    if(query.nextSolution()):
        returnValue = out1.value
    query.closeQuery()
    return returnValue

'''
This funtion prints all question and answer information in the prolog database to the console.
'''
def PrintAllInformation():
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
    for i in range(0,len(questionsOut)):
        print(questionsOut[i],"\n")
        for option in optionsOut[i]:
            print("\t", option,"\n")
