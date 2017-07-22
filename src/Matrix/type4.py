from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
from ques_type4 import *
import re
import time
from threading import Thread
import operator
import json


class Type4(Logs):

    def __init__(self, ques, col_size, row_size, scheme, answer_file, logger):
        self.scheme = scheme
        self.answer_file = answer_file
        self.logger = logger
        self.question = ques
        self.col_size = col_size
        self.row_size = row_size

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
        gotDivisionMark = False
        gotSubsMark = False
        middlesubs = False
        operator = None
        error_Identification = []
        concept = []
        step = 0
        errStep = 0
        dataArray = []

        self.logger.info('Reading answers')
        # open the answer file
        with open(self.answer_file) as answer:
            marks = 0
            isContainVariable = False
            #rearrange the question
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
                oneStepFinished = false
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
                    oneStepFinished = true
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
                        if not operator:
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size) and not gotSubsMark:
                                # print('your mark for subtraction ', self.scheme['subtraction'])
                                dataArray.append({"concept": "subtraction", "details": "Correct",
                                                  "marksAwarded": self.scheme['subtraction'], "step": step,
                                                  "totalMarks": self.scheme['subtraction']})
                                marks += 1
                                gotSubsMark = true
                    else:
                        subs_matrix = res - Matrix(list)
                        if subs_matrix == zeros(row_size, col_size):
                            if gotSubsMark and not gotDivisionMark:
                                # print('your mark for division is ', self.scheme['division'])
                                dataArray.append({"concept": "division", "details": "Correct",
                                                  "marksAwarded": self.scheme['division'], "step": step,
                                                  "totalMarks": self.scheme['division']})
                                marks += 1
                                gotDivisionMark = true
                            # elif not gotSubsMark and not gotDivisionMark:
                            #     print('your mark is ', self.scheme['totalmarks'])

                elif list :
                    subs_matrix = res - Matrix(list)
                    if subs_matrix == zeros(row_size, col_size) and not gotSubsMark and not gotDivisionMark:
                        # print('your mark is ', self.scheme['totalmarks'])
                        marks += 1
                if oneStepFinished:
                    list.clear()
                    mtrilist.clear()
                    isfoundrow = true
                    matri_name.clear()
                    siz = 0
                    count = 0
                    operator = None
                    multiplied = False
                    middlesubs = False
                i += 1
            if not dataArray:
                data = {"studentTotal": marks, "errStep":errStep, "maxMarks":self.scheme['totalmarks'], "error_identification":error_Identification}
            elif not error_Identification:
                data = {"studentTotal": marks, "maxMarks":self.scheme['totalmarks'], "concepts":dataArray}
            else:
                data = {"studentTotal": marks, "errStep":errStep, "maxMarks":self.scheme['totalmarks'], "concepts":dataArray, "error_identification":error_Identification}

            print(json.dumps(data))
            # print('your final marks is ', marks, 'out of ', self.scheme['totalmarks'])
        time.sleep(0.1)
        self.logger.info('Finish answer reading')



