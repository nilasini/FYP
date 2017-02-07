from logger_details import Logs
# from question import Question
from scheme import Scheme
from answerMarker import Answer
from question import Question


class Tutor:
    logs = Logs()
    #read the question
    question = Question('./Files/questions/Type3/sampleQ1.html', logs.logger)

    #read the scheme and parse it
    scheme = Scheme('./Files/schemes/Type3/sampleQ1_S.html', logs.logger)
    scheme_parsed = scheme.readScheme()

    #read the answer
    answer = Answer(question, scheme_parsed, './Files/answers/Type3/sampleA1_3.html', logs.logger)
    #mark the answer file
    answer.grading()




