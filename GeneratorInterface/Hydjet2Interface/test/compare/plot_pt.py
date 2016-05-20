from ROOT import *
import sys

centralities = ["0-02", "0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
energies = [('../OUTPUT_12-07-2016/', '276'), ('../OUTPUT_11-07-2016/', '502')]

fs = []
hs = []
Hs = []
cs = []

for e in energies:
    for ci, c in enumerate(centralities):
        #print c
        fs.append(TFile.Open(e[0]+'output_12M/output_all_2_'+c+'_2.0.root'))
        #fs[-1].ls()
        #pta = []
        for i in xrange(0, 7):
            hn = 'hpt1L'+str(i)
            hs.append(fs[-1].Get(hn))
            if i == 0:
                Hs.append(fs[-1].Get(hn).Clone())
            else:
                Hs[-1].Add(Hs[-1], hs[-1], 1.0, 1.0)
            #print hs[-1]
            #print '\t', hs[-1].GetMean()
            #pta.append(hs[-1].GetMean())
        #print pta
        #ptas = ', '.join([str(f) for f in pta])
        #print '   double pt'+str(ci)+'[7] = {'+ptas+'};'
        cs.append(TCanvas())
        Hs[-1].Draw()
        cs[-1].Print('~/www/13-07-2016/hydjet/compare_pt/'+Hs[-1].GetName()+'_'+c+'_'+e[1]+".png")
        #print

#raw_input('Press enter to continue...')

