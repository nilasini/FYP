# this class can solves matrix questions which have matrix with variables

from sympy import *
import re
import logging


class Solver:

    def solve(self):
        global leftsidewithoperand, leftsidewithoperand
        logging.basicConfig(level=logging.INFO)
        log_name = "logs"
        logger = logging.getLogger(log_name)
        x = Symbol('x')
        y = Symbol('y')
        #question 1
        # A = Matrix(([2, 0], [3, 1]))
        # B = Matrix(([4, 3], [5, 2]))

        # A = Matrix(([3, 2, 4], [0, 1, 5]))
        # B = Matrix(([x, 4, 8], [0, 3, y]))
        # C = Matrix(([1, 0, 0], [0, -1, 0]))

        # A = Matrix(([3, 2], [4, 0], [5, 1]))
        # B = Matrix(([2, 1], [x, 0], [-1, y]))
        # C = Matrix(([8, 5], [5, 0], [9, 5]))

        # A = Matrix(([3, 2, 4], [0, 1, 5]))
        # B = Matrix(([x, 4, 8], [0, 3, y]))
        # C = Matrix(([1, 0, 0], [0, -1, 0]))

        A = Matrix(([2, 1], [-3, 2]))
        B = Matrix(([0, 3], [-1, -3]))
        rowsizea = A.rows
        colsizea = A.cols
        answerofy = 0
        answerofx = 0
        simpleleftmatrix = None
        arrayofright = None
        leftsidewithoperand = None
        remainrowsize = rowsizea - 1
        arrayfirstrow = [] * colsizea
        with open('sampleFile.txt') as filein:
            i = 0
            for line in filein:
                # remove all empty lines
                if line.strip():
                    is_wrong_ans = false
                    # check whether it is first row of a matrix
                    if "=" in line:
                        nextrow = [[0] * colsizea for y in range(remainrowsize)]
                        arraynextrows = [[0] * colsizea for y in range(remainrowsize)]
                        # check lefthand equation operand
                        iscontainminus = false
                        iscontainplus = false
                        # split the first row using '='
                        arrayStr = line.split('=')
                        # extract the leftelement
                        leftelement = arrayStr.pop(0).strip()
                        # check whether the lefthand elements contains numbers with variables. Eg:2A
                        if re.search(r'\d', leftelement) and len(leftelement) < 3:
                            rightelement = arrayStr.pop(0)
                            arrayofright = rightelement.split()


                            # calculate the left side using sympy
                            if leftelement[1:2] == "A":
                                simpleleftmatrix = int(leftelement[0:1]) * A
                            elif leftelement[1:2] == "B":
                                simpleleftmatrix = int(leftelement[0:1]) * B

                        #check whether left hand side contain operand
                        else:
                            if "-" in leftelement:
                                iscontainminus = true
                                # split the left hand side using -
                                twooperandsplitarray = leftelement.split('-')
                            elif "+" in leftelement:
                                iscontainplus = true
                                # split the left hand side using -
                                twooperandsplitarray = leftelement.split('+')

                            # get the right hand side elements of the first row of the matrix
                            rightelement = arrayStr.pop(0)
                            arrayofright = rightelement.split()

                            for elements in twooperandsplitarray:
                                if len(elements) > 1:
                                    if "A" in elements:
                                        matix_g = int(elements[0:1]) * A
                                    if "B" in elements:
                                        matix_g = int(elements[0:1]) * B

                                # find the lefhand side matrix which contains operand using sympy
                                elif "A" in elements and iscontainminus:
                                    leftsidewithoperand = matix_g - A
                                    for val in leftsidewithoperand:
                                        iscontainx = false
                                        iscontainy = false
                                        if len(str(val)) > 1:
                                            if "x" in str(val) or str(val) == "x":
                                                iscontainx = true
                                            if "y" in str(val) or str(val) == "y":
                                                iscontainy = true
                                    if iscontainx and iscontainy:
                                        logger.info('x and y is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), x, y)
                                        answerofx = answers.pop(x)
                                        answerofy = answers.pop(y)
                                    elif iscontainx:
                                        logger.info('x only is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), x)
                                        answerofx = answers.pop(x)
                                    elif iscontainy:
                                        logger.info('y only is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), y)
                                        answerofy = answers.pop(y)
                                    else:
                                        answers = solve(C - leftsidewithoperand)
                                elif "A" in elements and iscontainplus:
                                    leftsidewithoperand = matix_g + A
                                    for val in leftsidewithoperand:
                                        iscontainx = false
                                        iscontainy = false
                                        if len(str(val)) > 1:
                                            if "x" in str(val) or str(val) == "x":
                                                iscontainx = true
                                            if "y" in str(val) or str(val) == "y":
                                                iscontainy = true
                                    if iscontainx and iscontainy:
                                        logger.info('x and y is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), x, y)
                                        answerofx = answers.pop(x)
                                        answerofy = answers.pop(y)
                                    elif iscontainx:
                                        logger.info('x only is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), x)
                                        answerofx = answers.pop(x)
                                    elif iscontainy:
                                        logger.info('y only is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), y)
                                        answerofy = answers.pop(y)
                                    else:
                                        answers = solve(C - leftsidewithoperand)
                                elif "B" in elements and iscontainminus:
                                    leftsidewithoperand = matix_g - B
                                    iscontainx = false
                                    iscontainy = false
                                    for val in leftsidewithoperand:
                                        if len(str(val)) > 1:
                                            if "x" in str(val) or str(val) == "x":
                                                iscontainx = true
                                            if "y" in str(val) or str(val) == "y":
                                                iscontainy = true
                                    if iscontainx and iscontainy:
                                        logger.info('x and y is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), x, y)
                                        if len(answers) < 1:
                                            logger.info('trying wrong answer')
                                            is_wrong_ans = true
                                        else:
                                            answerofx = answers.pop(x)
                                            answerofy = answers.pop(y)
                                    elif iscontainx:
                                        logger.info('x only is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), x)
                                        answerofx = answers.pop(x)
                                    elif iscontainy:
                                        logger.info('y only is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), y)
                                        answerofy = answers.pop(y)
                                    else:
                                        simpleleftmatrix = leftsidewithoperand
                                elif "B" in elements and iscontainplus:
                                    leftsidewithoperand = matix_g + B
                                    for val in leftsidewithoperand:
                                        iscontainx = false
                                        iscontainy = false
                                        if len(str(val)) > 1:
                                            if "x" in str(val) or str(val) == "x":
                                                iscontainx = true
                                            if "y" in str(val) or str(val) == "y":
                                                iscontainy = true
                                    if iscontainx and iscontainy:
                                        logger.info('x and y is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), x, y)
                                        answerofx = answers.pop(x)
                                        answerofy = answers.pop(y)
                                    elif iscontainx:
                                        logger.info('x only is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), x)
                                        answerofx = answers.pop(x)
                                    elif iscontainy:
                                        logger.info('y only is in the leftsidewithoperand ')
                                        answers = solve((C - leftsidewithoperand), y)
                                        answerofy = answers.pop(y)
                                    else:
                                        answers = solve(C - leftsidewithoperand)
                    else:
                        if i <= rowsizea:
                            temporary = line.split()
                            for k in range(len(temporary)):
                                nextrow[i - 1][k] = temporary[k]
                    i += 1
                    if i == rowsizea:
                        i = 0
                        logger.info('complete one matrix')
                        check_with_variable = false
                        if not is_wrong_ans:
                            for element in arrayofright:
                                if "x" in element or "y" in element:
                                    check_with_variable = true
                            for j in range(0, len(nextrow)):
                                print(' nextrow[j] ', nextrow[j])
                                for n in range(0,len(nextrow[j])):
                                    iscontainvariable = false
                                    if 'y' in elements or 'x' in elements:
                                        iscontainvariable = true
                                        break
                                if iscontainvariable:
                                    arraynextrows[j] = self.variable_contains(nextrow[j], answerofx, answerofy, colsizea)
                                    check_with_variable = true
                                else:
                                    for k in range(len(nextrow[j])):
                                        arraynextrows[j][k] = int(nextrow[j][k])
                            if check_with_variable:
                                # get the first row of the matrix as integer
                                arrayfirstrow = self.variable_contains(arrayofright, answerofx, answerofy, colsizea)
                            else:
                                # get the first row of the matrix as integer
                                print('arrayofright ', arrayofright)
                                for m in range(len(arrayofright)):
                                    arrayfirstrow.insert(m, int(arrayofright[m]))
                            size = len(arraynextrows) + 1
                            matricearray = [] * size
                            for l in range(0, size):
                                if l == 0:
                                    matricearray.insert(l, arrayfirstrow)
                                else:
                                    matricearray.insert(l, arraynextrows[l - 1])
                            matrix_d = Matrix(matricearray)
                            if check_with_variable:
                                subsans = matrix_d - C
                            else:
                                subsans = matrix_d - simpleleftmatrix
                            arrayfirstrow.clear()
                            matricearray.clear()
                            if subsans == zeros(rowsizea, colsizea):
                                logger.info('Correct step')
                            else:
                                logger.info('wrong answer')
                        if is_wrong_ans:
                            logger.info('wrong answer annn')
        filein.close()

    def variable_contains(self, matrixrow, answerofx, answerofy, coloumnsize):
        arrayrowtwo = [] * coloumnsize
        indexofy = None
        for elements in matrixrow:
            if "y" in elements or "x" in elements:
                indexofy = matrixrow.index(elements)
                isminus = false
                isplus = true
                if "-" in elements:
                    isminus = true
                elif"+" in elements:
                    isplus = true
                if isminus:
                    middlearr = elements.split('-')
                elif isplus:
                    middlearr = elements.split('+')
                array = [] * len(middlearr)
                for item in middlearr:
                    if "y" in item:
                        value = answerofy
                        array.append(value)
                    elif "x" in item:
                        value = answerofx
                        array.append(value)
                    else:
                        integeritem = int(item)
                        array.append(integeritem)
                if isminus:
                    firstelement = array[0]
                    secondelement = array[1]
                    ansofmiddlearr = int(firstelement) - int(secondelement)
                elif isplus:
                    firstelement = array[0]
                    secondelement = array[1]
                    ansofmiddlearr = int(firstelement) + int(secondelement)
        for i in range(0, len(matrixrow)):
            if i == indexofy:
                arrayrowtwo.insert(i, ansofmiddlearr)
            else:
                arrayrowtwo.insert(i, int(matrixrow[i]))
            i += 1
        return arrayrowtwo


Solver().solve()
