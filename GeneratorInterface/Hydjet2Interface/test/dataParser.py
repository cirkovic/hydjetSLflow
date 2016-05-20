from HTMLParser import HTMLParser
import sys

HTML=[]

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    '''
    indent = 0
    def handle_starttag(self, tag, attrs):
        self.indent += 1
        print "Encountered a start tag:", tag
        HTML.append(''.join([' ' for i in xrange(0, self.indent)])+tag)

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
        HTML.append(''.join([' ' for i in xrange(0, self.indent)])+tag)
        self.indent -= 1

    def handle_data(self, data):
        if ('v_2{GF}' in data or 'v_3{GF}' in data) and not 'centrality' in data:
            print "Encountered some data  :", data
            HTML.append(data)
    '''
    printData = False
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.printData = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.printData = False

    def handle_data(self, data):
        if self.printData:
            print "Encountered some data  :", data

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

import urllib2  # the lib that handles the url stuff
import sys

source = urllib2.urlopen('http://hepdata.cedar.ac.uk/view/ins927105/all') # it's a file like object and works just like a file
data = str('')
for line in source: # files are iterable
    #sys.stdout.write(line)
    data += line
#print

#print data

#sys.exit()

#parser.feed('<html><head><title>Test</title></head><body><h1>Parse me!</h1></body></html>')
parser.feed(data)

#print HTML
