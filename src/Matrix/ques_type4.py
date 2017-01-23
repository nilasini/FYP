from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *

class Question(Logs):

    x = ''
    y = ''
    col_size = None
    row_size = None

    def __init__(self,question_file,logger):
        self.question_file = question_file
        self.logger = logger

    def readQuestion(self):
        global x, y


        matri_right = []
        matri_left = []
        operator_left = []
        operator_right = []
        siz = 0
        lhs_dict = {}
        r = 0
        matri_right_var = []
        matri_left_var = []
        isOperator = false
        operator = ''
        isfoundcol = true
        isfoundrow = true

        # open the question file
        filein = open(self.question_file)
        i = 0
        j = 0
        self.logger.info('Reading question')
        # parse the question
        for line in filein:
            soup = BeautifulSoup(line, "html.parser")
            if 'mi' in line and 'mtd' not in line:
                temp = soup.text
                if r == 0:
                    matri_left_var.insert(i, temp)
                    # if isOperator:
                    #     matri_left_var.insert(i + 1, operator)
                    #     isOperator = false
                else:
                    matri_right_var.insert(i, temp)
                    # if isOperator:
                    #     matri_right_var.insert(i + 1, operator)
                    #     isOperator = false
            if 'mn' in line:
                if r == 0:
                    matri_left.insert(i, soup.text)
                else:
                    matri_right.insert(i, soup.text)
            if '/mo' in line:
                if '=' in soup.text:
                    r = 1
                else:
                   # if matri_left_var:
                   #     matri_left_var.insert(i, soup.text)
                   # else:
                   if r==0:
                       operator_left = soup.text
                       lhs_dict['operator_left'] = operator_left.strip()
                   else:
                       operator_right  = soup.text
                       lhs_dict['operator_right'] = operator_right.strip()
                       # isOperator = true
            if '/mtr' in line and isfoundcol:
                if len(matri_left) > 0:
                    Question.col_size = len(matri_left)
                    isfoundcol = false
                elif len(matri_right) > 0:
                    Question.col_size = len(matri_right)
                    isfoundcol = false
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
                if len(matri_right) and isfoundrow:
                    siz += len(matri_right)
                    Question.row_size = int(siz / Question.col_size)
                    isfoundrow = false
                elif len(matri_left) and isfoundrow:
                    siz += len(matri_left)
                    Question.row_size = int(siz / Question.col_size)
                    isfoundrow = false
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
                r = 0
            i += 1
        self.logger.info('Finish question reading')
        return lhs_dict