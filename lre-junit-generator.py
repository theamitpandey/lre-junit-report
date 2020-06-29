# This python utility can be used to generate Loadrunner Junit xml reports.
# it accepts the argument as Load Runner summary.html & generates the Junit xml 


import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import datetime

ifile = list(sys.argv)[1]

with open(ifile, 'r') as f:
    data = f.read()

html_data = BeautifulSoup(data, "lxml")
# print(html_data)
table = html_data.find("table", id="TransactionsTable")

rows = table.findAll('tr')
dictionary = {}
for tr in rows:
    td = tr.findAll("td")
    try:
        dictionary[td[0].findNext().text] = [td[1].findNext()["src"], td[6].findNext().text]
    except:
        print(td)

print(len(dictionary), dictionary)



testsuites = ET.Element("testsuites")
testsuite = ET.SubElement(testsuites, "testsuite")

number_failed = 0
number_total = 0
time_total = 0
for key in dictionary:
    testcase = ET.SubElement(testsuite, "testcase")
    testcase.set("name", key)
    testcase.set("time", dictionary[key][1])
    time_total = time_total + float(dictionary[key][1])
    number_total = number_total + 1
    if 'Failed' in dictionary[key][0]:
        x = ET.SubElement(testcase, 'failure')
        x.set("message", "SLA not met")
        number_failed = number_failed + 1

testsuite.set("time", str(time_total))
testsuite.set("tests", str(number_total))
testsuite.set("failures", str(number_failed))
testsuite.set("name", "LRE Report")
testsuite.set("timestamp", str(datetime.datetime.now()))

doc = ET.ElementTree(testsuites)
doc.write('./lre-junit.xml')
