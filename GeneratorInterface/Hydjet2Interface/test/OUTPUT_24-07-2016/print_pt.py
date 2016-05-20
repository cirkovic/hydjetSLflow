from ROOT import *
import sys

centralities = ["0-02", "0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]

fs = []
hs = []

IPATH=''
with open('IPATH.txt', 'r') as myfile:
    IPATH = myfile.read().replace('\n', '')

fname = 'pt_values.h'
f = open(fname, "w")
f.close()

for ci, c in enumerate(centralities):
    #print c
    fs.append(TFile.Open(IPATH+'output_all_2_'+c+'_2.0.root'))
    fs[-1].ls()
    pta = []
    for i in xrange(0, 7):
        hn = 'hpt1L'+str(i)
        hs.append(fs[-1].Get(hn))
        #print hs[-1]
        #print '\t', hs[-1].GetMean()
        pta.append(hs[-1].GetMean())
    #print pta
    ptas = ', '.join([str(f) for f in pta])
    print '   double pt'+str(ci)+'[7] = {'+ptas+'};'
    with open(fname, 'a') as f:
        f.write('   double pt'+str(ci)+'[7] = {'+ptas+'};\n')
    #print

