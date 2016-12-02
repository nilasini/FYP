from logging import INFO

import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
from sympy import *
import re
import logging

col_size = None
row_size = None

x = ''
y = ''

logging.basicConfig(level=INFO)
log_name = 'logs'
logger = logging.getLogger(log_name)


class MatrixAnswers:
    @staticmethod
    def read_question():
        global col_size, row_size, x, y
        isfound = true
        isfoundrow = true
        mtrilist = []
        matri_name = []
        question = ''
        siz = 0
        count = 0
        lhs_dict = {}
        filein = open('question2.html')
        i = 0
        j = 0
        logger.info('Reading question')

        # tree = ET.ElementTree(file=filein)
        # print('rrot is ', tree.getroot())
        # root = tree.getroot()
        # # print("tag=%s, attrib=%s" % (root.tag, root.attrib))
        #
        # for child in root:
        #     print(child.tag,child)
        #     if child.tag == "mfenced":
        #         for step_child in child:
        #             print(step_child.attrib)

        for line in filein:
            soup = BeautifulSoup(line, "html.parser")
            if 'mi' in line and 'mtd' not in line:
                temp = soup.text
                matri_name.insert(0, temp)
                count += 1
            if 'mn' in line:
                mtrilist.insert(i, soup.text)
            if 'mtd' in line and 'mi' in line:
                if j == 0:
                    x = symbols(soup.text)
                    j += 1
                else:
                    y = symbols(soup.text)
                mtrilist.insert(i, soup.text)
            if '/mtr' in line and isfound:
                col_size = len(mtrilist)
                isfound = false
            if 'mfenced' in line:
                count = 0
            if '/mo' in line and count > 0:
                if '=' not in soup.text:
                    matri_name.insert(0, soup.text)
            if '/math' in line and len(matri_name) > 0:
                for d in range(0, len(matri_name)):
                    question += matri_name.pop().strip()
                lhs_dict['ques'] = question
            if '/mtable' in line:
                if isfoundrow:
                    siz += len(mtrilist)
                    row_size = int(siz / col_size)
                    isfoundrow = false
                length = len(matri_name)
                matrix_leftside = ''
                list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                A = Matrix(list)
                if length > 2:
                    for d in range(0, length):
                        matrix_leftside += matri_name.pop().strip()
                    lhs_dict[matrix_leftside.strip()] = A
                else:
                    lhs_dict[matri_name.pop().strip()] = A
                mtrilist.clear()
            i += 1
        logger.info('Finish question reading')
        return lhs_dict

    @staticmethod
    def mark():
        isfound = true
        isfoundrow = true
        mtrilist = []
        matri_name = []
        list = []
        siz = 0
        count = 0
        ispassfenced = false
        iscontain_var = false
        iscontain_equals = false
        global x, y
        sign = None
        old_ans_matrix = None
        ans_matrix = None

        ques = MatrixAnswers().read_question()
        logger.info('Reading answers')
        with open('Answer3.html') as answer:
            i = 0
            for line in answer:
                ans_soup = BeautifulSoup(line, "html.parser")
                if 'mi' in line and 'mtd' not in line and not ispassfenced:
                    temp = ans_soup.text
                    matri_name.insert(0, temp)
                    count += 1
                if 'mfenced' in line:
                    count = 0
                    ispassfenced = true
                if '/mfenced' in line:
                    ispassfenced = false
                if 'mn' in line:
                        mtrilist.insert(i, ans_soup.text)
                        if 'x' in ans_soup.text or 'y' in ans_soup.text:
                            iscontain_var = true
                if '/mtr' in line and isfound:
                    col_size = len(mtrilist)
                    isfound = false
                if '/mo' in line and count > 0:
                    if '=' not in ans_soup.text:
                        matri_name.insert(0, ans_soup.text)
                        sign = ans_soup.text
                if '/mo' in line and count == 0:
                    if ans_soup.text == '=':
                        iscontain_equals = ans_soup.text
                if '/mtable' in line:
                    if isfoundrow:
                        siz += len(mtrilist)
                        row_size = int(siz / col_size)
                        isfoundrow = false
                if '/mfenced' in line:
                    list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                # check whether the lefthand elements contains numbers with variables. Eg:2A
                iscontainplus = false
                iscontainminus = false
                if matri_name and list:
                    length = len(matri_name)
                    matrix_leftside = ''

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
                            matrix_1 = int(twooperandsplitarray[0][0:1]) * ques[twooperandsplitarray[0][1:2]]
                        elif len(twooperandsplitarray[0]) <= 1:
                            matrix_1 = ques[twooperandsplitarray[0]]
                        if len(twooperandsplitarray[1]) > 1:
                            matrix_2 = int(twooperandsplitarray[1][0:1]) * ques[twooperandsplitarray[1][1:2]]
                        elif len(twooperandsplitarray[1]) <= 1:
                            matrix_2 = ques[twooperandsplitarray[1]]

                        if iscontainplus:
                            ans_matrix = matrix_1 + matrix_2
                        elif iscontainminus:
                            ans_matrix = matrix_1 - matrix_2
                        if len(list)==row_size:
                            subs_matrix = ans_matrix - Matrix(list)
                        else:
                            stu_ans_matr1 = list[0:row_size]
                            stu_ans_matr2 = list[row_size:len(list)]
                            if iscontainplus:
                                stu_ans = Matrix(stu_ans_matr1) + Matrix(stu_ans_matr2)
                            elif iscontainminus:
                                print('list ', list)
                                print('stu_ans_matr1 ', stu_ans_matr1)
                                print('stu_ans_matr2 ', stu_ans_matr2)
                                stu_ans = Matrix(stu_ans_matr1) - Matrix(stu_ans_matr2)
                            subs_matrix = ans_matrix - stu_ans
                        if subs_matrix == zeros(row_size, col_size):
                            logger.info('your step is correct')
                        list.clear()
                        mtrilist.clear()
                        isfound = true
                        isfoundrow = true
                        old_ans_matrix = ans_matrix
                        matri_name.clear()
                        siz = 0
                        count = 0
                        iscontain_var = false
                    else:
                        matrix_leftside = matri_name.pop().strip()
                        if re.search(r'\d', matrix_leftside):
                            ans_matrix = int(matrix_leftside[0:1]) * ques[matrix_leftside[1:2]]
                            subs_matrix = ans_matrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                logger.info('your step is correct')
                            list.clear()
                            mtrilist.clear()
                            isfound = true
                            isfoundrow = true
                            old_ans_matrix = ans_matrix
                            matri_name.clear()
                            siz = 0
                            count = 0
                            iscontain_var = false

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
                            logger.info('your step is correct')
                        list.clear()
                        mtrilist.clear()
                        isfound = true
                        isfoundrow = true
                        old_ans_matrix = ans_matrix
                        matri_name.clear()
                        siz = 0
                        count = 0
                        iscontain_var = false
                    else:
                        matrix_leftside = ques['ques']
                        if "-" in matrix_leftside:
                            iscontainminus = true
                            # split the left hand side using -
                            twooperandsplitarray = matrix_leftside.split('-')
                        elif "+" in matrix_leftside:
                            iscontainplus = true
                            # split the left hand side using +
                            twooperandsplitarray = matrix_leftside.split('+')
                        if len(twooperandsplitarray[0]) > 1:
                            matrix_1 = int(twooperandsplitarray[0][0:1]) * ques[twooperandsplitarray[0][1:2]]
                        elif len(twooperandsplitarray[0]) <= 1:
                            matrix_1 = ques[twooperandsplitarray[0]]
                        if len(twooperandsplitarray[1]) > 1:
                            matrix_2 = int(twooperandsplitarray[1][0:1]) * ques[twooperandsplitarray[1][1:2]]
                        elif len(twooperandsplitarray[1]) <= 1:
                            matrix_2 = ques[twooperandsplitarray[1]]

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
                            logger.info('your step is correct')
                        list.clear()
                        mtrilist.clear()
                        isfound = true
                        isfoundrow = true
                        old_ans_matrix = ans_matrix
                        matri_name.clear()
                        siz = 0
                        count = 0
                        iscontain_var = false
                i += 1
        logger.info('finish answer reading')
        answer.close()

MatrixAnswers().mark()