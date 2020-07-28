# pip install pyswip
from pyswip import Prolog, Functor, Variable, Query

# from databaseinteractions import GetQuestionAndOptions, GetAnswer

'''
This function queries the prolog database and returns both a question and its options
'''
def GetQuestionAndOptions(questionNumber, databasePath="data/database.pl"):

    prolog = Prolog()
    # Consult database
    prolog.consult(databasePath)

    question = Functor("question", 2)
    options = Functor("options", 4)
    out1 = Variable()
    out2 = Variable()
    out3 = Variable()

    questionOut = ""
    optionsOut = []

    query = Query(question(questionNumber, out1))
    while(query.nextSolution()):
        questionOut = str(out1.value)
    query.closeQuery()

    query = Query(options(questionNumber, out1, out2, out3))
    while(query.nextSolution()):
        optionsOut = [str(out1.value), str(out2.value), str(out3.value)]
    query.closeQuery()

    return [questionOut, optionsOut] # ['What color is the sky', ['Blue', 'Red', 'Green']]

'''
This function returns the one-letter answer to the question number provided to its argument
'''
def GetAnswer(questionNumber, databasePath="data/database.pl"):
    prolog = Prolog()
    # Consult database
    prolog.consult(databasePath)

    answer = Functor("answer", 2)
    out1 = Variable()

    returnValue = ""
    query = Query(answer(questionNumber, out1))
    if(query.nextSolution()):
        returnValue = str(out1.value)
    query.closeQuery()
    return returnValue

'''
This funtion prints all question and answer information in the prolog database to the console.
'''
def PrintAllInformation(databasePath="data/database.pl"):
    prolog = Prolog()
    # Consult database
    prolog.consult(databasePath)

    question = Functor("question", 2)
    options = Functor("options", 4)
    answer = Functor("answer", 2)
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
    for i in range(0,len(questionsOut)):
        print(questionsOut[i],"\n")
        for option in optionsOut[i]:
            print("\t", option,"\n")


def main():
    print(GetQuestionAndOptions(1))
    print(GetAnswer(1))
    # PrintAllInformation()

if __name__ == '__main__':
    main()
