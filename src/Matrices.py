# this class can solves matrix questions which have matrix with variables
from _operator import ne
from pydoc import ispackage

from sympy import *
import re


class Solver:
    def solve(self):
        x = Symbol('x')
        y = Symbol('y')
        A = Matrix(([3, 2], [4, 0], [5, 1]))
        B = Matrix(([2, 1], [x, 0], [-1, y]))
        C = Matrix(([8, 5], [5, 0], [9, 5]))
        # A = Matrix(([3, 2, 4], [0, 1, 5]))
        # B = Matrix(([x, 4, 8], [0, 3, y]))
        # C = Matrix(([1, 0, 0], [0, -1, 0]))
        rowsizea = A.rows
        colsizea = A.cols
        answerofy = None
        answerofx = None
        simpleleftmatrix = None
        rightelement = None
        arrayofright = None
        remainrowsize = rowsizea - 1

        with open('sampleFile.txt') as filein:
            i = 0
            for line in filein:
                # remove all empty lines
                if line.strip():
                    # check whether it is first row of a matrix
                    if "=" in line:
                        nextrow = [[0] * colsizea for y in range(remainrowsize)]
                        arraynextrows=[[0] * colsizea for y in range(remainrowsize)]


                        # check lefthand equation operand
                        iscontainminus = false
                        iscontainplus = false

                        # split the first row using '='
                        arrayStr = line.split('=')

                        # extract the leftelement
                        leftelement = arrayStr.pop(0)

                        # check whether the lefthand elements contains numbers with variables. Eg:2A
                        if re.search(r'\d', leftelement) and len(leftelement) < 3:
                            rightelement = arrayStr.pop(0)
                            arrayofright = rightelement.split()
                            arrayfirstrow = [] * colsizea

                            # get the first row of the matrix as integer
                            for j in range(len(arrayofright)):
                                arrayfirstrow.insert(j, int(arrayofright.pop(0)))
                            print('arrayfirstrow ',arrayfirstrow)

                            # calculate the left side using sympy
                            if leftelement[1:2] == "A":
                                simpleleftmatrix = int(leftelement[0:1]) * A
                            elif leftelement[1:2] == "B":
                                simpleleftmatrix = int(leftelement[0:1]) * B
                            print('Left hand side of the equation using sympy ', simpleleftmatrix)
                            print('right hand side of the first row ', arrayfirstrow)

                        #check whether left hand side contain operand
                        else:
                            if "-" in leftelement:
                                iscontainminus = true
                                # split the left hand side using -
                                twoOperandSplitArray = leftelement.split('-')
                            elif "+" in leftelement:
                                iscontainplus = true
                                # split the left hand side using -
                                twoOperandSplitArray = leftelement.split('+')

                            # get the right hand side elements of the first row of the matrix
                            rightelement = arrayStr.pop(0)
                            arrayofright = rightelement.split()

                            for elements in twoOperandSplitArray:
                                if len(elements) > 1:
                                    if "A" in elements:
                                        G = int(elements[0:1]) * A
                                    if "B" in elements:
                                        G = int(elements[0:1]) * B

                                # find the lefhand side matrix which contains operand using sympy
                                elif "A" in elements and iscontainminus:
                                    leftsidewithoperand = G - A
                                    answers = solve((C - leftsidewithoperand), x, y)
                                    answerofx = answers.pop(x)
                                    answerofy = answers.pop(y)
                                elif "A" in elements and iscontainplus:
                                    leftsidewithoperand = G + A
                                    answers = solve((C - leftsidewithoperand), x, y)
                                    answerofx = answers.pop(x)
                                    answerofy = answers.pop(y)
                                elif "B" in elements and iscontainminus:
                                    leftsidewithoperand = G - B
                                    print('C - leftsidewithoperand ',C - leftsidewithoperand)
                                    answers = solve((C - leftsidewithoperand), x, y)
                                    print('answers pop x', answers)
                                    answerofx = answers.pop(x)
                                    answerofy = answers.pop(y)
                                    print('lefhand side which contains operand using sympy ', leftsidewithoperand)
                                elif "B" in elements and iscontainplus:
                                    leftsidewithoperand = G + B
                                    answers = solve((C - leftsidewithoperand), x, y)
                                    answerofx = answers.pop(x)
                                    answerofy = answers.pop(y)

                    else:
                        if i <= rowsizea:
                            temporary = line.split()
                            for k in range(len(temporary)):
                                nextrow[i - 1][k] = temporary[k]
                    i += 1
                    print('.......................one line finished..................')
                    if i == rowsizea:
                        i = 0
                        j = 0
                        for j in range(len(nextrow)):
                            for elements in nextrow[j]:
                                iscontainvariable = false
                                if "y" in elements or "x" in elements:
                                    iscontainvariable = true
                                    break
                            if iscontainvariable:
                                arraynextrows[j] = self.variableContains(nextrow[j], answerofx, answerofy, colsizea)
                                # get the first row of the matrix as integer
                                arrayfirstrow = self.variableContains(arrayofright, answerofx, answerofy, colsizea)
                            else:
                                for k in range(len(nextrow[j])):
                                    arraynextrows[j][k] = int(nextrow[j][k])
                        print(' array of next rows, next row ', arraynextrows, nextrow)
                        print('arrayfirstrow, arraynextrows ', arrayfirstrow, arraynextrows)
                        size = len(arraynextrows)+1
                        matricearray = [] * size
                        print('size is ',size)
                        for l in range(0, size):
                            if l == 0:
                                matricearray.insert(l, arrayfirstrow)
                            else:
                                matricearray.insert(l, arraynextrows[l - 1])
                        print('matricearray[l] ', matricearray)
                        D = Matrix(matricearray)
                        print('this is D ', D)
                        if (iscontainvariable):
                            subsans = D - C
                        else:
                            subsans = D - simpleleftmatrix
                            print('subsans ', subsans)
                        if subsans == zeros(rowsizea, colsizea):
                            print("correct")
        filein.close()

    def variableContains(self, matrixrow, answerofx, answerofy,coloumnsize):
        arrayrowtwo = [] * coloumnsize
        indexofy = None
        for elements in matrixrow:
            if "y" in elements or "x" in elements:
                firstelement=0
                secondelement=0
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
                print('middlearr ',middlearr)
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
                    print('first element ',firstelement, 'secondelement', secondelement,'ans of variable index ',ansofmiddlearr)
                elif isplus:
                    print(' array[1] ', array[1])
                    firstelement = array[0]
                    secondelement = array[1]
                    ansofmiddlearr = int(firstelement) + int(secondelement)
        i = 0
        for elements in matrixrow:
            if i == indexofy:
                arrayrowtwo.insert(i, ansofmiddlearr)
            else:
                arrayrowtwo.insert(i, int(matrixrow[i]))
            i += 1
        return arrayrowtwo


Solver().solve()
