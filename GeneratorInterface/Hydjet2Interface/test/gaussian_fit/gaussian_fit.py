from ROOT import *
import sys
#import random

fs = []
hs = []
cs = []

gf = "(1/([0]*sqrt(2*pi)))*exp(-((x-[1])^2)/(2*[0]^2))"
gfs = []
#Ngs = 5
Ngs = 3
for i in xrange(0, Ngs):
    #gfs.append("(1/([%s]*sqrt(2*pi)))*exp(-((x-[%s])^2)/(2*[%s]^2))" % (str(2*i+1), str(2*i+2), str(2*i+1)))
    gfs.append("[%s]*(1/([%s]*sqrt(2*pi)))*exp(-((x-[%s])^2)/(2*[%s]^2))" % (str(3*i+0), str(3*i+1), str(3*i+2), str(3*i+1)))

gfs = "+".join(gfs)
print gfs
#sys.exit()
#f = TF1("gfs", "[0]*("+gfs+")", -1.0, 1.0)
f = TF1("gfs", gfs, -1.0, 1.0)
#f.SetParameters(1.0, 0.1, 0.0, 0.2, 0.6, 0.2, -0.6)
#f.SetParameters(1.0, 0.1, 0.0, 1.0, 0.2, 0.6, 1.0, 0.2, -0.6)
#f.SetParameter(0, 1.0)
for i in xrange(0, Ngs):
    f.SetParameter(3*i+0, random.uniform(0.0, 1.0))
    f.SetParameter(3*i+1, random.uniform(0.0, 1.0))
    f.SetParameter(3*i+2, random.uniform(-1.0, 1.0))
cs.append(TCanvas())
f.Draw()

#raw_input("Press enter to finish...")

#sys.exit()

fs.append(TFile.Open("/afs/cern.ch/user/c/cirkovic/public/Jovan_24-07-2016/5.02TeV/00_05/data_n2/pca_data.root"))
#fs[-1].cd("mode_2")
#fs[-1].ls()
#for i in xrange(0, 7):
#for i in xrange(3, 4):
    hs.append(fs[-1].Get("mode_2/ei_histo_1D"+str(i)))
    hs[-1].Rebin(200)
    cs.append(TCanvas())
    #hs[-1].Draw("HIST E0")
    hs[-1].Fit("gfs", "M")

#for i in xrange(1, hs[-1].GetXaxis().GetNbins()):
#    print hs[-1].GetBinCenter(i), hs[-1].GetBinContent(i)

#fe = TFitEditor(cs[-1], hs[-1])

raw_input("Press enter to finish...")

