from html.parser import HTMLParser

# create a subclass and override the handler methods

lines = []
matrices = []


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        if tag == 'mi':
            matrices.append()

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
            print("Encountered some data  :", data)

filein = open('Question_MathML')
s = filein.read()
# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed(s)