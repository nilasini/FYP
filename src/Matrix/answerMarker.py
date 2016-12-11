from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re
from type2 import Type2
from type3 import Type3
from type1 import Type1
from type4 import Type4

class Answer(Logs):

    def __init__(self, ques, scheme, answer_file, logger):
        self.scheme = scheme
        self.answer_file = answer_file
        self.logger = logger
        self.question = ques.readQuestion()
        self.quest = ques


    def grading(self):
        if re.search("[0-9]?[A-Z]?[-][0-9]?[A-Z]", self.question['ques']):
            type2 = Type2(self.question, self.scheme, self.answer_file, self.logger)
            type2.markAns()
        elif re.search("[0-9][A-Z]", self.question['ques']):
            print('it contains 2A type formula')
            type1 = Type1(self.question, self.scheme, self.answer_file, self.logger)
            type1.markAns()
        elif re.search("[a-z][a-z]?", self.question['ques']):
            print('it contains variables within a matrix')
            type3 = Type3(self.question, self.scheme, self.answer_file, self.logger)
            type3.markAns()
        elif re.search("[A-Z]", self.question['ques']):
            print('it contains only a matrix')
            type4 = Type4(self.quest, self.scheme, self.answer_file, self.logger)
            type4.markAns()



