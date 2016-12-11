from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re


class Type2(Logs):
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

        self.logger.info('Reading answers')
        with open(self.answer_file) as answer:
            i = 0
            marks = 0
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
                        if re.search(r'\d', matrix_leftside):
                            ans_matrix = int(matrix_leftside[0:1]) * self.question[matrix_leftside[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                #self.logger.info('your step is correct')
                                if multiplied and not gotSubsMark:
                                    print('your mark for substitution ', self.scheme['substitution'])
                                    gotSubsMark = True
                                    marks+=1
                                if not multiplied and not gotMultipliedMark:
                                    print('your mark for multiplication ', self.scheme['multiplication'])
                                    gotMultipliedMark = True
                                    marks += 1
                                if middlesubs and not gotSubsMark:
                                    print('your mark for substitution ', self.scheme['substitution'])
                                    gotSubsMark = True
                                    marks += 1

                                else:
                                    if multiplied and not gotSubsMark:
                                        print('your mark for substitution ', self.scheme['substitution'])
                                        gotSubsMark = True
                                        marks += 1
                                    if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                        print('your mark for multiplication ', self.scheme['multiplication'])
                                        gotMultipliedMark = True
                                        marks += 1
                                    if not gotSubsMark and gotMultipliedMark:
                                        print('your mark for substitution ', self.scheme['substitution'])
                                        gotSubsMark = True
                                        marks += 1
                                    if middlesubs and not gotSubsMark:
                                        print('your mark for substitution ', self.scheme['substitution'])
                                        gotSubsMark = True
                                        marks += 1
                            list.clear()
                            mtrilist.clear()
                            isfoundrow = true
                            matri_name.clear()
                            siz = 0
                            count = 0
                            multiplied = False
                            middlesubs = False
                if list or isTwoMatrixInvolved:
                    matrix_question = self.question['ques']
                    twooperandsplitarray = []
                    if "-" in matrix_question:
                        iscontainminus = true
                        # split the left hand side using -
                        twooperandsplitarray = matrix_question.split('-')
                    elif "+" in matrix_question:
                        iscontainplus = true
                        # split the left hand side using +
                        twooperandsplitarray = matrix_question.split('+')
                    if len(twooperandsplitarray) < 1:

                        if re.search(r'\d', matrix_question):
                            ans_matrix = int(matrix_question[0:1]) * self.question[matrix_question[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                # self.logger.info('your step is correct')
                                if not multiplied and not gotMultipliedMark:
                                    print('your mark for multiplication ', self.scheme['multiplication'])
                                    gotMultipliedMark = True
                                    marks += 1
                    else:
                        if len(twooperandsplitarray[0]) > 1:
                            matrix_1 = int(twooperandsplitarray[0][0:1]) * self.question[twooperandsplitarray[0][1:2]]
                        elif len(twooperandsplitarray[0]) <= 1:
                            matrix_1 = self.question[twooperandsplitarray[0]]
                        if len(twooperandsplitarray[1]) > 1:
                            matrix_2 = int(twooperandsplitarray[1][0:1]) * self.question[twooperandsplitarray[1][1:2]]
                        elif len(twooperandsplitarray[1]) <= 1:
                            matrix_2 = self.question[twooperandsplitarray[1]]

                        if iscontainplus:
                            ans_matrix = matrix_1 + matrix_2
                        elif iscontainminus:
                            ans_matrix = matrix_1 - matrix_2

                        stu_ans_matr1 = list[0:row_size]
                    if operator:
                        stu_ans_matr2 = list[row_size:len(list)]
                        if str(operator).strip() == '+':
                            stu_ans = Matrix(stu_ans_matr1) + Matrix(stu_ans_matr2)
                            subs_matrix = ans_matrix - stu_ans
                            if subs_matrix == zeros(row_size, col_size):
                                #self.logger.info('your step is correct')
                                if multiplied and not gotSubsMark:
                                    print('your mark for substitution ', self.scheme['substitution'])
                                    gotSubsMark = True
                                    marks += 1
                                if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                    print('your mark for multiplication ', self.scheme['multiplication'])
                                    gotMultipliedMark = True
                                    marks += 1
                                if not gotSubsMark and gotMultipliedMark:
                                    print('your mark for substitution ', self.scheme['substitution'])
                                    gotSubsMark = True
                                    marks += 1
                                if middlesubs and not gotSubsMark:
                                    print('your mark for substitution ', self.scheme['substitution'])
                                    gotSubsMark = True
                                    marks += 1
                            list.clear()
                            mtrilist.clear()
                            isfoundrow = true
                            matri_name.clear()
                            siz = 0
                            count = 0
                            multiplied = False
                            middlesubs = False
                            operator = None


                        elif str(operator).strip() == '-':
                            stu_ans = Matrix(stu_ans_matr1) - Matrix(stu_ans_matr2)
                            subs_matrix = ans_matrix - stu_ans
                            if subs_matrix == zeros(row_size, col_size):
                               # self.logger.info('your step is correct')
                                if multiplied and not gotSubsMark:
                                    print('your mark for substitution ', self.scheme['substitution'])
                                    gotSubsMark = True
                                    marks += 1
                                if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                    print('your mark for multiplication ', self.scheme['multiplication'])
                                    gotMultipliedMark = True
                                    marks += 1
                                if not gotSubsMark and gotMultipliedMark:
                                    print('your mark for substitution ', self.scheme['substitution'])
                                    gotSubsMark = True
                                    marks += 1
                                if middlesubs and not gotSubsMark:
                                    print('your mark for substitution ', self.scheme['substitution'])
                                    gotSubsMark = True
                                    marks += 1
                            list.clear()
                            mtrilist.clear()
                            isfoundrow = true
                            matri_name.clear()
                            siz = 0
                            count = 0
                            multiplied = False
                            middlesubs = False
                            operator = None


                    else:
                        subs_matrix = ans_matrix - Matrix(stu_ans_matr1)
                        if subs_matrix == zeros(row_size, col_size):
                            #self.logger.info('your step is correct')
                            if len(list) / row_size == 1 and not gotFinalStepMark and not middlesubs:
                                if iscontainminus:
                                    print('your mark for subtraction ', self.scheme['subtraction'])
                                    marks += 1
                                else:
                                    print('your mark for addition ', self.scheme['addition'])
                                    gotFinalStepMark = True
                                    marks += 1
                            if not gotMultipliedMark:
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
                        operator = None
                i += 1
            print('your final marks is ', marks)