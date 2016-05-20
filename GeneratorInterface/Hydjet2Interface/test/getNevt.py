from ROOT import gROOT, TFile, TH1F
import sys
gROOT.SetBatch(True)
f = TFile.Open(sys.argv[1])
h = f.Get("hevt")
print int(h.Integral())
