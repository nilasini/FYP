from logger_details import Logs
from scheme import Scheme
from answerMarker import Answer
from question import Question


import time
from threading import Thread

class Tutor(Thread):
    logs = Logs()
    question = Question('./Files/questions/type1/sampleQ1.html', logs.logger)

    scheme = Scheme('./Files/schemes/type1/sampleQ1_S.html', logs.logger)
    scheme_parsed = scheme.readScheme()

    answer = Answer(question, scheme_parsed, './Files/answers/type1/sampleA1_1.html', logs.logger)
    time.sleep(0.1)
    # read and mark the answer file
    answer.markAns()
