from logger_details import Logs
# from question import Question
from scheme import Scheme
from answerMarker import Answer
from ques_type4 import Question
# from Question import Question

import time
from threading import Thread


class Tutor(Thread):
    #def evaluateAnswer(studentAnswer, question, markingScheme) :
    logs = Logs()
    # initiate the Question
    question = Question('./Files/questions/Type4/sampleQ1.html', logs.logger)  # initiate the Scheme
    scheme = Scheme('./Files/schemes/Type4/sampleQ1_S.html', logs.logger)
    # parse the scheme
    scheme_parsed = scheme.readScheme()
    time.sleep(0.1)
    # read the answer
    answer = Answer(question, scheme_parsed, './Files/answers/Type4/sampleA1_1.html', logs.logger)
    # mark the answer file
    answer.grading()



