from _thread import exit

from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re
from queue import *
from math import isclose


class Answer(Logs):
    def __init__(self, ques, scheme, answer_file, logger):
        self.scheme = scheme
        self.answer_file = answer_file
        self.logger = logger
        self.question = ques.readquestion()
        self.quest = ques

    def markAns(self):
        answer_list = Queue(maxsize=0)
        count = 0
        ans = ''
        iscontainoperator = false
        self.logger.info('Reading answers')
        with open(self.answer_file) as answer:
            i = 0
            marks = 0
            # parse the answer file
            for line in answer:
                ans_soup = BeautifulSoup(line, "html.parser")
                if 'mn' in line or 'mo' in line:
                    if 'mo' in line:
                        iscontainoperator = true
                    answer_list.put(ans_soup.text.strip())
                    count += 1
                if 'mspace' in line:
                    for d in range(0, answer_list.qsize()):
                        ans += answer_list.get()
                    answer_list.queue.clear()

            if '=' in ans:
                splittedarray = ans.split('=')
                if not re.search("[+]|[-]|[*]", splittedarray[0]):
                    ans = splittedarray[0]
                else:
                    ans = splittedarray[1]
            if '+' in self.question and ans:
                isshowerr = false
                sym_afterdeci1 = 0
                sym_afterdeci2 = 0
                self.logger.info('Type : decimal addition')
                splitted_arr = self.question.split('+')
                if '.' not in splitted_arr[0]:
                    splitted_arr[0] = splitted_arr[0] + '.' + '0'
                if '.' not in splitted_arr[1]:
                    splitted_arr[1] = splitted_arr[1] + '.' + '0'
                if len(splitted_arr[0]) > len(splitted_arr[1]):
                    numofdecimal = splitted_arr[0][::-1].find('.')
                else:
                    numofdecimal = splitted_arr[1][::-1].find('.')
                stu_ans = float(ans)  # student answer
                # sympy's correct answer
                sym_ans = round(float(splitted_arr[0]) + float(splitted_arr[1]), int(numofdecimal))

                # check inverse operation
                inverse_ans = float(splitted_arr[0]) - float(splitted_arr[1])
                inversemul_ans = float(splitted_arr[0]) * float(splitted_arr[1])

                #check whether added decimal part separately from the whole number part
                if '.' in splitted_arr[0]:
                    sym_afterdeci1 = len(((splitted_arr[0]).split('.'))[1])  # count number of decimal after decimal point
                if '.' in splitted_arr[1]:
                    sym_afterdeci2 = len(((splitted_arr[1]).split('.'))[1])  # count number of decimal after decimal point
                diff = abs(sym_afterdeci1 - sym_afterdeci2)  # check which number has more decimal
                separate_ans1 = int(((splitted_arr[0]).split('.'))[0]) + int(((splitted_arr[1]).split('.'))[0])
                if sym_afterdeci1 > sym_afterdeci2:
                    separate_ans2 = int(((splitted_arr[1]).split('.'))[1]) * (10 ** diff) + int(
                        ((splitted_arr[0]).split('.'))[1])  # make two numbers equal length
                else:
                    separate_ans2 = int(((splitted_arr[0]).split('.'))[1]) * (10 ** diff) + int(
                        ((splitted_arr[1]).split('.'))[1])  # make two numbers equal length

                # check whether decimal point has been misplaced
                # reverse the string and find the position of a decimal point
                sym_decimalpoint = (str(sym_ans))[::-1].find('.')
                stu_decimalpoint = (str(stu_ans))[::-1].find('.')
                difference = abs((str(sym_ans))[::-1].find('.') - (str(stu_ans))[::-1].find('.'))
                for k in range(1, difference + 1):
                    if stu_decimalpoint > sym_decimalpoint:
                        if isclose(stu_ans * (10 ** k), sym_ans):
                            isshowerr = true
                            break
                    else:
                        if isclose(sym_ans * (10 ** k), stu_ans):
                            isshowerr = true
                            break

                if isclose(float(ans), sym_ans):
                    temp_mark = int(self.scheme['addition'])
                    print('your answer is correct. your mark for addition is ', temp_mark)
                    marks += temp_mark
                elif isclose(float(ans), inverse_ans):
                    print('your answer is wrong. you have done subtraction instead of addition')
                elif isclose(float(ans), inversemul_ans):
                    print('your answer is wrong. you have done multiplication instead of addition')
                elif (float(str(separate_ans1) + '.' + str(separate_ans2))) == float(ans):
                    print(' your answer is wrong. you have added decimal part separately from the whole number part')
                    exit()
                elif isshowerr:
                    print("your answer is wrong, you have misplaced the decimal point")
                else:
                    print("your answer is wrong")

            elif '-' in self.question and ans:
                sym_afterdeci1 = 0
                sym_afterdeci2 = 0
                self.logger.info('Type : decimal subtraction')
                isshowerr = false
                splitted_arr = self.question.split('-')
                if '.' not in splitted_arr[0]:
                    splitted_arr[0] = splitted_arr[0] + '.' + '0'
                if '.' not in splitted_arr[1]:
                    splitted_arr[1] = splitted_arr[1] + '.' + '0'
                if len(splitted_arr[0]) > len(splitted_arr[1]):
                    numofdecimal = splitted_arr[0][::-1].find('.')
                else:
                    numofdecimal = splitted_arr[1][::-1].find('.')
                numofdecimal += 1

                # sympy's correct answer
                val = '.'+str(numofdecimal)+'f'
                sym_ans = format(float(splitted_arr[0]) - float(splitted_arr[1]), val)
                stu_ans = format(float(ans), val)  # student answer
                print('stu_ans ', stu_ans)

                # check inverse operation
                inverse_ans = float(splitted_arr[0]) + float(splitted_arr[1])

                # check whether added decimal part separately from the whole number part
                # if '.' in splitted_arr[0]:
                #     sym_afterdeci1 = len(((splitted_arr[0]).split('.'))[1])  # count number of decimal after decimal point
                # if '.' in splitted_arr[1]:
                #     sym_afterdeci2 = len(((splitted_arr[1]).split('.'))[1])  # count number of decimal after decimal point
                # diff = abs(sym_afterdeci1 - sym_afterdeci2)  # check which number has more decimal
                # separate_ans1 = int(((splitted_arr[0]).split('.'))[0]) - int(((splitted_arr[1]).split('.'))[0])
                # if sym_afterdeci1 > sym_afterdeci2:
                #     separate_ans2 = int(((splitted_arr[1]).split('.'))[1]) * (10 ** diff) - int(
                #         ((splitted_arr[0]).split('.'))[1])  # make two numbers equal length
                # else:
                #     separate_ans2 = int(((splitted_arr[0]).split('.'))[1]) * (10 ** diff) - int(
                #         ((splitted_arr[1]).split('.'))[1])  # make two numbers equal length

                # check whether decimal point has been misplaced
                # reverse the string and find the position of a decimal point
                sym_decimalpoint = (str(sym_ans))[::-1].find('.')
                stu_decimalpoint = (str(stu_ans))[::-1].find('.')
                # difference = abs((str(sym_ans))[::-1].find('.') - (str(stu_ans))[::-1].find('.'))
                if (str(sym_ans))[::-1].find('.') > (str(stu_ans))[::-1].find('.'):
                    for k in range(1, (str(sym_ans))[::-1].find('.') + 1):
                        if float(sym_ans) > float(stu_ans):
                            if isclose(float(stu_ans) * (10 ** k), float(sym_ans)):
                                isshowerr = true
                                break
                        else:
                            if isclose(float(sym_ans) * (10 ** k), float(stu_ans)):
                                isshowerr = true
                                break
                else:
                    for k in range(1, (str(stu_ans))[::-1].find('.') + 1):
                        if float(sym_ans) > float(stu_ans):
                            if isclose(float(stu_ans) * (10 ** k), float(sym_ans)):
                                isshowerr = true
                                break
                        else:
                            if isclose(float(sym_ans) * (10 ** k), float(stu_ans)):
                                isshowerr = true
                                break
                # for k in range(1, difference + 1):
                #     if stu_decimalpoint > sym_decimalpoint:
                #         if isclose(float(stu_ans) * (10 ** k), sym_ans):
                #             isshowerr = true
                #             break
                #     else:
                #         if isclose(float(sym_ans) * (10 ** k), stu_ans):
                #             isshowerr = true
                #             break

                if isclose(float(ans), float(sym_ans)):
                    temp_mark = int(self.scheme['subtraction'])
                    print('your answer is correct. your mark for subtraction is ', temp_mark)
                    marks += temp_mark
                elif isclose(float(ans), inverse_ans):
                    print('your answer is wrong. you have done subtraction instead of addition')
                # elif (float(str(separate_ans1) + '.' + str(separate_ans2))) == float(ans):
                #     print(' your answer is wrong. you have added decimal part separately from the whole number part')
                #     exit()
                elif isshowerr:
                    print("your answer is wrong, you have misplaced the decimal point")
                else:
                    print("your answer is wrong")
            elif '*' in self.question and ans:
                isshowerr = false
                self.logger.info('Type : decimal multiplication')
                splitted_arr = self.question.split('*')
                numofdecimal = splitted_arr[0][::-1].find('.') + splitted_arr[1][::-1].find('.')
                stu_ans = float(ans)  # student answer
                # sympy's correct answer
                sym_ans = round(float(splitted_arr[0]) * float(splitted_arr[1]), int(numofdecimal))

                # check inverse operation
                inverse_ans = float(splitted_arr[0]) + float(splitted_arr[1])

                # check whether decimal point has been misplaced
                # reverse the string and find the position of a decimal point
                sym_decimalpoint = (str(sym_ans))[::-1].find('.')
                stu_decimalpoint = (str(stu_ans))[::-1].find('.')

                difference = abs((str(sym_ans))[::-1].find('.') - (str(stu_ans))[::-1].find('.'))
                for k in range(1, difference + 1):
                    if stu_decimalpoint > sym_decimalpoint:
                        if isclose(stu_ans * (10 ** k), sym_ans):
                            isshowerr = true
                            break
                    else:
                        if isclose(sym_ans * (10 ** k), stu_ans):
                            isshowerr = true
                            break

                if isclose(float(ans), sym_ans):
                    temp_mark = int(self.scheme['multiplication'])
                    print('your answer is correct. your mark for multiplication is ', temp_mark)
                    marks += temp_mark
                elif isclose(float(ans), inverse_ans):
                    print('your answer is wrong. you have done addition instead of multiplication')
                # elif (float(str(separate_ans1) + '.' + str(separate_ans2))) == float(ans):
                #     print(' your answer is wrong. you have added decimal part separately from the whole number part')
                #     exit()
                elif isshowerr:
                    print("your answer is wrong, you have misplaced the decimal point")
                else:
                    print("your answer is wrong")
                # sym_ans = float(splitted_arr[0]) * float(splitted_arr[1])
                # if isclose(float(ans), sym_ans):
                #     temp_mark = int(self.scheme['multiplication'])
                #     print('your answer is correct. your mark for multiplication is ', temp_mark)
                #     marks += temp_mark




        return ans
