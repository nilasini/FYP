from bs4 import BeautifulSoup


class Marks:
    scheme_soup = ""
    tag = ""
    attribute = ""
    markval = 0
    is_constant_there = False

    @staticmethod
    def processmarks():
        mtrilist = []
        matri_name = []
        answerset = []
        siz = 0
        temp = []
        count = 0
        ispassfenced = False
        global x, y
        rightside_constant = None
        isfound = True
        isfoundrow = True
        with open('myscheme.xml') as scheme:
            i=0
            for line in scheme:
                scheme_soup = BeautifulSoup(line, "html.parser")
                if 'data' in line and '/data' not in line:
                    markval = 0
                    tag = scheme_soup.find('data')
                    attribute = tag['marks']
                    markval = int(attribute)
                #     print(mark)
                # if mark > 0:
                #     if 'mn' in line and 'mtd' not in line:
                # #         is_constant_there = True
                # if 'mi' in line and 'mtd' not in line and not ispassfenced:
                #     temp = scheme_soup.text
                #     matri_name.insert(0, temp)
                #     count += 1
                if 'mfenced' in line:
                    count = 0
                    ispassfenced = True
                if '/mfenced' in line:
                    ispassfenced = False
                    rightside_constant = None
                if 'mn' in line and 'mtd' in line:
                    if rightside_constant:
                        s_text = int(rightside_constant) * int(scheme_soup.text)
                        mtrilist.insert(i, str(s_text))
                        # if 'x' in str(s_text) or 'y' in str(s_text):
                        #     iscontain_var = true
                    else:
                        mtrilist.insert(i, scheme_soup.text)
                        # if 'x' in ans_soup.text or 'y' in ans_soup.text:
                        #     iscontain_var = true
                if 'mn' in line and 'mtd' not in line:
                    rightside_constant = scheme_soup.text
                if '/mtr' in line and isfound:
                    col_size = len(mtrilist)
                    isfound = False
                if '/mo' in line and count > 0:
                    if '=' not in scheme_soup.text:
                        matri_name.insert(0, scheme_soup.text)
                if '/mo' in line and count == 0:
                    if scheme_soup.text == '=':
                        iscontain_equals = scheme_soup.text
                if '/mtable' in line:
                    if isfoundrow:
                        siz += len(mtrilist)
                        row_size = int(siz / col_size)
                        isfoundrow = False
                if 'mspace' in line:
                    llist = [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)]
                    print('list is ', llist)
                    temp.insert(0, [mtrilist[x:x + col_size] for x in range(0, len(mtrilist), col_size)])
                    ansMark1 = AnsWithMark(temp.pop(0), markval)
                    print('get ans ', ansMark1.getAnswerStep(), 'marks is ', ansMark1.getMarks())
                    # AnsWithMark().setAnswerStep(temp.pop(0))
                    llist.clear()
                    matri_name.clear()
                    mtrilist.clear()
                    print()
                i = i + 1

class AnsWithMark:


    def __init__(self, step_lists, marks):
        self.step_lists = step_lists
        self.marks = marks

    def getAnswerStep(self):
        return self.step_lists

    def getMarks(self):
        return self.marks

Marks().processmarks()
