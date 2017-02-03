from bs4 import BeautifulSoup
from sympy import *
import re

# row_size = 2
# col_size = 2
col_size = None
row_size = None


class MatrixAnswers:
    def read_question(self):
        global col_size, row_size
        isfound = true
        isfoundrow = true
        mtrilist = []
        matri_name = []
        siz = 0
        lhs_dict = {}

        filein = open('Question_MathML')
        i = 0
        for line in filein:
            soup = BeautifulSoup(line, "html.parser")
            if not 'mtd' in line and 'mi' in line:
                temp = soup.text
                matri_name.insert(0, temp)
            if 'mtd' in line:
                mtrilist.insert(i, int(soup.text))
            if '/mtr' in line and isfound:
                col_size = len(mtrilist)
                print('col size ', col_size)
                isfound = false
            if '/mtable' in line:
                if isfoundrow:
                    siz += len(mtrilist)
                    row_size = int(siz / col_size)
                    isfoundrow = false
                    print('row sixe ', row_size)
                list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                A = Matrix((list))
                lhs_dict[matri_name.pop().strip()] = A
                mtrilist.clear()
            # if 'mo' in line:
            #     print('operator ', soup.text)
            i += 1
        print('distion ', lhs_dict)
        return lhs_dict

    def mark(self):
        isfound = true
        isfoundrow = true
        mtrilist = []
        matri_name = []
        siz = 0
        lhs_dict = {}
        ques = MatrixAnswers().read_question()
        print('question ', ques)
        with open('Answer_MathML') as answer:
            # i = 0
            # for line in answer:
            #     # remove empty lines
            #     if line.strip():
            #         splitted_array = line.split('=')
            #         matrix = [int(s) for s in re.findall(r'[+-]?[0-9][0-9]?', splitted_array[1])]
            #         matrix_name = splitted_array[0].strip()
            #         list = [matrix[x:x + 2] for x in range(0, len(matrix), 2)]
            i = 0
            for line in answer:
                ans_soup = BeautifulSoup(line, "html.parser")
                if not 'mtd' in line and 'mi' in line:
                    temp = ans_soup.text
                    matri_name.insert(0, temp)
                if 'mtd' in line:
                    mtrilist.insert(i, int(ans_soup.text))
                if '/mtr' in line and isfound:
                    col_size = len(mtrilist)
                    print('col size ', col_size)
                    isfound = false
                if '/mtable' in line:
                    if isfoundrow:
                        siz += len(mtrilist)
                        row_size = int(siz / col_size)
                        isfoundrow = false
                        print('row sixe ', row_size)
                    list = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                    A = Matrix((list))
                    lhs_dict[matri_name.pop().strip()] = A
                    mtrilist.clear()
                # if 'mo' in line:
                #     print('operator ', ans_soup.text)
                i += 1
                    # check whether the lefthand elements contains numbers with variables. Eg:2A
                    if re.search(r'\d', matrix_name) and len(matrix_name) < 3:
                        simpleleftmatrix = int(matrix_name[0:1]) * ques[matrix_name[1:2]]
                        print('simpleleftmatrix ', simpleleftmatrix)
                        print(' Matrix((list)) ', list)
                        # D = Matrix(list)
                        subs_matrix = simpleleftmatrix - Matrix((list))
                        if subs_matrix == zeros(2, 2):
                            print('correct')
                        # check whether left hand side contain operand
                    elif re.search(r'\+|\-', matrix_name):
                        operand = re.findall(r'\+|\-', matrix_name)
                        twooperandsplitarray = matrix_name.split('-')
                        matrix_g = None
                        for elements in twooperandsplitarray:
                            if len(elements) > 1:
                                matrix_g = int(elements[0:1]) * ques[elements[1:2]]
                            else:
                                if matrix_g is None:
                                    print('svdsv')
                                else:
                                    if '+' in operand:
                                        leftsidewithoperand = matrix_g + ques[elements[0:1]]
                                    else:
                                        leftsidewithoperand = matrix_g - ques[elements[0:1]]
                            subsans = leftsidewithoperand - Matrix((list))
                            # if subsans
                    i += 1

        answer.close()

MatrixAnswers().mark()
