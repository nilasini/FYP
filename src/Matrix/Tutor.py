from logger_details import Logs
from question import Question
from answer import Answer


class Tutor:
    logs = Logs()
    question = Question('./Files/questions/Type2/SampleQ1.html', logs.logger)
    #read the question file
    ques = question.readQuestion()
    answer = Answer('./Files/schemes/Type2/sampleQ1_S.html', './Files/answers/Type2/sampleA1_1.html', ques, logs.logger)
    #read and mark the answer file
    answer.markAnswer()

