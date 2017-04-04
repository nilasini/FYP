from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
from queue import *

class Question(Logs):

    def __init__(self, question_file, logger):
        self.question_file = question_file
        self.logger = logger

    def readquestion(self):
        ques_list = Queue(maxsize=0)
        count = 0
        question = ''
        issqrt = false
        sqrt_list = []
        # open the question file
        filein = open(self.question_file)
        self.logger.info('Reading question')

        # parse the question
        for line in filein:
            soup = BeautifulSoup(line, "html.parser")
            # if 'msqrt' in line and '/msqrt' not in line:
            # #     issqrt = true
            # if 'mn' in line:

            if 'mn' in line and issqrt:
                sqrt_list.insert(0, int(soup.text.strip()))
            if '/msqrt' in line:
                issqrt = false
                # print('jsckjsbv ',sqrt(int(sqrt_list.pop())))
                ques_list.put(sqrt(sqrt_list.pop()))
            if 'mo' in line:
                ques_list.put(soup.text.strip())
            if '/math' in line:
                for d in range(0, ques_list.qsize()):
                    question += str(ques_list.get())

        self.logger.info('Finish question reading')
        print('question is ',question)
        return question