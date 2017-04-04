from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re


class Answer(Logs):
    col_size = None
    row_size = None

    def __init__(self,scheme, answer_file, ques, logger):
        self.scheme = scheme
        self.answer_file = answer_file
        self.logger = logger
        self.ques = ques

    def markAnswer(self):
        x = Symbol('x')  # define symbol for variable
        y = Symbol('y')  # define symbol for variable
        isfoundcol = true  # check whether column size has found
        isfoundrow = true  # check whether row size has found
        mtrilist = []  # store right hand side answer
        matri_name = []  # store left hand side
        list = []  # store all matrix or values in the RHS
        count = 0  # check whether matrix expression has started
        ispassfenced = false
        iscontain_equals = false
        old_ans_matrix = None
        ans_matrix = None
        rightside_constant = None
        # check whether the step is already multiplied by the system
        multiplied = False
        gotMultipliedMark = False
        gotSubsMark = False
        gotFinalStepMark = False
        # check whether middle minus there
        middlesubs = False

        self.logger.info('Reading answers')
        # open the answer file
        with open(self.scheme) as scheme:
            for line in scheme:
                scheme_soup = BeautifulSoup(line, "html.parser")
        with open(self.answer_file) as answer:
            i = 0
            isContainVariable = False
            # parse the answer file
            for line in answer:
                ans_soup = BeautifulSoup(line, "html.parser")
                if 'mi' in line and 'mtd' not in line and not ispassfenced:
                    if((ans_soup.text.strip() == str(x)) or (ans_soup.text.strip() == str(y))):
                        isContainVariable = True
                    temp = ans_soup.text
                    matri_name.insert(0, temp)
                    count += 1
                if 'mfenced' in line:
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
                    if isContainVariable:
                        mtrilist.insert(i, ans_soup.text)
                        isContainVariable = False
                    else:
                        rightside_constant = ans_soup.text
                if '/mtr' in line and isfoundcol:
                    col_size = len(mtrilist)
                    isfoundcol = false
                if '/mo' in line and count > 0:
                    if '=' not in ans_soup.text:
                        matri_name.insert(0, ans_soup.text)
                if '/mo' in line and count == 0:
                    if ans_soup.text == '=':
                        iscontain_equals = ans_soup.text
                if '/mtable' in line:
                    if isfoundrow:
                        siz = len(mtrilist)
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
                # if student write lefthand side and right hand side
                if matri_name and list:
                    length = len(matri_name)
                    matrix_leftside = ''
                    # more than one matrix involved
                    if length > 2:
                        for d in range(0, length):
                            matrix_leftside += matri_name.pop().strip()
                        if "-" in matrix_leftside:
                            iscontainminus = true
                            # split the left hand side using -
                            twooperandsplitarray = matrix_leftside.split('-')
                        elif "+" in matrix_leftside:
                            iscontainplus = true
                            # split the left hand side using +
                            twooperandsplitarray = matrix_leftside.split('+')
                        if len(twooperandsplitarray[0]) > 1:
                            matrix_1 = int(twooperandsplitarray[0][0:1]) * self.ques[twooperandsplitarray[0][1:2]]
                        elif len(twooperandsplitarray[0]) <= 1:
                            matrix_1 = self.ques[twooperandsplitarray[0]]
                        if len(twooperandsplitarray[1]) > 1:
                            matrix_2 = int(twooperandsplitarray[1][0:1]) * self.ques[twooperandsplitarray[1][1:2]]
                        elif len(twooperandsplitarray[1]) <= 1:
                            matrix_2 = self.ques[twooperandsplitarray[1]]

                        if iscontainplus:
                            ans_matrix = matrix_1 + matrix_2
                        elif iscontainminus:
                            ans_matrix = matrix_1 - matrix_2
                        if len(list) == row_size:
                            subs_matrix = ans_matrix - Matrix(list)
                        else:
                            # check the substitution is in the middle step rather than first step
                            stu_ans_matr1 = list[0:row_size]
                            stu_ans_matr2 = list[row_size:len(list)]
                            if iscontainplus:
                                stu_ans = Matrix(stu_ans_matr1) + Matrix(stu_ans_matr2)
                            elif iscontainminus:
                                stu_ans = Matrix(stu_ans_matr1) - Matrix(stu_ans_matr2)
                            subs_matrix = ans_matrix - stu_ans
                        if subs_matrix == zeros(row_size, col_size):
                            self.logger.info('your step is correct')
                            if multiplied and not gotSubsMark:
                                self.logger.info('your are getting one mark for subtitution')
                                gotSubsMark = True
                            if len(list) / row_size == 1 and not gotFinalStepMark and not middlesubs:
                                self.logger.info('your are getting one mark for final step ')
                                gotFinalStepMark = True
                            if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                self.logger.info('your are getting one mark for mulplication step ')
                                gotMultipliedMark = True
                            if middlesubs and not gotSubsMark:
                                self.logger.info('your are getting one mark for subtitution')
                                gotSubsMark = True
                            if self.ques['ques'] == 'xy':
                                answers = solve((self.ques[matrix_leftside]-ans_matrix), x, y)
                                answerofx = answers.pop(x)
                                answerofy = answers.pop(y)
                            elif self.ques['ques'] == 'x':
                                answers = solve((self.ques[matrix_leftside] - ans_matrix), x)
                                answerofx = answers.pop(x)

                        list.clear()
                        mtrilist.clear()
                        isfoundcol = true
                        isfoundrow = true
                        old_ans_matrix = ans_matrix
                        matri_name.clear()
                        siz = 0
                        count = 0
                        multiplied = False
                        middlesubs = False
                    # only one matrix involved
                    else:
                        matrix_leftside = matri_name.pop().strip()
                        if matrix_leftside=='x':
                            retrieveans = list.pop(0).pop(0)
                            if (answerofx - int(retrieveans.strip())) == 0:
                                self.logger.info('your found x correctly')
                            list.clear()
                            mtrilist.clear()
                            isfoundcol = true
                            isfoundrow = true
                            old_ans_matrix = ans_matrix
                            matri_name.clear()
                            siz = 0
                            count = 0
                            multiplied = False
                            middlesubs = False
                        if matrix_leftside == 'y':
                            retrieveans = list.pop(0).pop(0)
                            if (answerofy - int(retrieveans.strip())) == 0:
                                self.logger.info('your found y correctly')
                            list.clear()
                            mtrilist.clear()
                            isfoundcol = true
                            isfoundrow = true
                            old_ans_matrix = ans_matrix
                            matri_name.clear()
                            siz = 0
                            count = 0
                            multiplied = False
                            middlesubs = False
                        else:
                            if re.search(r'\d', matrix_leftside):
                                ans_matrix = int(matrix_leftside[0:1]) * self.ques[matrix_leftside[1:2]]
                                subs_matrix = ans_matrix - Matrix(list)
                                if subs_matrix == zeros(row_size, col_size):
                                    self.logger.info('your step is correct')

                                    if len(self.ques['ques']) > 2 :
                                        if multiplied and not gotSubsMark:
                                            self.logger.info('your are getting one mark for subtitution')
                                            gotSubsMark = True
                                        # if len(list) / row_size == 1 and not gotFinalStepMark:
                                        #     logger.info('your are getting one mark for final step ')
                                        #     gotFinalStepMark = True
                                        if len(list) / row_size == 1 and not multiplied and not gotMultipliedMark:
                                            self.logger.info('your are getting one mark for mulplication step ')
                                            gotMultipliedMark = True

                                    elif (self.ques['ques'] == 'xy') :
                                        if multiplied and not gotSubsMark:
                                            self.logger.info('your are getting one mark for subtitution')
                                            gotSubsMark = True
                                        # if len(list) / row_size == 1 and not gotFinalStepMark:
                                        #     logger.info('your are getting one mark for final step ')
                                        #     gotFinalStepMark = True
                                        if len(list) / row_size == 1 and not multiplied and not gotMultipliedMark:
                                            self.logger.info('your are getting one mark for mulplication step ')
                                            gotMultipliedMark = True

                                    else:
                                        if multiplied and not gotSubsMark:
                                            self.logger.info('your are getting one mark for subtitution')
                                            gotSubsMark = True
                                        if len(list) / row_size == 1 and not gotFinalStepMark:
                                            self.logger.info('your are getting one mark for final step ')
                                            gotFinalStepMark = True
                                        if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                            self.logger.info('your are getting one mark for mulplication step ')
                                            gotMultipliedMark = True
                                list.clear()
                                mtrilist.clear()
                                isfoundcol = true
                                isfoundrow = true
                                old_ans_matrix = ans_matrix
                                matri_name.clear()
                                siz = 0
                                count = 0
                                multiplied = False
                                middlesubs = False
                # if student didn't write any lefthand side rather only right hand side answers were there
                elif list:
                    if iscontain_equals:
                        if len(list) == row_size:
                            subs_matrix = old_ans_matrix - Matrix(list)
                        else:
                            stu_ans_matr1 = list[0:row_size]
                            stu_ans_matr2 = list[row_size:len(list)]
                            if iscontainplus:
                                stu_ans = Matrix(stu_ans_matr1) + Matrix(stu_ans_matr2)
                            elif iscontainminus:
                                stu_ans = Matrix(stu_ans_matr1) - Matrix(stu_ans_matr2)
                            subs_matrix = old_ans_matrix - stu_ans
                        if subs_matrix == zeros(row_size, col_size):
                            self.logger.info('your step is correct')
                            if multiplied and not gotSubsMark:
                                self.logger.info('your are getting one mark for subtitution')
                                gotSubsMark = True
                            if len(list) / row_size == 1 and not gotFinalStepMark and not middlesubs:
                                self.logger.info('your are getting one mark for final step ')
                                gotFinalStepMark = True
                            if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                self.logger.info('your are getting one mark for mulplication step ')
                                gotMultipliedMark = True
                            if middlesubs and not gotSubsMark:
                                self.logger.info('your are getting one mark for subtitution')
                                gotSubsMark = True
                        list.clear()
                        mtrilist.clear()
                        isfoundcol = true
                        isfoundrow = true
                        old_ans_matrix = ans_matrix
                        matri_name.clear()
                        siz = 0
                        count = 0
                        multiplied = False
                        middlesubs = False
                    else:
                        matrix_leftside = self.ques['ques']
                        if "-" in matrix_leftside:
                            iscontainminus = true
                            # split the left hand side using -
                            twooperandsplitarray = matrix_leftside.split('-')
                        elif "+" in matrix_leftside:
                            iscontainplus = true
                            # split the left hand side using +
                            twooperandsplitarray = matrix_leftside.split('+')
                        if len(twooperandsplitarray[0]) > 1:
                            matrix_1 = int(twooperandsplitarray[0][0:1]) * self.ques[twooperandsplitarray[0][1:2]]
                        elif len(twooperandsplitarray[0]) <= 1:
                            matrix_1 = self.ques[twooperandsplitarray[0]]
                        if len(twooperandsplitarray[1]) > 1:
                            matrix_2 = int(twooperandsplitarray[1][0:1]) * self.ques[twooperandsplitarray[1][1:2]]
                        elif len(twooperandsplitarray[1]) <= 1:
                            matrix_2 = self.ques[twooperandsplitarray[1]]

                        if iscontainplus:
                            ans_matrix = matrix_1 + matrix_2
                        elif iscontainminus:
                            ans_matrix = matrix_1 - matrix_2
                        if len(list) == row_size:
                            subs_matrix = ans_matrix - Matrix(list)
                        else:
                            stu_ans_matr1 = list[0:row_size]
                            stu_ans_matr2 = list[row_size:len(list)]
                            if iscontainplus:
                                stu_ans = Matrix(stu_ans_matr1) + Matrix(stu_ans_matr2)
                            elif iscontainminus:
                                stu_ans = Matrix(stu_ans_matr1) - Matrix(stu_ans_matr2)
                            subs_matrix = ans_matrix - stu_ans
                        if subs_matrix == zeros(row_size, col_size):
                            self.logger.info('your step is correct')
                            if multiplied and not gotSubsMark:
                                self.logger.info('your are getting one mark for subtitution')
                                gotSubsMark = True
                            if len(list) / row_size == 1 and not gotFinalStepMark and not middlesubs:
                                self.logger.info('your are getting one mark for final step ')
                                gotFinalStepMark = True
                            if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                self.logger.info('your are getting one mark for mulplication step ')
                                gotMultipliedMark = True
                            if middlesubs and not gotSubsMark:
                                self.logger.info('your are getting one mark for subtitution')
                                gotSubsMark = True
                        list.clear()
                        mtrilist.clear()
                        isfoundcol = true
                        isfoundrow = true
                        old_ans_matrix = ans_matrix
                        matri_name.clear()
                        siz = 0
                        count = 0
                        multiplied = False
                        middlesubs = False
                i += 1
        self.logger.info('finish answer reading')
