from logging import INFO

from bs4 import BeautifulSoup
from sympy import *
import re
import logging

col_size = None
row_size = None

logging.basicConfig(level=INFO)
log_name = 'logs'
logger = logging.getLogger(log_name)


class MatrixAnswers:
    @staticmethod
    def read_question():
        global col_size, row_size
        isfound = true
        isfoundrow = true
        mtrilist = []
        matri_name = []
        siz = 0
        lhs_dict = {}

        filein = open('question1.html')
        i = 0
        logger.info('Reading question')
        for line in filein:
            soup = BeautifulSoup(line, "html.parser")
            if 'mi' in line:
                temp = soup.text
                matri_name.insert(0, temp)
            if 'mn' in line:
                mtrilist.insert(i, int(soup.text))
            if '/mtr' in line and isfound:
                col_size = len(mtrilist)
                isfound = false
            if '/mtable' in line:
                if isfoundrow:
                    siz += len(mtrilist)
                    row_size = int(siz / col_size)
                    isfoundrow = false
                list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                A = Matrix(list)
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

        ques = MatrixAnswers().read_question()
        logger.info('Reading answers')
        with open('Answer1.html') as answer:
            i = 0
            for line in answer:
                ans_soup = BeautifulSoup(line, "html.parser")
                if 'mi' in line:
                    temp = ans_soup.text
                    matri_name.insert(0, temp)
                    count += 1
                if 'mfenced' in line:
                    count = 0
                if 'mn' in line:
                    mtrilist.insert(i, int(ans_soup.text))
                if '/mtr' in line and isfound:
                    col_size = len(mtrilist)
                    isfound = false
                if '/mo' in line and count > 0:
                    matri_name.insert(0, ans_soup.text)
                if '/mtable' in line:
                    if isfoundrow:
                        siz += len(mtrilist)
                        row_size = int(siz / col_size)
                        isfoundrow = false
                    list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                # check whether the lefthand elements contains numbers with variables. Eg:2A
                if matri_name and list:
                    length = len(matri_name)
                    iscontainplus = false
                    iscontainminus = false
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
                        elif len(twooperandsplitarray[0]) < 1:
                            matrix_1 = ques[twooperandsplitarray[0]]
                        if len(twooperandsplitarray[1]) > 1:
                            matrix_2 = int(twooperandsplitarray[1][0:1]) * ques[twooperandsplitarray[1][1:2]]
                        elif len(twooperandsplitarray[1]) < 1:
                            matrix_2 = ques[twooperandsplitarray[1]]

                        if iscontainplus:
                            ans_matrix = matrix_1 + matrix_2
                        elif iscontainminus:
                            ans_matrix = matrix_1 - matrix_2
                        subs_matrix = ans_matrix - Matrix(list)
                        if subs_matrix == zeros(row_size, col_size):
                            logger.info('your answer is correct')
                        list.clear()
                        mtrilist.clear()
                        isfound = true
                        isfoundrow = true
                        matri_name.clear()
                        siz = 0
                        count = 0
                    else:
                        matrix_leftside = matri_name.pop().strip()
                        if re.search(r'\d', matrix_leftside):
                            simpleleftmatrix = int(matrix_leftside[0:1]) * ques[matrix_leftside[1:2]]
                            subs_matrix = simpleleftmatrix - Matrix(list)
                            if subs_matrix == zeros(row_size, col_size):
                                logger.info('your answer is correct')
                            list.clear()
                            mtrilist.clear()
                            isfound = true
                            isfoundrow = true
                            matri_name.clear()
                            siz = 0
                            count = 0
                i += 1
        logger.info('finish answer reading')
        answer.close()

MatrixAnswers().mark()
