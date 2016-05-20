from ROOT import *
import sys
import random
import json
from pprint import pprint

gROOT.SetBatch(True)
GENERATE = False

fs = []
hs = []
fns = []
cs = {}

gfs = []
Ngs = 3
for i in xrange(0, Ngs):
    gfs.append("[%s]*(1/([%s]*sqrt(2*pi)))*exp(-((x-[%s])^2)/(2*[%s]^2))" % (str(3*i+0), str(3*i+1), str(3*i+2), str(3*i+1)))
gfs = "+".join(gfs)
print gfs
f = TF1("gfs", gfs, -1.0, 1.0)

if GENERATE:
    pars = {}
else:
    with open('pars3.json') as pars_file:
        pars = json.load(pars_file)

for energy in ['2.76TeV', '5.02TeV']:
    for centrality in ['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']:
        for n in ['n2', 'n3']:
            for mode in ['mode_2']:
                fs.append(TFile.Open("/afs/cern.ch/user/c/cirkovic/public/Jovan_24-07-2016/"+energy+"/"+centrality+"/data_"+n+"/pca_data.root"))
                #fs[-1].ls()
                for i in xrange(0, 7):
                    hs.append(fs[-1].Get(mode+"/ei_histo_1D"+str(i)))
                    hs[-1].Rebin(200)
                    hint = 0
                    for b in xrange(1, hs[-1].GetXaxis().GetNbins()+1):
                        hint += hs[-1].GetBinContent(b)*hs[-1].GetBinWidth(b)
                    fns.append(TF1(energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode, gfs, -1.0, 1.0))
                    for j in xrange(0, Ngs):
                        pars_temp = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(-1.0, 1.0)]
                        fns[-1].SetParameter(3*j+0, pars_temp[0])
                        fns[-1].SetParameter(3*j+1, pars_temp[1])
                        fns[-1].SetParameter(3*j+2, pars_temp[2])
                    cs[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode] = TCanvas()
                    #hs[-1].Draw("HIST E0")
                    hs[-1].Fit(energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode, "M")
                    #pars[-1][-1][1].append(fns[-1].GetNDF())
                    chisquare = fns[-1].GetChisquare()
                    fint = fns[-1].Integral(-1.0, 1.0)
                    if GENERATE or ((chisquare < pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][0]) and (abs(hint-fint) < abs(pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][1]))):
                    # (chisquare * abs(fns[-1].Integral(-1.0, 1.0) - hint) < pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][0] * pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][1]):
                        #del pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0][:]
                        #for j in xrange(0, Ngs):
                        #    pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0].append([fns[-1].GetParameter(3*j+0), fns[-1].GetParameter(3*j+1), fns[-1].GetParameter(3*j+2)])
                        #del pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][:]
                        pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode] = [[], []]
                        for j in xrange(0, Ngs):
                           pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0].append([fns[-1].GetParameter(3*j+0), fns[-1].GetParameter(3*j+1), fns[-1].GetParameter(3*j+2)])
                        pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(chisquare)
                        #pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(hint)
                        pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(fint-hint)
                        cs[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode].Print("/afs/cern.ch/user/c/cirkovic/www/28-07-2016_temp1/"+energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+".png")

pprint(pars)
with open('pars3.json', 'w') as outfile:
    json.dump(pars, outfile)

