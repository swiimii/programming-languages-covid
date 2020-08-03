from pyswip import Prolog, Functor, Variable, Query


def getDBInfo(questionNumber):
    ''' This function queries the prolog database and returns database info
    on passed in question number

    @param questionNumber: int of the question number in the .pl file. starts @ 1

    returns list of:
                    -element1: str of question
                    -element2: list of strs containing question options
                    -element3: str of correct answer
    '''
    # NOTE: int arg is for how many args are to the right of the db obj
    answer = Functor("answer", 2)
    question = Functor("question", 2)
    options = Functor("options", 4)

    # Declare all variables we're going to use to store prolog info
    out1 = Variable()
    out2 = Variable()
    out3 = Variable()

    # Set default values for containing str version of query return
    questionOut = ""
    optionsOut = []
    answerOut = ""

    # Find corresponding question to questionNumber passed in
    query = Query(question(questionNumber, out1))
    while(query.nextSolution()):
        questionOut = str(out1.value)
    query.closeQuery()

    # Find corresponding question options to questionNumber passed in
    query = Query(options(questionNumber, out1, out2, out3))
    while(query.nextSolution()):
        optionsOut = [str(out1.value), str(out2.value), str(out3.value)]
    query.closeQuery()

    # Find corresponding answer to questionNumber passed in
    query = Query(answer(questionNumber, out1))
    while(query.nextSolution()):
        answerOut = str(out1.value)
    query.closeQuery()

    # Follows format: ['What color is the sky', ['Blue', 'Red', 'Green'], answer]
    return [questionOut, optionsOut, answerOut]


def main():
    PROLOG_PATH = 'data/database.pl'
    PROLOG_OBJ = Prolog()
    PROLOG_OBJ.consult(PROLOG_PATH)
    print(getDBInfo(1))

if __name__ == '__main__':
    main()
