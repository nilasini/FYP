from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re


class Type3(Logs):
    col_size = None
    row_size = None

    def __init__(self, ques, scheme, answer_file, logger):
        self.scheme = scheme
        self.answer_file = answer_file
        self.logger = logger
        self.question = ques

    def markAns(self):
        x = Symbol('x')
        y = Symbol('y')
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
        operator = None

        self.logger.info('Reading answers')
        # open the answer file
        with open(self.answer_file) as answer:
            i = 0
            k = 0
            marks = 0
            isContainVariable = False
            # parse the answer file
            for line in answer:
                ans_soup = BeautifulSoup(line, "html.parser")
                oneStepFinished = false
                if 'mi' in line and 'mtd' not in line and not ispassfenced:
                    if ((ans_soup.text.strip() == str(x)) or (ans_soup.text.strip() == str(y))):
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
                        # if 'x' in ans_soup.text or 'y' in ans_soup.text:
                        #     iscontain_var = true
                        if re.search("[a-z]", ans_soup.text):
                            iscontain_var = true
                if 'mn' in line and 'mtd' not in line:
                    if isContainVariable:
                        mtrilist.insert(i, ans_soup.text)
                        isContainVariable = False
                    else:
                        rightside_constant = ans_soup.text
                if '/mtr' in line and isfound:
                    col_size = len(mtrilist)
                    isfound = false
                if '/mo' in line and count > 0:
                    if '=' not in ans_soup.text:
                        matri_name.insert(0, ans_soup.text)
                if '/mo' in line and count == 0:
                    if ans_soup.text == '=':
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
                    oneStepFinished = true
                    for elements in list:
                        for element in elements:
                            if re.search("\d[-]\d", element):
                                middlesubs = True

                iscontainplus = false
                iscontainminus = false
                noVarInLeft = false
                # if student write lefthand side and right hand side
                if k == 0 and ((matri_name and list) or list):
                    matrix_question = ''
                    for element in self.question:
                        if re.search("[0-9]?[A-Z][-|+][0-9]?[A-Z]", element):
                            matrix_question = element
                            break
                    k += 1
                    if "-" in matrix_question:
                        iscontainminus = true
                        # split the left hand side using -
                        twooperandsplitarray = matrix_question.split('-')
                    elif "+" in matrix_question:
                        iscontainplus = true
                        # split the left hand side using +
                        twooperandsplitarray = matrix_question.split('+')
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
                    M1 = self.question[matrix_question]
                    answers = solve(M1 - ans_matrix, x, y)
                    answerofx = answers.pop(x)
                    answerofy = answers.pop(y)

                if matri_name and list:
                    length = len(matri_name)
                    # more than one matrix involved
                    if length > 2:
                        for element in matri_name:
                            if re.search("[A-Z]", element):
                                list = matri_name
                                matri_name.clear()
                                noVarInLeft = true

                    if length < 2 or length == 2:
                        # check the substitution is in the middle step rather than first step
                        matrix_leftside = matri_name.pop().strip()
                        if re.search(r'\d', matrix_leftside):
                            ans_matrix = int(matrix_leftside[0:1]) * self.question[matrix_leftside[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                if not multiplied and not gotMultipliedMark:
                                    print('your mark for multiplication ', self.scheme['multiplication'])
                                    gotMultipliedMark = True
                                    marks += 1

                        if matrix_leftside == "x":
                            retrieveans = list.pop(0).pop(0)
                            if (answerofx - int(retrieveans.strip())) == 0:
                                print('your mark for find x is ', self.scheme['findonevariable'])
                                marks += 1

                        if matrix_leftside == "y":
                            retrieveans = list.pop(0).pop(0)
                            if (answerofy - int(retrieveans.strip())) == 0:
                                print('your mark for find y is ', self.scheme['findonevariable'])
                                marks += 1

                # if student didn't write any lefthand side rather only right hand side answers were there
                if (list and (not matri_name)) or noVarInLeft:
                    multiplied = False
                    middlesubs = False
                    if iscontain_var:
                        #stu_ans_matr2 = list[row_size:len(list)]
                        #if str(operator).strip() == '+':
                            stu_ans_matr1 = list[0:row_size]
                            stu_ans = Matrix(stu_ans_matr1)
                            stu_ans_temp = stu_ans.replace(x, answerofx)
                            stu_ans = stu_ans_temp.replace(y, answerofy)

                            subs_matrix = self.question[matrix_question] - stu_ans
                            if subs_matrix == zeros(row_size, col_size):
                                if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                    print('your mark for multiplication ', self.scheme['multiplication'])
                                    gotMultipliedMark = True
                                    marks += 1
                                if "+" in matrix_question:
                                    print('your mark for find addition is ', self.scheme['addition'])
                                    marks += 1
                                elif "-" in matrix_question:
                                    print('your mark for find subtraction is ', self.scheme['subtraction'])
                                    marks += 1
                if oneStepFinished:
                    iscontain_var = false
                    list.clear()
                    mtrilist.clear()
                    isfound = true
                    isfoundrow = true
                    old_ans_matrix = ans_matrix
                    matri_name.clear()
                    siz = 0
                    count = 0
                    multiplied = False
                    middlesubs = False

                i += 1
            print('your final marks is ', marks)
