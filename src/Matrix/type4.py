from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
from ques_type4 import *
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
        isfoundcol = true
        isfoundrow = true
        mtrilist = []
        matri_name = []
        list = []
        siz = 0
        count = 0
        ispassfenced = false
        ans_matrix = None
        rightside_constant = None
        # check whether the step is already multiplied by the system if 2 is there system will multiply and do the rest
        multiplied = False
        gotMultipliedMark = False
        gotSubsMark = False
        gotFinalStepMark = False
        # check whether middle minus there
        middlesubs = False
        operator = None

        self.logger.info('Reading answers')
        # open the answer file
        with open(self.answer_file) as answer:
            marks = 0
            isContainVariable = False
            # parse the answer file
            # size = len(self.question['left_var'])
            # if size > 1:
            #     var1 = self.question['left_var'].pop().strip()
            #     var2 = self.question['left_var'].pop().strip()
            #     Ques_var = self.question['ques']
            #     Ques_var = MatrixSymbol('Ques_var', self.row_size, self.col_size)
            #     if self.question['ques'] not in var1:
            #         variab1 = var1
            #         variab2 = var2
            #     else:
            #         variab1 = var2
            #         variab2 = var1
            #     value = None
            #     if self.question['operator_left'] == '+':
            #         if len(variab2) > 1:
            #             value = variab2[0:1]
            #         variab1 = MatrixSymbol('variab1', self.row_size, self.col_size)
            #         if value:
            #             result = (int(value)*Matrix(Ques_var)+Matrix(variab1) - self.question['right']).xreplace({variab1:Ques_var})
            #         else:
            #             result = (Matrix(Ques_var) + Matrix(variab1) - self.question['right']).xreplace({variab1: Ques_var})
            #         res = solve(result, Matrix(Ques_var))
            #         tt = Matrix(Ques_var).xreplace(res)
            # #     print('reskkkkkk', res)
            # #     elif self.question['operator_left'] == '-':
            # #         if re.search(r'\d', variab):
            # #             Ques_var = self.question['ques']
            # #             Ques_var = MatrixSymbol('Ques_var', self.row_size, self.col_size)
            # #             ans_matrix = int(variab[0:1]) * Matrix(Ques_var)
            # #         result = solve(ans_matrix - self.question['left'] - self.question['right'], Matrix(Ques_var))
            # #         res = Matrix(Ques_var).xreplace(result)
            # #         print('reskkkkkk', res)
            # #     print()
            # else:
            var=self.question['left_var'].pop().strip()
            if self.question['operator_left'] == '+':
                if re.search(r'\d', var):
                    Ques_var = self.question['ques']
                    Ques_var = MatrixSymbol('Ques_var', self.row_size, self.col_size)
                    ans_matrix = int(var[0:1]) * Matrix(Ques_var)
                result = solve(ans_matrix + self.question['left']-self.question['right'], Matrix(Ques_var))
                res = Matrix(Ques_var).xreplace(result)
            elif self.question['operator_left'] == '-':
                if re.search(r'\d', var):
                    Ques_var = self.question['ques']
                    Ques_var = MatrixSymbol('Ques_var', self.row_size, self.col_size)
                    ans_matrix = int(var[0:1]) * Matrix(Ques_var)
                result = solve(ans_matrix - self.question['left'] - self.question['right'], Matrix(Ques_var))
                res = Matrix(Ques_var).xreplace(result)
                self.logger.info('Reading answers')
            i = 0
            # parse the answer file
            for line in answer:
                ans_soup = BeautifulSoup(line, "html.parser")
                if 'mi' in line and 'mtd' not in line and not ispassfenced:
                    temp = ans_soup.text
                    matri_name.insert(i, temp)
                    count += 1
                if 'mfenced' in line and '/mfenced' not in line:
                    count = 0
                    ispassfenced = true
                if '/mfenced' in line:
                    ispassfenced = false
                    rightside_constant = None
                if 'mn' in line and 'mtd' in line:
                    if rightside_constant:
                        s_text = int(rightside_constant) * int(ans_soup.text)
                        mtrilist.insert(i, str(s_text))
                        multiplied = True
                    else:
                        mtrilist.insert(i, ans_soup.text)
                if 'mn' in line and 'mtd' not in line:
                    rightside_constant = ans_soup.text
                if '/mtr' in line and isfoundcol:
                    col_size = len(mtrilist)
                    isfoundcol = false
                if '/mo' in line and count > 0:
                    if '=' not in ans_soup.text:
                        matri_name.insert(0, ans_soup.text)
                if '/mo' in line and count == 0:
                    if ans_soup.text == '=':
                        # student use = for each step starting instead of LHS
                        iscontain_equals = ans_soup.text
                    else:
                        operator = ans_soup.text
                if '/mtable' in line:
                    if isfoundrow:
                        siz += len(mtrilist)
                        row_size = int(siz / col_size)
                        isfoundrow = false
                if 'mspace' in line:
                    list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                    for elements in list:
                        for element in elements:
                            if re.search("\d[-]\d", element):
                                middlesubs = True

                iscontainplus = false
                iscontainminus = false
                isTwoMatrixInvolved = false
                if list and matri_name:
                    length = len(matri_name)
                    matrix_leftside = matri_name.pop().strip()
                    if re.search(r'\d', matrix_leftside):
                        ans_matrix = int(matrix_leftside[0:1]) * res
                        subs_matrix = ans_matrix - Matrix(list)
                        if subs_matrix == zeros(row_size, col_size):
                            print('your mark for substitution ')
                            marks += 1
                    else:
                        subs_matrix = res - Matrix(list)
                        if subs_matrix == zeros(row_size, col_size):
                            print('your mark for substitution ')
                            marks += 1
                        list.clear()
                        mtrilist.clear()
                        isfoundrow = true
                        matri_name.clear()
                        siz = 0
                        count = 0
                        multiplied = False
                        middlesubs = False
                elif list:
                    subs_matrix = res - Matrix(list)
                    if subs_matrix == zeros(row_size, col_size):
                        print('your mark for substitution ')
                        marks += 1
                    list.clear()
                    mtrilist.clear()
                    isfoundrow = true
                    matri_name.clear()
                    siz = 0
                    count = 0
                    multiplied = False
                    middlesubs = False
                i += 1
            print('your final marks is ', marks)





