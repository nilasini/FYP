from logger_details import Logs
# from question import Question
from scheme import Scheme
from answerMarker import Answer
from xxx import Question


class Tutor:
    logs = Logs()
    question = Question('./Files/questions/Type4/sampleQ1.html', logs.logger)
    #ques = question.readQuestion()

    scheme = Scheme('./Files/schemes/Type3/sampleQ1_S.html', logs.logger)
    scheme_parsed = scheme.readScheme()

    answer = Answer(question, scheme_parsed, './Files/answers/Type3/sampleA1_1.html', logs.logger)
    # read and mark the answer file
    answer.grading()


