from logger_details import Logs
# from question import Question
from scheme import Scheme
from answerMarker import Answer
from question import Question


class Tutor:
    logs = Logs()
    question = Question('./Files/questions/Type2/sampleQ2.html', logs.logger)
    #ques = question.readQuestion()

    scheme = Scheme('./Files/schemes/Type2/sampleQ2_S.html', logs.logger)
    scheme_parsed = scheme.readScheme()

    answer = Answer(question, scheme_parsed, './Files/wrong answers/Type2/sampleA2_1.html', logs.logger)
    # read and mark the answer file
    answer.grading()




