from ROOT import *
import sys

cs = []

OPTIONS = "READ"
OPTIONS = "UPDATE"
f = TFile.Open('out_2_00-05.root', OPTIONS)
#f.ls()
f.cd("/PCA/Q_VALUES/00_05/Multiplicity")
#f.ls()
h = gDirectory.Get("P7_multiplicity")
for i in xrange(8, 12):
    h1 = h.Clone()
    h1.SetName("P"+str(i)+"_multiplicity")
    h1.SetTitle("P"+str(i)+"_multiplicity")
    h1.Write("", TObject.kOverwrite)
#cs.append(TCanvas())
#h.Draw()

#raw_input("Press Enter to continue...")
f.ls()

f.Close()

print

for n in ['n2', 'n3']:
    for typ in ['COS_NOT_NORMED', 'COS_NORMED']:
        f = TFile.Open('out_2_00-05.root', OPTIONS)
        f.cd("/PCA/Q_VALUES/00_05/Signal/"+n+"/"+typ)
        h = gDirectory.Get("cosDelta_P7P7")
        for k in ['P1P8', 'P1P9', 'P1P10', 'P1P11', 'P2P8', 'P2P9', 'P2P10', 'P2P11', 'P3P8', 'P3P9', 'P3P10', 'P3P11', 'P4P8', 'P4P9', 'P4P10', 'P4P11', 'P5P8', 'P5P9', 'P5P10', 'P5P11', 'P6P8', 'P6P9', 'P6P10', 'P6P11', 'P7P8', 'P7P9', 'P7P10', 'P7P11', 'P8P9', 'P8P10', 'P8P11', 'P9P10', 'P9P11', 'P10P11', 'P8P8', 'P9P9', 'P10P10', 'P11P11']:
            h1 = h.Clone()
            h1.SetName("cosDelta_"+k)
            h1.SetTitle("cosDelta_"+k)
            h1.Write("", TObject.kOverwrite)
        f.ls()
        print
        f.Close()

