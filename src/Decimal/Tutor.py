from logger_details import Logs
# from question import Question
from scheme import Scheme
from answerMarker import Answer
from question import Question


class Tutor:
    logs = Logs()
    question = Question('./Files/questions/sampleQ1.html', logs.logger)

    scheme = Scheme('./Files/schemes/sampleQ1_S.html', logs.logger)
    scheme_parsed = scheme.readScheme()

    answer = Answer(question, scheme_parsed, './Files/answers/sampleA1_1.html', logs.logger)
    # read and mark the answer file
    answer.markAns()
