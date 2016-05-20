from ROOT import *
import sys

#from subprocess import call
#a = call(["ls", sys.argv[1]])
#print a

import subprocess
output = subprocess.Popen(["ls", sys.argv[1]], stdout=subprocess.PIPE).communicate()[0]
output = output.split('\n')[0:-1]

fs = []
hs = []

for o in output:
    fs.append(TFile.Open(sys.argv[1]+'/'+o))
    hs.append(fs[-1].Get("hevt"))
    print o, int(hs[-1].Integral())

