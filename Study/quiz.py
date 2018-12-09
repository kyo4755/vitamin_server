from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import Quiz
from random import *
import json


@app.route("/study/getQuiz", methods=['POST'])
def get_quiz():
    session = db_session()
    return_msg = {'result': '0000'}

    if request.method == 'POST':
        index = request.form['index']

        totalCount = session.query(Quiz.index).count()

        if index is None or len(index) == 0:
            index = randint(1, totalCount)
            nonQuery = session.query(Quiz).filter(Quiz.index == index).first()
            return_msg['index'] = nonQuery.index
            return_msg['question'] = nonQuery.question
            return_msg['num1'] = nonQuery.numOne
            return_msg['num2'] = nonQuery.numTwo
            return_msg['num3'] = nonQuery.numThree
            return_msg['num4'] = nonQuery.numFour
            return_msg['answer'] = nonQuery.answer
            return_msg['isEnd'] = 0

        else:
            indexSplit = index.split('||')
            counting = 0
            while True:
                counting = counting + 1

                if counting == totalCount:
                    return_msg['example'] = {
                        'isEnd': 1
                    }
                    break

                index = randint(1, totalCount)

                if str(index) in indexSplit:
                    continue
                else:
                    inQuery = session.query(Quiz).filter(Quiz.index == index).first()
                    return_msg['index'] = inQuery.index
                    return_msg['question'] = inQuery.question
                    return_msg['num1'] = inQuery.numOne
                    return_msg['num2'] = inQuery.numTwo
                    return_msg['num3'] = inQuery.numThree
                    return_msg['num4'] = inQuery.numFour
                    return_msg['answer'] = inQuery.answer
                    return_msg['isEnd'] = 0

                    break

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/study/setQuiz", methods=['POST'])
def set_quiz():
    session = db_session()
    return_msg = {'result': '0000'}
    is_add_to_db = True

    if request.method == 'POST':
        question = request.form['question']
        if question is None or len(question) == 0:
            return_msg['result'] = '0001'
            is_add_to_db = False

        numOne = request.form['numOne']
        if numOne is None or len(numOne) == 0:
            return_msg['result'] = '0002'
            is_add_to_db = False

        numTwo = request.form['numTwo']
        if numTwo is None or len(numTwo) == 0:
            return_msg['result'] = '0003'
            is_add_to_db = False

        numThree = request.form['numThree']
        if numThree is None or len(numThree) == 0:
            return_msg['result'] = '0004'
            is_add_to_db = False

        numFour = request.form['numFour']
        if numFour is None or len(numFour) == 0:
            return_msg['result'] = '0005'
            is_add_to_db = False

        answer = request.form['answer']
        if answer is None or len(answer) == 0:
            return_msg['result'] = '0006'
            is_add_to_db = False

        if is_add_to_db:
            t = Quiz(question, numOne, numTwo, numThree, numFour, answer)
            session.add(t)

            session.commit()
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string
