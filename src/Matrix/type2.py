from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re
import time
import numpy as np
from threading import Thread
import json

class Type2(Logs, Thread):
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
        error_Identification = []
        concept = []
        step = 0
        errStep = 0
        dataArray = []

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
                oneStepFinished = false
                ans_soup = BeautifulSoup(line, "html.parser")
                if 'mi' in line and 'mtd' not in line and not ispassfenced:
                    temp = ans_soup.text.strip()
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
                        s_text = int(rightside_constant) * int(ans_soup.text.strip())
                        mtrilist.insert(i, str(s_text))
                        multiplied = True
                    else:
                        mtrilist.insert(i, ans_soup.text.strip())
                if 'mn' in line and 'mtd' not in line:
                    rightside_constant = ans_soup.text.strip()
                if '/mtr' in line and isfoundcol:
                    col_size = len(mtrilist)
                    isfoundcol = false
                if '/mo' in line and count > 0:
                    if '=' not in ans_soup.text:
                        matri_name.insert(0, ans_soup.text.strip())
                if '/mo' in line and count == 0:
                    if ans_soup.text == '=':
                        # student use = for each step starting instead of LHS
                        iscontain_equals = ans_soup.text.strip()
                    else:
                        operator = ans_soup.text.strip()
                if '/mtable' in line:
                    if isfoundrow:
                        siz += len(mtrilist)
                        row_size = int(siz / col_size)
                        isfoundrow = false
                if 'mspace' in line:
                    step += 1
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
                        if re.search(r'\d', matrix_leftside):
                            ans_matrix = int(matrix_leftside[0:1]) * self.question[matrix_leftside[1:2]]
                            withoutcons_ans_matrix = self.question[matrix_leftside[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                # self.logger.info('your step is correct')
                                if multiplied and not gotSubsMark:
                                    # print('your mark for substitution ', self.scheme['substitution'])
                                    concept.append('your mark for substitution ' + str(self.scheme['substitution']))
                                    dataArray.append({"concept": "substitution", "details": "Correct",
                                                      "marksAwarded": self.scheme['substitution'], "step": step,
                                                      "totalMarks": self.scheme['substitution']}
                                                     )
                                    gotSubsMark = True
                                    marks += 1
                                if not multiplied and not gotMultipliedMark:
                                    # print('your mark for multiplication ', self.scheme['multiplication'])
                                    concept.append('your mark for multiplication ' + str(self.scheme['multiplication']))
                                    dataArray.append({"concept": "multiplication", "details": "Correct",
                                                      "marksAwarded": self.scheme['multiplication'], "step": step,
                                                      "totalMarks": self.scheme['multiplication']})
                                    gotMultipliedMark = True
                                    marks += 1
                                if middlesubs and not gotSubsMark:
                                    # print('your mark for substitution ', self.scheme['substitution'])
                                    concept.append('your mark for substitution '+ str(self.scheme['substitution']))
                                    dataArray.append({"concept": "substitution", "details": "Correct",
                                                      "marksAwarded": self.scheme['substitution'], "step": step,
                                                      "totalMarks": self.scheme['substitution']})
                                    gotSubsMark = True
                                    marks += 1
                                else:
                                    # if multiplied and not gotSubsMark:
                                    #     print('your mark for substitution ', self.scheme['substitution'])
                                    #     gotSubsMark = True
                                    #     marks += 1
                                    if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                        # print('your mark for multiplication ', self.scheme['multiplication'])
                                        concept.append ('your mark for multiplication '+ str(self.scheme['multiplication']))
                                        dataArray.append({"concept": "multiplication", "details": "Correct",
                                                      "marksAwarded": self.scheme['multiplication'], "step": step,
                                                      "totalMarks": self.scheme['multiplication']})
                                        gotMultipliedMark = True
                                        marks += 1
                                    if not gotSubsMark and gotMultipliedMark:
                                        # print('your mark for substitution ', self.scheme['substitution'])
                                        concept.append('your mark for substitution '+str(self.scheme['substitution']))
                                        dataArray.append({"concept": "substitution", "details": "Correct",
                                                          "marksAwarded": self.scheme['substitution'], "step": step,
                                                          "totalMarks": self.scheme['substitution']})
                                        gotSubsMark = True
                                        marks += 1
                                    # if middlesubs and not gotSubsMark:
                                    #     print('your mark for substitution ', self.scheme['substitution'])
                                    #     gotSubsMark = True
                                    #     marks += 1
                            else:
                                if (withoutcons_ans_matrix - Matrix(list)) == zeros(row_size, col_size):
                                    # print('you have forgotten to muliply by the constant ', matrix_leftside[0:1])
                                    errStep = step
                                    error_Identification.append ('you have forgotten to muliply by the constant '+ str(matrix_leftside[0:1]))
                                    break
                                if multiplied:
                                    # print('you have made mistake in substitution of ', matrix_leftside[1:2])
                                    errStep = step
                                    error_Identification.append('you have made mistake in substitution of '+ str(matrix_leftside[1:2]))
                                    break
                                if not multiplied:
                                    # print('you have made mistake in multiplication in calculation of ', matrix_leftside)
                                    errStep = step
                                    error_Identification.append('you have made mistake in multiplication in calculation of '+str(matrix_leftside))
                                    break
                                if middlesubs:
                                    # print('you have made mistake in substitution of ', matrix_leftside[1:2])
                                    errStep = step
                                    error_Identification.append('you have made mistake in substitution of '+str(matrix_leftside[1:2]))
                                    break
                                isShowErrMsg = false
                                # check only one row by the constant
                                # mulipliedonerow = false
                                # notmultipliedonerow = false
                                # num = 0
                                # # check only one row by the constant
                                # for k in range(ans_matrix.shape[0]):
                                #     l1 = ans_matrix.row(k)
                                #     if l1 == stu_ans.row(k):
                                #         mulipliedonerow = true
                                #         num += 1
                                # for k in range(withoutcons_ansmtrix.shape[0]):
                                #     l1 = withoutcons_ansmtrix.row(k)
                                #     if l1 == stu_ans.row(k):
                                #         notmultipliedonerow = true
                                #         num += 1
                                # if num == ans_matrix.shape[0]:
                                #     print('you have forgotten to multiply one or more row by constant ', matrix_question)
                                #     break
                                # num = 0
                                # for k in range(self.question[matrix_leftside[1:2]].shape[0]):
                                #     l1 = int(matrix_leftside[0:1]) * self.question[matrix_leftside[1:2]].row(k)
                                #     if l1 == Matrix(list).row(k):
                                #         num += 1
                                #         isShowErrMsg = true
                                # if isShowErrMsg:
                                #     print('you have multiplied correctly only ', num,' row by constant when calculating ',matrix_leftside)
                                #     break
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
                            withoutcons_ans_matrix = self.question[matrix_question[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                # self.logger.info('your step is correct')
                                if not multiplied and not gotMultipliedMark:
                                    # print('your mark for multiplication ', self.scheme['multiplication'])
                                    concept.append('your mark for multiplication '+ str(self.scheme['multiplication']))
                                    dataArray.append({"concept": "multiplication", "details": "Correct",
                                                      "marksAwarded": self.scheme['multiplication'], "step": step,
                                                      "totalMarks": self.scheme['multiplication']})
                                    gotMultipliedMark = True
                                    marks += 1
                            else:
                                if (withoutcons_ans_matrix - Matrix(list)) == zeros(row_size, col_size):
                                    # print('you have forgotten to muliply by the constant when finding step ', Matrix(list))
                                    errStep = step
                                    error_Identification.append('you have forgotten to muliply by the constant when finding step '+ str(Matrix(list)))
                                    break
                                numofcrctmuliplication = 0
                                # check for multiplication only first row by the constant
                                for k in range(ans_matrix.shape[0]):
                                    if k == 0:
                                        l1 = ans_matrix.row(k)
                                    if k != 0:
                                        for val in used:
                                            l2 = val.row(k)
                                            if k != 0 and l2 == stu_ans.row(k):
                                                numofcrctmuliplication += 1
                                    if k == 0 and l1 == stu_ans.row(0):
                                        numofcrctmuliplication += 1

                                if numofcrctmuliplication == ans_matrix.shape[0]:
                                    # print('your step ', Matrix(stu_ans),
                                    #       ' is wrong. you have multiplied only first row by constant')
                                    errStep = step
                                    error_Identification.append('your step '+str(Matrix(stu_ans))+' is wrong. you have multiplied only first row by constant')
                                    break
                                else:
                                    # print('you have made mistake in multiplication and your mistake is in ', Matrix(list))
                                    errStep = step
                                    error_Identification.append('you have made mistake in multiplication and your mistake is in '+ str(Matrix(list)))
                                    break
                    else:
                        withoutcons_ansmtrix = []
                        if len(twooperandsplitarray[0]) > 1:
                            matrix_1 = int(twooperandsplitarray[0][0:1]) * self.question[twooperandsplitarray[0][1:2]]
                            withoutcons_matrix1 = self.question[twooperandsplitarray[0][1:2]]
                        elif len(twooperandsplitarray[0]) <= 1:
                            matrix_1 = self.question[twooperandsplitarray[0]]
                            withoutcons_matrix1 = matrix_1
                        if len(twooperandsplitarray[1]) > 1:
                            matrix_2 = int(twooperandsplitarray[1][0:1]) * self.question[twooperandsplitarray[1][1:2]]
                            withoutcons_matrix_2 = self.question[twooperandsplitarray[0][1:2]]
                        elif len(twooperandsplitarray[1]) <= 1:
                            matrix_2 = self.question[twooperandsplitarray[1]]
                            withoutcons_matrix_2 = matrix_2
                        if iscontainplus:
                            ans_matrix = matrix_1 + matrix_2
                            inverseans_matrix = matrix_1 - matrix_2
                            withoutcons_ansmtrix.append(withoutcons_matrix1 + withoutcons_matrix_2)
                            withoutcons_ansmtrix.append(matrix_1 + withoutcons_matrix_2)
                            withoutcons_ansmtrix.append(withoutcons_matrix1 + matrix_2)
                        elif iscontainminus:
                            ans_matrix = matrix_1 - matrix_2
                            inverseans_matrix = matrix_1 + matrix_2
                            if withoutcons_matrix1 - withoutcons_matrix_2 != ans_matrix:
                                withoutcons_ansmtrix.append(withoutcons_matrix1 - withoutcons_matrix_2)
                            if matrix_1 - withoutcons_matrix_2 != ans_matrix:
                                withoutcons_ansmtrix.append(matrix_1 - withoutcons_matrix_2)
                            if withoutcons_matrix1 - matrix_2 != ans_matrix:
                                withoutcons_ansmtrix.append(withoutcons_matrix1 - matrix_2)
                            used = []
                            unique = [used.append(x) for x in withoutcons_ansmtrix if x not in used]
                        stu_ans_matr1 = list[0:row_size]
                    if operator:
                        stu_ans_matr2 = list[row_size:len(list)]
                        if str(operator).strip() == '+':
                            stu_ans = Matrix(stu_ans_matr1) + Matrix(stu_ans_matr2)
                            subs_matrix = ans_matrix - stu_ans
                            if subs_matrix == zeros(row_size, col_size):
                                # self.logger.info('your step is correct')
                                if multiplied and not gotSubsMark:
                                    # print('your mark for substitution ', self.scheme['substitution'])
                                    concept.append('your mark for substitution '+str(self.scheme['substitution']))
                                    dataArray.append({"concept": "substitution", "details": "Correct",
                                                      "marksAwarded": self.scheme['substitution'], "step": step,
                                                      "totalMarks": self.scheme['substitution']})
                                    gotSubsMark = True
                                    marks += 1
                                if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                    # print('your mark for multiplication ', self.scheme['multiplication'])
                                    concept.append('your mark for multiplication '+ str(self.scheme['multiplication']))
                                    dataArray.append({"concept": "multiplication", "details": "Correct",
                                                      "marksAwarded": self.scheme['multiplication'], "step": step,
                                                      "totalMarks": self.scheme['multiplication']})
                                    gotMultipliedMark = True
                                    marks += 1
                                if not gotSubsMark and gotMultipliedMark:
                                    # print('your mark for substitution ', self.scheme['substitution'])
                                    concept.append('your mark for substitution '+ str(self.scheme['substitution']))
                                    dataArray.append({"concept": "substitution", "details": "Correct",
                                                      "marksAwarded": self.scheme['substitution'], "step": step,
                                                      "totalMarks": self.scheme['substitution']})
                                    gotSubsMark = True
                                    marks += 1
                                if middlesubs and not gotSubsMark:
                                    # print('your mark for substitution ', self.scheme['substitution'])
                                    concept.append('your mark for substitution '+ str(self.scheme['substitution']))
                                    dataArray.append({"concept": "substitution", "details": "Correct",
                                                      "marksAwarded": self.scheme['substitution'], "step": step,
                                                      "totalMarks": self.scheme['substitution']})
                                    gotSubsMark = True
                                    marks += 1
                            else:
                                numofcrctmuliplication = 0
                                # check for multiplication only first row by the constant
                                for k in range(ans_matrix.shape[0]):
                                    if k == 0:
                                        l1 = ans_matrix.row(k)
                                    if k != 0:
                                        for val in used:
                                            l2 = val.row(k)
                                            if k != 0 and l2 == stu_ans.row(k):
                                                numofcrctmuliplication += 1
                                    if k == 0 and l1 == stu_ans.row(0):
                                        numofcrctmuliplication += 1

                                if numofcrctmuliplication == ans_matrix.shape[0]:
                                    # print('your step ', Matrix(stu_ans),
                                    #       ' is wrong. you have multiplied only first row by constant')
                                    errStep = step
                                    error_Identification.append('your step '+ str(Matrix(stu_ans))+ ' is wrong. you have multiplied only first row by constant')
                                    break
                                isShowErrMsg = false
                                for val in range(len(withoutcons_ansmtrix)):
                                    if val - stu_ans == zeros(row_size, col_size):
                                        # print('you have forgotten to muliply by the constant in ', stu_ans)
                                        errStep = step
                                        error_Identification.append('you have forgotten to muliply by the constant in '+ str(stu_ans))
                                        isShowErrMsg =true
                                        break
                                if isShowErrMsg:
                                    break
                                if multiplied:
                                    # print('you have made mistake in substitution and your mistake is ', twooperandsplitarray[0][1:2] + twooperandsplitarray[1][1:2])
                                    errStep = step
                                    error_Identification.append('you have made mistake in substitution and your mistake is ' +str(twooperandsplitarray[0][1:2]) + str(twooperandsplitarray[1][1:2]))
                                    break
                                if len(list) / row_size > 1 and not multiplied:
                                    # print('you have made mistake in multiplication when finding ', matrix_question)
                                    errStep = step
                                    error_Identification.append('you have made mistake in multiplication when finding '+ str(matrix_question))
                                    break
                                if middlesubs:
                                    # print('you have made mistake in substitution and ur mistake is in ', stu_ans)
                                    errStep = step
                                    error_Identification.append('you have made mistake in substitution and ur mistake is in '+ str(stu_ans))
                                    break
                        elif str(operator).strip() == '-':
                            stu_ans = Matrix(stu_ans_matr1) - Matrix(stu_ans_matr2)
                            subs_matrix = ans_matrix - stu_ans
                            if subs_matrix == zeros(row_size, col_size):
                                # self.logger.info('your step is correct')
                                if multiplied and not gotSubsMark:
                                    # print('your mark for substitution ', self.scheme['substitution'])
                                    concept.append('your mark for substitution '+ str(self.scheme['substitution']))
                                    dataArray.append({"concept": "substitution", "details": "Correct",
                                                      "marksAwarded": self.scheme['substitution'], "step": step,
                                                      "totalMarks": self.scheme['substitution']})
                                    gotSubsMark = True
                                    marks += 1
                                if len(list) / row_size > 1 and not multiplied and not gotMultipliedMark:
                                    # print('your mark for multiplication ', self.scheme['multiplication'])
                                    concept.append('your mark for multiplication '+ str(self.scheme['multiplication']))
                                    dataArray.append({"concept": "multiplication", "details": "Correct",
                                                      "marksAwarded": self.scheme['multiplication'], "step": step,
                                                      "totalMarks": self.scheme['multiplication']})
                                    gotMultipliedMark = True
                                    marks += 1
                                if not gotSubsMark and gotMultipliedMark:
                                    # print('your mark for substitution ', self.scheme['substitution'])
                                    concept.append('your mark for substitution '+ str(self.scheme['substitution']))
                                    dataArray.append({"concept": "substitution", "details": "Correct",
                                                      "marksAwarded": self.scheme['substitution'], "step": step,
                                                      "totalMarks": self.scheme['substitution']})
                                    gotSubsMark = True
                                    marks += 1
                                if middlesubs and not gotSubsMark:
                                    # print('your mark for substitution ', self.scheme['substitution'])
                                    concept.append('your mark for substitution '+ str(self.scheme['substitution']))
                                    dataArray.append({"concept": "substitution", "details": "Correct",
                                                      "marksAwarded": self.scheme['substitution'], "step": step,
                                                      "totalMarks": self.scheme['substitution']})
                                    gotSubsMark = True
                                    marks += 1
                            else:
                                numofcrctmuliplication = 0
                                # check for multiplication only first row by the constant
                                for k in range(ans_matrix.shape[0]):
                                    if k == 0:
                                        l1 = ans_matrix.row(k)
                                    if k != 0:
                                        for val in used:
                                            l2 = val.row(k)
                                            if k != 0 and l2 == stu_ans.row(k):
                                                numofcrctmuliplication += 1
                                    if k == 0 and l1 == stu_ans.row(0):
                                        numofcrctmuliplication += 1

                                if numofcrctmuliplication == ans_matrix.shape[0]:
                                    # print('your step ', Matrix(stu_ans), ' is wrong. you have multiplied only first row by constant')
                                    errStep = step
                                    error_Identification.append('your step '+ str(Matrix(stu_ans))+ ' is wrong. you have multiplied only first row by constant')
                                    break
                                isShowErrMsg = false
                                for val in used:
                                    if val - stu_ans == zeros(row_size, col_size):
                                        # print('you have forgotten to muliply by the constant when finding step ', Matrix(stu_ans))
                                        errStep = step
                                        error_Identification.append('you have forgotten to muliply by the constant when finding step ' + str(Matrix(stu_ans)))
                                        isShowErrMsg =true
                                        break
                                if isShowErrMsg:
                                    break
                                if multiplied:
                                    # print('you have made mistake in substitution ', stu_ans)
                                    errStep = step
                                    error_Identification.append('you have made mistake in substitution ' + str(stu_ans))
                                    break
                                if len(list) / row_size > 1 and not multiplied:
                                    # print('you have made mistake in multiplication when calculating ', matrix_question)
                                    errStep = step
                                    error_Identification.append('you have made mistake in multiplication when calculating '+ str(matrix_question))
                                    break
                                if middlesubs:
                                    # print('you have made mistake in substitution ', stu_ans)
                                    errStep = step
                                    error_Identification.append('you have made mistake in substitution ' + str(stu_ans))
                                    break
                    else:
                        subs_matrix = ans_matrix - Matrix(stu_ans_matr1)
                        if subs_matrix == zeros(row_size, col_size):
                            # self.logger.info('your step is correct')
                            if len(list) / row_size == 1 and not gotFinalStepMark and not middlesubs:
                                if iscontainminus:
                                    # print('your mark for subtraction ', self.scheme['subtraction'])
                                    concept.append('your mark for subtraction '+ str(self.scheme['subtraction']))
                                    dataArray.append({"concept": "subtraction", "details": "Correct",
                                                      "marksAwarded": self.scheme['subtraction'], "step": step,
                                                      "totalMarks": self.scheme['subtraction']})
                                    marks += 1
                                    gotFinalStepMark = true
                                else:
                                    # print('your mark for addition ', self.scheme['addition'])
                                    concept.append('your mark for addition '+ str(self.scheme['addition']))
                                    dataArray.append({"concept": "addition", "details": "Correct",
                                                      "marksAwarded": self.scheme['addition'], "step": step,
                                                      "totalMarks": self.scheme['addition']})
                                    gotFinalStepMark = True
                                    marks += 1
                            if not gotMultipliedMark:
                                # print('your mark for multiplication ', self.scheme['multiplication'])
                                concept.append('your mark for multiplication '+ str(self.scheme['multiplication']))
                                dataArray.append({"concept": "multiplication", "details": "Correct",
                                                  "marksAwarded": self.scheme['multiplication'], "step": step,
                                                  "totalMarks": self.scheme['multiplication']})
                                gotMultipliedMark = True
                                marks += 1
                            if not gotSubsMark:
                                # print('your mark for substitution ', self.scheme['substitution'])
                                concept.append('your mark for substitution '+ str(self.scheme['substitution']))
                                dataArray.append({"concept": "substitution", "details": "Correct",
                                                  "marksAwarded": self.scheme['substitution'], "step": step,
                                                  "totalMarks": self.scheme['substitution']})
                                gotSubsMark = True
                                marks += 1
                        else:
                            temp = Matrix(stu_ans_matr1)
                            list1 = np.matrix(inverseans_matrix).tolist()
                            list2 = np.matrix(temp).tolist()
                            list3 = np.matrix(ans_matrix).tolist()
                            isShowErrMsg = false
                            numofcrctmuliplication = 0
                            # check for multiplication only first row by the constant
                            for k in range(ans_matrix.shape[0]):
                                if k == 0:
                                    l1 = ans_matrix.row(k)
                                if k != 0:
                                    for val in used:
                                        l2 = val.row(k)
                                        if k != 0 and l2 == Matrix(stu_ans_matr1).row(k):
                                            numofcrctmuliplication += 1
                                if k == 0 and l1 == Matrix(stu_ans_matr1).row(0):
                                    numofcrctmuliplication += 1

                            if numofcrctmuliplication == ans_matrix.shape[0]:
                                errStep = step
                                error_Identification.append('your step '+ str(Matrix(stu_ans_matr1)) + ' is wrong. you have multiplied only first row by constant')
                                # print('your step ', Matrix(stu_ans_matr1), ' is wrong. you have multiplied only first row by constant')
                                break
                            for val in used:
                                if val - Matrix(stu_ans_matr1) == zeros(row_size, col_size):
                                    errStep = step
                                    error_Identification.append('you have forgotten to muliply by the constant when finding step ' + str(Matrix(stu_ans_matr1)))
                                    # print('you have forgotten to muliply by the constant when finding step ', Matrix(stu_ans_matr1))
                                    isShowErrMsg = true
                                    break
                            if isShowErrMsg:
                                break
                            for element in range(len(list1)):
                                l1 = list1.pop()
                                l2 = list2.pop()
                                l3 = list3.pop()
                                for val in range(len(list1)):
                                    for value in range(len(l1)):
                                        element_val1 = l1.pop()
                                        element_val2 = l3.pop()
                                        if element_val1 == l2.pop() and element_val1 != element_val2:
                                            errStep = step
                                            error_Identification.append('you have done addition instead of subtraction when finding '+ str(Matrix(stu_ans_matr1)))
                                            # print('you have done addition instead of subtraction when finding ', Matrix(stu_ans_matr1))
                                            isShowErrMsg = true
                                            break
                            if isShowErrMsg:
                                break
                            if len(list) / row_size == 1 and not middlesubs:
                                if iscontainminus:
                                    errStep = step
                                    error_Identification.append('Your step ' + str(Matrix(stu_ans_matr1)) + ' is wrong.  you have made mistake in subtraction when finding '+ str(matrix_question))
                                    # print('Your step ', Matrix(stu_ans_matr1),' is wrong.', ' you have made mistake in subtraction when finding ', matrix_question)
                                    break
                                else:
                                    errStep = step
                                    error_Identification.append('you have made mistake in addition when finding '+ str(Matrix(stu_ans_matr1)))
                                    # print('you have made mistake in addition when finding ', Matrix(stu_ans_matr1))
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
            if not dataArray:
                data = {"studentTotal": marks, "errStep":errStep, "maxMarks":self.scheme['totalmarks'], "error_identification":error_Identification}
            elif not error_Identification:
                data = {"studentTotal": marks, "maxMarks":self.scheme['totalmarks'], "concepts":dataArray}
            else:
                data = {"studentTotal": marks, "errStep":errStep, "maxMarks":self.scheme['totalmarks'], "concepts":dataArray, "error_identification":error_Identification}

            print(json.dumps(data))

            # print('your final marks is ', marks, 'out of ',self.scheme['totalmarks'])
        time.sleep(0.1)
        self.logger.info('Finish answer reading')
