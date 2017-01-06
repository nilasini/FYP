from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
from queue import *

class Question(Logs):

    def __init__(self, question_file, logger):
        self.question_file = question_file
        self.logger = logger

    def readQuestion(self):
        ques_list = Queue(maxsize=0)
        count = 0
        question = ''
        # open the question file
        filein = open(self.question_file)
        self.logger.info('Reading question')

        # parse the question
        for line in filein:
            soup = BeautifulSoup(line, "html.parser")
            if 'mn' in line or 'mo' in line:
                temp = soup.text
                ques_list.put(temp)
                count += 1

            if '/math' in line:
                for d in range(0, ques_list.qsize()):
                    question += ques_list.get().strip()

        self.logger.info('Finish question reading')
        return question