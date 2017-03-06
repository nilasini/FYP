from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re
import time
from threading import Thread


class Type3(Logs, Thread):
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
        viceversa_ans = 0
        isfound = true
        isfoundrow = true
        mtrilist = []
        matri_name = []
        list = []
        siz = 0
        count = 0
        ispassfenced = false
        equation = []
        eqn_list = []
        iscontain_equals = false
        old_ans_matrix = None
        ans_matrix = None
        rightside_constant = None
        iscontain_var = None
        # check whether the step is already multiplied by the system
        multiplied = False
        gotMultipliedMark = False
        gotequationmarkforx = False
        gotequationmarkfory = False
        gotxmark = False
        gotymark = False
        # check whether middle minus there
        middlesubs = False
        operator = None
        correct_finding = 0
        iseqnforxcrct = true
        iseqnforycrct = true

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
                if 'mfenced' in line:
                    # count = 0
                    ispassfenced = true
                if '/mfenced' in line:
                    ispassfenced = false
                    rightside_constant = None
                if '/mtr' in line and isfound:
                    col_size = len(mtrilist)
                    isfound = false
                if '/mtable' in line:
                    if isfoundrow:
                        siz += len(mtrilist)
                        row_size = int(siz / col_size)
                        isfoundrow = false
                if 'mi' in line and 'mtd' not in line and not ispassfenced and not equation:
                    if (re.search("[a-z]", ans_soup.text.strip())):
                        isContainVariable = True
                        equation.append( ans_soup.text.strip())
                    else:
                        temp = ans_soup.text
                        matri_name.insert(0, temp)
                        # count += 1
                elif '/mo' in line and not ispassfenced and not equation:
                    if ans_soup.text == '=':
                        iscontain_equals = ans_soup.text
                    else:
                        operator = ans_soup.text
                elif 'mi' in line and equation:
                    equation.append(ans_soup.text.strip())
                elif 'mn' in line and 'mtd' in line:
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
                elif 'mn' in line and 'mtd' not in line and ispassfenced:
                    if isContainVariable:
                        mtrilist.insert(i, ans_soup.text)
                        isContainVariable = False
                    else:
                        rightside_constant = ans_soup.text
                elif 'mn' in line and 'mtd' not in line and not ispassfenced:
                    equation.append(ans_soup.text.strip())
                elif '/mo' in line and ispassfenced and not equation:
                    if '=' not in ans_soup.text:
                        matri_name.insert(0, ans_soup.text)
                elif '/mo' in line and equation:
                    equation.append(ans_soup.text.strip())
                elif 'mspace' in line and equation:
                    eqn_list.append(equation)
                elif 'mspace' in line and not equation:
                    list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                    oneStepFinished = true
                    for elements in list:
                        for element in elements:
                            if re.search("\d[-]\d", element):
                                middlesubs = True
                iscontainplus = false
                iscontainminus = false
                noVarInLeft = false
                val = ''
                # if student write left hand side and right hand side
                if k == 0:
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
                            withoutcons_ans_matrix = self.question[matrix_leftside[1:2]]
                            ans_matrix = int(matrix_leftside[0:1]) * self.question[matrix_leftside[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
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
                                    print('you have forgotten to muliply by the constant ', matrix_leftside[0:1])
                                    break
                                if not multiplied:
                                    print('you have made mistake in multiplication in calculation of ', matrix_leftside)
                                    break
                # if student didn't write any left hand side rather only right hand side answers were there
                if (list and (not matri_name)) or noVarInLeft:
                    multiplied = False
                    middlesubs = False
                    if iscontain_var:
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
                                    print('you have forgotten to muliply by the constant ', matrix_leftside[0:1])
                                    break
                                if not multiplied:
                                    print('you have made mistake in multiplication in calculation of ', matrix_leftside)
                                    break
                if eqn_list:
                    val1 = eqn_list.pop()
                    for r in val1:
                        val += r
                    splitted_eqn = val.split('=')
                    if '-' in splitted_eqn[0]:
                        splitted_leqn = splitted_eqn[0].split('-')
                        if re.search("[a-z]", splitted_leqn[0]) and re.search("[a-z]", splitted_leqn[1]):
                            if re.search(r'\d', splitted_leqn[0]):
                                result1 = int(splitted_leqn[0][0:1]) * (Symbol(splitted_leqn[0][1:2]))
                            else:
                                result1 = Symbol(splitted_leqn[0])
                            if re.search(r'\d', splitted_leqn[1]):
                                result2 = int(splitted_leqn[1][0:1]) * (Symbol(splitted_leqn[1][1:2]))
                            else:
                                result2 = Symbol(splitted_leqn[1])
                            result = (result1 - result2).subs({x:answerofx, y:answerofy})
                            if result == (int)(splitted_eqn[1]):
                                print('you are getting mark for correct equation ', self.scheme['equation'])
                                marks += 1
                            else:
                                print('you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                        elif re.search("[a-z]", splitted_leqn[0]):
                            if re.search("x", splitted_leqn[0]):
                                result = ((Symbol)(splitted_leqn[0])-(int)(splitted_leqn[1])).subs(x, answerofx)
                                if result == (int)(splitted_eqn[1]) and ((gotMultipliedMark and not gotequationmarkfory) or (not gotMultipliedMark and not gotequationmarkforx)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkforx = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforxcrct = true
                                if not result == (int)(splitted_eqn[1]):
                                    iseqnforxcrct = false
                                    print('equation for x is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                            else:
                                result = (Symbol)(splitted_leqn[0] - (int)(splitted_leqn[1])).subs(y, answerofy)
                                if result == (int)(splitted_eqn[1]) and ((gotMultipliedMark and not gotequationmarkforx) or (not gotMultipliedMark and not gotequationmarkfory)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkfory = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforycrct = true
                                if not result == (int)(splitted_eqn[1]):
                                    print('equation for y is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                                    iseqnforycrct = false
                        elif re.search("[a-z]", splitted_leqn[1]):
                            if re.search("x", splitted_leqn[1]):
                                result = ((int)(splitted_leqn[0])-(Symbol)(splitted_leqn[1])).subs(x, answerofx)
                                if result == (int)(splitted_eqn[1]) and ((gotMultipliedMark and not gotequationmarkfory) or (not gotMultipliedMark and not gotequationmarkforx)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkforx = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforxcrct = true
                                # elif result == (int)(splitted_eqn[1]) and not gotMultipliedMark:
                                #     print('you are getting mark for correct equation ', self.scheme['equation'])
                                #     gotequationmarkforx = true
                                #     iseqnforxcrct = true
                                #     marks += 1
                                if not result == (int)(splitted_eqn[1]):
                                    print('equation for x is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                                    iseqnforxcrct = false
                            else:
                                result = ((int)(splitted_leqn[0]) - (Symbol)(splitted_leqn[1])).subs(y, answerofy)
                                if result == (int)(splitted_eqn[1]) and ((gotMultipliedMark and not gotequationmarkforx) or (not gotMultipliedMark and not gotequationmarkfory)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkfory = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforycrct = true
                                # elif result == (int)(splitted_eqn[1]) and not gotMultipliedMark:
                                #     print('you are getting mark for correct equation ', self.scheme['equation'])
                                #     gotequationmarkfory = true
                                #     iseqnforycrct = true
                                #     marks += 1
                                if not result == (int)(splitted_eqn[1]):
                                    print('equation for y is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                                    iseqnforycrct = false
                    elif '+' in splitted_eqn[0]:
                        splitted_leqn = splitted_eqn[0].split('+')
                        if re.search("[a-z]", splitted_leqn[0]) and re.search("[a-z]", splitted_leqn[1]):
                            if re.search(r'\d', splitted_leqn[0]):
                                result1 = int(splitted_leqn[0][0:1]) * (Symbol(splitted_leqn[0][1:2]))
                            else:
                                result1 = Symbol(splitted_leqn[0])
                            if re.search(r'\d', splitted_leqn[1]):
                                result2 = int(splitted_leqn[1][0:1]) * (Symbol(splitted_leqn[1][1:2]))
                            else:
                                result2 = Symbol(splitted_leqn[1])
                            result = (result1 + result2).subs({x: answerofx, y: answerofy})
                            if result == (int)(splitted_eqn[1]):
                                print('you are getting mark for correct equation ', self.scheme['equation'])
                                marks += 1
                            else:
                                print(
                                    'you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                        elif re.search("[a-z]", splitted_leqn[0]):
                            if re.search("x", splitted_leqn[0]):
                                result = ((Symbol)(splitted_leqn[0]) + (int)(splitted_leqn[1])).subs(x, answerofx)
                                if result == (int)(splitted_eqn[1]) and (
                                    (gotMultipliedMark and not gotequationmarkfory) or (
                                    not gotMultipliedMark and not gotequationmarkforx)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkforx = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforxcrct = true
                                if not result == (int)(splitted_eqn[1]):
                                    iseqnforxcrct = false
                                    print(
                                        'equation for x is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                            else:
                                result = (Symbol)(splitted_leqn[0] + (int)(splitted_leqn[1])).subs(y, answerofy)
                                if result == (int)(splitted_eqn[1]) and (
                                    (gotMultipliedMark and not gotequationmarkforx) or (
                                    not gotMultipliedMark and not gotequationmarkfory)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkfory = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforycrct = true
                                if not result == (int)(splitted_eqn[1]):
                                    print(
                                        'equation for y is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                                    iseqnforycrct = false
                        elif re.search("[a-z]", splitted_leqn[1]):
                            if re.search("x", splitted_leqn[1]):
                                result = ((int)(splitted_leqn[0]) + (Symbol)(splitted_leqn[1])).subs(x, answerofx)
                                if result == (int)(splitted_eqn[1]) and (
                                    (gotMultipliedMark and not gotequationmarkfory) or (
                                    not gotMultipliedMark and not gotequationmarkforx)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkforx = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforxcrct = true
                                # elif result == (int)(splitted_eqn[1]) and not gotMultipliedMark:
                                #     print('you are getting mark for correct equation ', self.scheme['equation'])
                                #     gotequationmarkforx = true
                                #     iseqnforxcrct = true
                                #     marks += 1
                                if not result == (int)(splitted_eqn[1]):
                                    print('equation for x is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                                    iseqnforxcrct = false
                            else:
                                result = ((int)(splitted_leqn[0]) + (Symbol)(splitted_leqn[1])).subs(y, answerofy)
                                if result == (int)(splitted_eqn[1]) and (
                                    (gotMultipliedMark and not gotequationmarkforx) or (
                                    not gotMultipliedMark and not gotequationmarkfory)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkfory = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforycrct = true
                                # elif result == (int)(splitted_eqn[1]) and not gotMultipliedMark:
                                #     print('you are getting mark for correct equation ', self.scheme['equation'])
                                #     gotequationmarkfory = true
                                #     iseqnforycrct = true
                                #     marks += 1
                                if not result == (int)(splitted_eqn[1]):
                                    print(
                                        'equation for y is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                                    iseqnforycrct = false
                    else:
                        if splitted_eqn[0] == "x":
                            retrieveans = splitted_eqn[1].strip()
                            if re.search("[0-9]+[+|-][0-9]+", retrieveans):
                                if "-" in retrieveans:  # check for x=6-1 type answers
                                    splitted_ans = retrieveans.split('-')
                                    retrieveans = int(splitted_ans[0]) - int(splitted_ans[1])
                                elif "+" in retrieveans:
                                    splitted_ans = retrieveans.split('+')
                                    retrieveans = int(splitted_ans[0]) + int(splitted_ans[1])
                                if result == (int)(splitted_eqn[1]) and ((gotMultipliedMark and not gotequationmarkfory) or (not gotMultipliedMark and not gotequationmarkforx)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkforx = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforxcrct = true
                                else:
                                    print('equation for x is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                                    iseqnforxcrct = false
                            elif (answerofx - int(retrieveans)) == 0 and iseqnforxcrct and not gotxmark:
                                print('your mark for find x is ', self.scheme['findonevariable'])
                                marks += 1
                                gotxmark = true
                                correct_finding += 1
                            elif (answerofx - int(retrieveans)) == 0 and iseqnforxcrct and gotxmark:
                                print('your answer for y step has been duplicated')
                            elif (answerofx - int(retrieveans)) == 0 and not iseqnforxcrct:
                                print('your x value is correct but your equation for x is wrong therefore you are not '
                                      'getting any mark for finding x')
                            elif (answerofy - int(retrieveans.strip())) == 0:
                                viceversa_ans += 1
                            elif (answerofx - -(int(retrieveans.strip()))) == 0:
                                print('your answer for x has been negated')
                            elif iseqnforxcrct:
                                print('your value for x is wrong')
                        if splitted_eqn[0] == "y":
                            retrieveans = splitted_eqn[1].strip()
                            if re.search("[0-9]+[+|-][0-9]+", retrieveans):
                                if "-" in retrieveans:  # check for x=6-1 type answers
                                    splitted_ans = retrieveans.split('-')
                                    retrieveans = int(splitted_ans[0]) - int(splitted_ans[1])
                                elif "+" in retrieveans:
                                    splitted_ans = retrieveans.split('+')
                                    retrieveans = int(splitted_ans[0]) + int(splitted_ans[1])
                                if (answerofy - int(retrieveans)) == 0:
                                    iseqnforycrct = true
                                if result == (int)(splitted_eqn[1]) and ((gotMultipliedMark and not gotequationmarkforx) or (not gotMultipliedMark and not gotequationmarkfory)):
                                    print('you are getting mark for correct equation ', self.scheme['equation'])
                                    gotequationmarkfory = true
                                    marks += 1
                                if result == (int)(splitted_eqn[1]):
                                    iseqnforycrct = true
                                else:
                                    print('equation for y is wrong, you are in lack of understanding in how to make an algebraic equation from a matrix equation')
                                    iseqnforycrct = false
                            elif (answerofy - int(retrieveans.strip())) == 0 and iseqnforycrct and not gotymark:
                                print('your mark for find y is ', self.scheme['findonevariable'])
                                marks += 1
                                correct_finding += 1
                                gotymark = true
                            elif (answerofy - int(retrieveans.strip())) == 0 and iseqnforycrct and gotymark:
                                print('your answer for y step has been duplicated')
                            elif (answerofy - int(retrieveans)) == 0 and not iseqnforycrct:
                                print('your y value is correct but your equation for y is wrong therefore you are not '
                                      'getting any mark for finding y')
                            elif (answerofx - int(retrieveans.strip())) == 0:
                                viceversa_ans += 1
                            elif (answerofy - -(int(retrieveans.strip()))) == 0:
                                print('your answer for y has been negated')
                            else:
                                print('your value for y is wrong')
                        if viceversa_ans == 2:
                            print('you have mirrored the answer for x and y')
                            viceversa_ans = 0
                            break

                    eqn_list.clear()
                    equation.clear()
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
            print('your final marks is ', marks, 'out of ', self.scheme['totalmarks'])
        time.sleep(0.1)
        self.logger.info('Finish answer reading')
