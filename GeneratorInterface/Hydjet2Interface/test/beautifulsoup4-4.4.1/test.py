from bs4 import BeautifulSoup
import urllib2  # the lib that handles the url stuff
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

source = 2

html = str('')

if source == 1:
    html = """
      <table class="details" border="0" cellpadding="5" cellspacing="2" width="95%">
        <tr valign="top">
          <th>Tests</th>
          <th>Failures</th>
          <th>Success Rate</th>
          <th>Average Time</th>
          <th>Min Time</th>
          <th>Max Time</th>
       </tr>
       <tr valign="top" class="Failure">
         <td>103</td>
         <td>24</td>
         <td>76.70%</td>
         <td>71 ms</td>
         <td>0 ms</td>
         <td>829 ms</td>
      </tr>
    </table>"""
elif source == 2:
    source = urllib2.urlopen('http://hepdata.cedar.ac.uk/view/ins927105/all') # it's a file like object and works just like a file
    for line in source: # files are iterable
        html += line

#html = html.encode('utf8', 'replace')
#html = unicode(html, 'utf8')
html = html.decode("windows-1252")

soup = BeautifulSoup(html, "html.parser")
#table = soup.find("table", attrs={"class":"details"})
#table = soup.find_all(text="v_2{GF}")
#print table
#table = soup.find_all(text="v_3{GF}")
#print table

tables = soup.find_all("table")

tables2 = []
tables3 = []

for table in tables:
    if table.find_all(text="v_2{GF}") != []:
        tables2.append(table)
    elif table.find_all(text="v_3{GF}") != []:
        tables3.append(table)

print len(tables2), len(tables3)

for table in tables3:
    print table
    '''
    trs = table.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        text = []
        for td in tds:
            txt = td.get_text()
            #txt = txt.decode("windows-1252")
            txt = txt.decode("utf8")
            #txt = txt.encode('windows-1252', 'replace')
            #txt = txt.encode('punycode')
            #txt = txt.encode('utf8', 'replace')
            txt = str(''.join([i if ord(i) < 128 else ' ' for i in txt]))
            text.append(txt)
        print text
    '''
    print

sys.exit()

#for table in tables:
#    for th in table.find("tr").find_all("th"):
#        
#    table.find_all(text="v_2{GF}")
#    print table

sys.exit()

# The first tr contains the field names.
headings = [th.get_text() for th in table.find("tr").find_all("th")]

datasets = []
for row in table.find_all("tr")[1:]:
    dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
    datasets.append(dataset)

print datasets
