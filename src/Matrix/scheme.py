from logger_details import Logs
from bs4 import BeautifulSoup

class Scheme(Logs):
    #this method will run when create new instance of this class
    def __init__(self, scheme, logger):
        self.scheme = scheme
        self.logger = logger

    #marking the student answer
    def readScheme(self):
        self.logger.info('Reading scheme')
        scheme_dict = {}
        # open the scheme
        with open(self.scheme) as scheme:
            for line in scheme:
                scheme_soup = BeautifulSoup(line, "html.parser")
                if 'data' in line:
                    tag = scheme_soup.find('data')
                    if tag is not None:
                        attribute1 = tag['marks']
                        attribute2 = tag['concept']
                        marks = int(attribute1)
                        #add the concept and marks pair to a dictionary
                        scheme_dict[attribute2] = marks
                if 'sub_question' in line:
                    tag = scheme_soup.find('sub_question')
                    if tag is not None:
                        attribute3 = tag['totalmarks']
                        tot_marks = int(attribute3)
                        scheme_dict['totalmarks'] = tot_marks
        self.logger.info('Finish scheme reading')
        return scheme_dict
        #no need to close the file with statement will handle that

