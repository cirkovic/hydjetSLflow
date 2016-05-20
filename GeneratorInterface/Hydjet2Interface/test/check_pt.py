from ROOT import *
import sys

fs = []
cs = []
Hs = []

for j in ['output_all_2_0-10_2.0.root', 'output_all_2_20-30_2.0.root', 'output_all_2_0-5_2.0.root', 'output_all_2_50-60_2.0.root', 'output_all_2_30-40_2.0.root', 'output_all_2_0-02_2.0.root', 'output_all_2_10-20_2.0.root', 'output_all_2_40-50_2.0.root']:

    fs.append(TFile.Open('OUTPUT_21-06-2016/output_20M/'+j))
    fs[-1].ls()

    hs = []

    for i in xrange(21, 28):
        hs.append(gDirectory.Get('hpt1L'+str(i)))

    Hs.append(hs[0].Clone())

    for h in hs[1:]:
        Hs[-1].Add(h)
        
    cs.append(TCanvas())
    Hs[-1].Draw()

raw_input('Press enter to finish...')

