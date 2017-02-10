from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *


class Question(Logs):

    col_size = None
    row_size = None

    def __init__(self, question_file, logger):
        self.question_file = question_file
        self.logger = logger

    def readquestion(self):

        # open the question file
        filein = open(self.question_file)
        self.logger.info('Reading question')
        lhs = self.read(filein)  # read and parse the question for type 4
        self.logger.info('Finish question reading')
        return lhs

    def read(self, filein):
        matri_right = []  # store right hand side values
        matri_left = []  # store left hand side values
        lhs_dict = {}  # store question in a dictionary
        isequalfound = false  # check whether equal sign has find or not
        matri_right_var = []  # store right hand side variable matrix
        matri_left_var = []  # store left hand side variable matrix
        isfoundcol = false  # check whether column size has found
        isfoundrow = false  # check whether row size has found
        global col_size, row_size
        i = 0
        for line in filein:
            soup = BeautifulSoup(line, "html.parser")
            if 'mi' in line and 'mtd' not in line:  # check for matrix variables
                temp = soup.text
                if not isequalfound:  # check whether variable is in RHS or LHS
                    matri_left_var.insert(i, temp)
                else:
                    matri_right_var.insert(i, temp)
            if 'mn' in line:
                if not isequalfound:  # check for numbers within matrix
                    matri_left.insert(i, soup.text)
                else:
                    matri_right.insert(i, soup.text)
            if '/mo' in line:
                if '=' in soup.text:
                    isequalfound = true
                else:
                     if not isequalfound:
                       operator_left = soup.text
                       lhs_dict['operator_left'] = operator_left.strip()
                     else:
                       operator_right  = soup.text
                       lhs_dict['operator_right'] = operator_right.strip()
            if '/mtr' in line and not isfoundcol:
                if len(matri_left) > 0:
                    Question.col_size = len(matri_left)
                    isfoundcol = true
                elif len(matri_right) > 0:
                    Question.col_size = len(matri_right)
                    isfoundcol = true
            if '/math' in line and len(matri_left_var) > 0:
                question = matri_left_var.pop().strip()
                lhs_dict['ques'] = question
                temp = []
                n = 0
                if len(matri_left_var) > 0:
                    for element in matri_left_var:
                        temp.insert(n, element.strip())
                        n+=1
                    lhs_dict['left_var'] = temp
                elif len(matri_right_var) > 0:
                    for element in matri_right_var:
                         temp += matri_right_var.pop().strip()
                    lhs_dict['rigth_var'] = temp

            if '/mtable' in line:
                if len(matri_right) and not isfoundrow:
                    siz = len(matri_right)
                    Question.row_size = int(siz / Question.col_size)
                    isfoundrow = true
                elif len(matri_left) and not isfoundrow:
                    siz = len(matri_left)
                    Question.row_size = int(siz / Question.col_size)
                    isfoundrow = true
                length_l = len(matri_left)
                lenght_r = len(matri_right)
                if length_l > 0:
                    list_l = [matri_left[x:x + Question.col_size] for x in range(0, len(matri_left), Question.col_size)]
                    M = Matrix(list_l)
                    lhs_dict['left'] = M
                if lenght_r > 0:
                    list_r = [matri_right[x:x + Question.col_size] for x in range(0, len(matri_right), Question.col_size)]
                    M = Matrix(list_r)
                    lhs_dict['right'] = M

                matri_right.clear()
                matri_left.clear()
            if 'mspace' in line:
                isequalfound = false
            i += 1
        return lhs_dict