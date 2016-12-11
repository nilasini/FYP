from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
from xxx import *
import re
import operator


class Type4(Logs):

    def __init__(self, ques, scheme, answer_file, logger):
        self.scheme = scheme
        self.answer_file = answer_file
        self.logger = logger
        self.question = ques.readQuestion()
        self.col_size = ques.col_size
        self.row_size = ques.row_size


    def markAns(self):
        isfound = true
        isfoundrow = true
        mtrilist = []
        matri_name = []
        list = []
        siz = 0
        count = 0
        ispassfenced = false
        iscontain_equals = false
        old_ans_matrix = None
        ans_matrix = None
        rightside_constant = None
        iscontain_var = None
        # check whether the step is already multiplied by the system
        multiplied = False
        gotMultipliedMark = False
        gotSubsMark = False
        gotFinalStepMark = False
        # check whether middle minus there
        middlesubs = False
        equation = ''
        ops = {"+": operator.add, "-": operator.sub}
        self.logger.info('Reading answers')
        # open the answer file
        with open(self.answer_file) as answer:
            i = 0
            k = 0
            marks = 0
            isContainVariable = False
            # parse the answer file
            size = len(self.question['left_var'])
            print('size is ',len(self.question['left_var']))
            if size > 1:
                print()
            else:
                J = MatrixSymbol('J', self.row_size, self.col_size)
                if self.question['operator_left']=='+':
                    result = self.question['left_var'].pop() + self.question['left']
                    print(result)
            if self.question['left_var']:
                L = self.question['left']
                K = self.question['right']

                # equation = str(L) + self.question['left_var'].pop() + self.question['left_var'].pop() + '=' + str(K)
                # print('equation is ', equation)
                # print('m', )


            # for line in answer:
            #     ans_soup = BeautifulSoup(line, "html.parser")
            #     if 'mi' in line and 'mtd' not in line and not ispassfenced:
            #         temp = ans_soup.text
            #         matri_name.insert(0, temp)
            #         count += 1
            #     if 'mfenced' in line:
            #         count = 0
            #         ispassfenced = true
            #     if '/mfenced' in line:
            #         ispassfenced = false
            #         rightside_constant = None
            #     if 'mn' in line and 'mtd' in line:
            #         mtrilist.insert(i, ans_soup.text)
            #     if '/mtr' in line and isfound:
            #         col_size = len(mtrilist)
            #         isfound = false
            #     if '/mtable' in line:
            #         if isfoundrow:
            #             siz += len(mtrilist)
            #             row_size = int(siz / col_size)
            #             isfoundrow = false
            #     if 'mspace' in line:
            #         list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
            #
            #     iscontainplus = false
            #     iscontainminus = false
            #     noVarInLeft = false
            #
            #     if ((matri_name and list) or list):
            #         matrix_question = self.question['ques']








