from ROOT import *
import sys

fo = open(sys.argv[1], 'w')
fo.close()

with open('IPATH.txt', 'r') as myfile:
    ipath = myfile.read().replace('\n', '')

    centralities = ["0-02", "0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]

    fs = []
    hs = []

    for ci, c in enumerate(centralities):
        #print c
        fs.append(TFile.Open(ipath+'output_all_2_'+c+'_2.0.root'))
        #fs[-1].ls()
        pta = []
        for i in xrange(0, 7):
            hn = 'hpt1L'+str(i)
            hs.append(fs[-1].Get(hn))
            #print hs[-1]
            #print '\t', hs[-1].GetMean()
            pta.append(hs[-1].GetMean())
        #print pta
        ptas = ', '.join([str(f) for f in pta])
        fo = open(sys.argv[1], 'a')
        fo.write('   double pt'+str(ci)+'[7] = {'+ptas+'};\n')
        fo.close()
        #print

