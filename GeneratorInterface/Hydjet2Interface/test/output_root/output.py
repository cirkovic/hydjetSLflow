from ROOT import *

gROOT.SetBatch(True)

fs = {}
hs = {}

for ene in ['276', '502']:
    for cent in ['0-02', '0-5', '0-10', '10-20', '20-30', '30-40', '40-50', '50-60']:
        fn = 'output_16_2_'+cent+'_2.0_'+ene+'.root'
        fs[fn] = TFile.Open(fn)
        f = fs[fn]
        hn = 'hevt'
        hs[fn+'__'+hn] = f.Get(hn)
        h1 = hs[fn+'__'+hn]
        hn = 'hpt'
        hs[fn+'__'+hn] = f.Get(hn)
        h2 = hs[fn+'__'+hn]
        hn = 'hmult'
        hs[fn+'__'+hn] = f.Get(hn)
        h3 = hs[fn+'__'+hn]
        #print fn+'__'+hn, ':', h1.GetEntries(), h1.GetMean(), h1.Integral(), h2.GetEntries(), h2.GetMean(), h2.Integral(), h3.GetEntries(), h3.GetMean(), h3.Integral()
        print fn+'__'+hn, ':', h2.GetEntries(), h2.GetMean(), h3.GetEntries(), h3.GetMean()
