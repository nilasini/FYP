from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *

class Question(Logs):
    col_size = None
    row_size = None

    x = ''
    y = ''

    def __init__(self,question_file,logger):
        self.question_file = question_file
        self.logger = logger

    def readQuestion(self):
        global col_size, row_size, x, y
        isfound = True
        isfoundrow = True
        mtrilist = []
        matri_name = []
        question = ''
        siz = 0
        count = 0
        lhs_dict = {}

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
        self.logger.info('Finish question reading')
        return lhs_dict