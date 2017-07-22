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
        self.question = ques.readquestion()
        self.quest = ques

    # call each matrix type according to the matching regex.
    def grading(self):
        if re.search("[0-9]?[A-Z][-|+][0-9]?[A-Z]", self.question['ques']):  # check for 2A-B type question
            self.logger.info('Type : Matrix addition/subtraction')
            type2 = Type2(self.question, self.scheme, self.answer_file, self.logger)
            type2.markAns()
        elif re.search("[0-9][A-Z]", self.question['ques']):  # check for 2A type question
            self.logger.info('Type : numeric multiplication of matrix')
            type1 = Type1(self.question, self.scheme, self.answer_file, self.logger)
            type1.markAns()
        elif re.search("[a-z][a-z]?", self.question['ques']):  # check for finding unknown variables type question
            self.logger.info('Type : finding unknown variables')
            type3 = Type3(self.question, self.scheme, self.answer_file, self.logger)
            type3.markAns()
        elif re.search("[A-Z]", self.question['ques']):  # check for finding matrix type question
            self.logger.info('Type : finding unknown matrix')
            type4 = Type4(self.question, self.quest.col_size, self.quest.row_size, self.scheme, self.answer_file, self.logger)
            type4.markAns()




