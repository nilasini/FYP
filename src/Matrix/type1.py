from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re
import time
from threading import Thread


class Type1(Logs, Thread):
    col_size = None
    row_size = None

    def __init__(self, ques, scheme, answer_file, logger):
        self.scheme = scheme
        self.answer_file = answer_file
        self.logger = logger
        self.question = ques

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
        isfinished = false

        self.logger.info('Reading answers')
        with open(self.answer_file) as answer:
            i = 0
            marks = 0
            # parse the answer file
            for line in answer:
                oneStepFinished = false
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
                        #student use = for each step starting instead of LHS
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
                    matrix_leftside = ''
                    # more than one matrix involved
                    if length > 2:
                        isTwoMatrixInvolved = true
                    else:
                        matrix_leftside = matri_name.pop().strip()
                        withoutcons_ans_matrix = self.question[matrix_leftside[1:2]]
                        if re.search(r'\d', matrix_leftside):
                            ans_matrix = int(matrix_leftside[0:1]) * self.question[matrix_leftside[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                if not multiplied and not gotMultipliedMark:
                                    print('your mark for multiplication ', self.scheme['multiplication'])
                                    gotMultipliedMark = True
                                    marks += 1
                                else:
                                    if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                        print('your mark for multiplication ', self.scheme['multiplication'])
                                        gotMultipliedMark = True
                                        marks += 1
                                list.clear()
                                mtrilist.clear()
                                isfoundrow = true
                                matri_name.clear()
                                siz = 0
                                count = 0
                                multiplied = False
                                middlesubs = False
                            else:
                                numofcrctmuliplication = 0
                                # check for multiplication only first row by the constant
                                for k in range(self.question[matrix_leftside[1:2]].shape[0]):
                                    if k == 0:
                                        l1 = int(matrix_leftside[0:1]) * self.question[matrix_leftside[1:2]].row(k)
                                    else:
                                        l2 = self.question[matrix_leftside[1:2]].row(k)
                                    if k == 0 and l1 == Matrix(list).row(0):
                                        numofcrctmuliplication += 1
                                    elif k != 0 and l2 == Matrix(list).row(k):
                                        numofcrctmuliplication += 1
                                if numofcrctmuliplication == self.question[matrix_leftside[1:2]].shape[0]:
                                    print('you have multiplied only first row by constant when calculating ',
                                          matrix_leftside)
                                    break
                                if (withoutcons_ans_matrix - Matrix(list)) == zeros(row_size, col_size):
                                    print('you have forgotten to muliply by the constant ', matrix_leftside[0:1])
                                    break
                                if multiplied:
                                    print('you have made mistake in substitution of ', matrix_leftside[1:2])
                                    break
                                if not multiplied:
                                    print('you have made mistake in multiplication in calculation of ', matrix_leftside)
                                    break
                                if middlesubs:
                                    print('you have made mistake in substitution of ', matrix_leftside[1:2])
                                    break
                elif list:
                        matrix_question = self.question['ques']
                        if re.search(r'\d', matrix_question):
                            withoutcons_ans_matrix = self.question[matrix_question[1:2]]
                            ans_matrix = int(matrix_question[0:1]) * self.question[matrix_question[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                # self.logger.info('your step is correct')
                                if not multiplied and not gotMultipliedMark:
                                    print('your mark for multiplication ', self.scheme['multiplication'])
                                    gotMultipliedMark = True
                                    marks += 1
                            else:
                                numofcrctmuliplication = 0
                                # check for multiplication only first row by the constant
                                for k in range(self.question[matrix_question[1:2]].shape[0]):
                                    if k == 0:
                                        l1 = int(matrix_question[0:1]) * self.question[matrix_question[1:2]].row(k)
                                    else:
                                        l2 = self.question[matrix_question[1:2]].row(k)
                                    if k == 0 and l1 == Matrix(list).row(0):
                                        numofcrctmuliplication += 1
                                    elif k != 0 and l2 == Matrix(list).row(k):
                                        numofcrctmuliplication += 1
                                if numofcrctmuliplication == self.question[matrix_question[1:2]].shape[0]:
                                    print('you have multiplied only first row by constant when calculating ',
                                          matrix_question)
                                    break
                                if (withoutcons_ans_matrix - Matrix(list)) == zeros(row_size, col_size):
                                    print('you have forgotten to muliply by the constant ', matrix_question[0:1])
                                    break
                                if multiplied:
                                    print('you have made mistake in substitution of ', matrix_question[1:2])
                                    break
                                if not multiplied:
                                    print('you have made mistake in multiplication in calculation of ', matrix_question)
                                    break
                                if middlesubs:
                                    print('you have made mistake in substitution of ', matrix_question[1:2])
                                    break

                if oneStepFinished:
                    list.clear()
                    mtrilist.clear()
                    isfoundrow = true
                    matri_name.clear()
                    siz = 0
                    count = 0
                    multiplied = False
                    middlesubs = False
                    operator = None
                i += 1
            print('your final marks is ', marks, 'out of ',self.scheme['totalmarks'])
        time.sleep(0.1)
        self.logger.info('Finish answer reading')
