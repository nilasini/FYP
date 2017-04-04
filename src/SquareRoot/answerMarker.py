from logger_details import Logs
from bs4 import BeautifulSoup
from sympy import *
import re
from queue import *

class Answer(Logs):

    def __init__(self, ques, scheme, answer_file, logger):
        self.scheme = scheme
        self.answer_file = answer_file
        self.logger = logger
        self.question = ques.read_question()
        self.quest = ques

    def markAns(self):
        answer_list = Queue(maxsize = 0)
        # count = 0
        # ans = ''
        #
        # self.logger.info('Reading answers')
        # with open(self.answer_file) as answer:
        #     i = 0
        #     marks = 0
        #     # parse the answer file
        #     for line in answer:
        #         ans_soup = BeautifulSoup(line, "html.parser")
        #         if 'mn' in line or 'mo' in line:
        #             answer_list.put(ans_soup.text.strip())
        #             count += 1
        #         if 'mspace' in line:
        #             answer_list.queue.clear()
        #             count = 0
        #         if '/math' in line and not(re.search("[+]|[-]|[*]", line)):
        #             for d in range(0, answer_list.qsize()):
        #                 ans += answer_list.get()
        #
        #     if '*' in self.question:
        #         splitted_arr = self.question.split('*')
        #         sym_ans = float(splitted_arr[0]) * float(splitted_arr[1])
        #         if float(ans) == sym_ans:
        #             temp_mark = int(self.scheme['multiplication'])
        #             print('your answer is correct. your mark for multiplication is ', temp_mark)
        #             marks += temp_mark
        # return ans






