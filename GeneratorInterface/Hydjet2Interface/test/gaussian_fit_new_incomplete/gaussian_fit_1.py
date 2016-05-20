from ROOT import *
import sys
import random
from datetime import datetime
random.seed(datetime.now())
import json
from pprint import pprint
import numpy as np

gROOT.SetBatch(True)
gStyle.SetFuncWidth(5)
GENERATE = sys.argv[1] if len(sys.argv) == 2 else False
#print GENERATE
REDO_LIST = []
REDO_LIST = ["2.76TeV_00_10_n2_gfs_3_mode_2", "2.76TeV_00_10_n3_gfs_0_mode_2", "2.76TeV_30_40_n3_gfs_1_mode_2", "2.76TeV_40_50_n3_gfs_0_mode_2", "2.76TeV_50_60_n3_gfs_0_mode_2", "5.02TeV_00_02_n2_gfs_5_mode_2", "5.02TeV_00_02_n2_gfs_6_mode_2", "5.02TeV_00_05_n3_gfs_0_mode_2", "5.02TeV_00_05_n3_gfs_1_mode_2", "5.02TeV_50_60_n2_gfs_2_mode_2"]
REDO_LIST = []
OUTPUT='pars_best.json'
WWW='/afs/cern.ch/user/c/cirkovic/www/07-08-2016_temp/'

fs = []
hs = []
fns = []
cs = {}

gfs_1 = "[%s]*(1/([%s]*sqrt(2*pi)))*exp(-((x-[%s])^2)/(2*[%s]^2))"
gfs = []
Ngs = 3
for i in xrange(0, Ngs):
    gfs.append(gfs_1 % (str(3*i+0), str(3*i+1), str(3*i+2), str(3*i+1)))
gfs = "+".join(gfs)
print gfs
fgs_cols = [kGreen, kYellow, kCyan]
f = TF1("gfs", gfs, -1.0, 1.0)

if GENERATE:
    pars = {}
else:
    with open(OUTPUT) as pars_file:
        pars = json.load(pars_file)

for energy in ['2.76TeV', '5.02TeV']:
    for centrality in ['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']:
        for n in ['n2', 'n3']:
            for mode in ['mode_2']:
                fs.append(TFile.Open("./"+energy+"/"+centrality+"/data_"+n+"/pca_data.root"))
                #fs[-1].ls()
                for i in xrange(0, 7):
                    hs.append(fs[-1].Get(mode+"/ei_histo_1D"+str(i)))
                    hs[-1].Rebin(200)
                    hint = 0
                    for b in xrange(1, hs[-1].GetXaxis().GetNbins()+1):
                        hint += hs[-1].GetBinContent(b)*hs[-1].GetBinWidth(b)
                    fns.append(TF1(energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode, gfs, -1.0, 1.0))
                    for j in xrange(0, Ngs):
                        #A, mean, sigma = .0, .0, .0
                        #if GENERATE:
                        #    A = hs[-1].GetMaximum()/3.0
                        #    mean = hs[-1].GetMean()
                        #    sigma = hs[-1].GetMeanError()
                        #else:
                        A = random.uniform(0.0, hs[-1].GetMaximum())
                        mean = random.uniform(-0.9, 0.9)
                        sigma = random.uniform(0.0, 1.0-abs(mean))
                        #A = hs[-1].GetMaximum()/3.0
                        #sigma = hs[-1].GetMeanError()+random.uniform(hs[-1].GetMeanError()/2.0, hs[-1].GetMeanError()*2.0)
                        #mean = hs[-1].GetMean()+random.uniform(-hs[-1].GetMean(), hs[-1].GetMean())
                        #pars_temp = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(-1.0, 1.0)]
                        pars_temp = [A, sigma, mean]

                        fns[-1].SetParameter(3*j+0, pars_temp[0])
                        fns[-1].SetParLimits(3*j+0, 0.0, hs[-1].GetMaximum())
                        #fns[-1].SetParLimits(3*j+0, 0.0, hs[-1].GetMaximum())

                        fns[-1].SetParameter(3*j+1, pars_temp[1])
                        fns[-1].SetParLimits(3*j+1, 0.0, 1.0-abs(mean))
                        #fns[-1].SetParLimits(3*j+1, 0.0, hs[-1].GetMeanError()*200)

                        fns[-1].SetParameter(3*j+2, pars_temp[2])
                        fns[-1].SetParLimits(3*j+2, -0.9, 0.9)
                        #fns[-1].SetParLimits(3*j+2, -0.99, 0.99)

                    cs[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode] = TCanvas()
                    #hs[-1].Draw("HIST E0")
                    hs[-1].Fit(energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode, "M")
                    #pars[-1][-1][1].append(fns[-1].GetNDF())
                    chisquare = fns[-1].GetChisquare()
                    fint = fns[-1].Integral(-1.0, 1.0)

                    x, h1, h2 = [], [], []
                    for b in xrange(1, hs[-1].GetXaxis().GetNbins()+1):
                        x.append(hs[-1].GetBinCenter(b))
                        h1.append(hs[-1].GetBinContent(b))
                        h2.append(fns[-1].Eval(hs[-1].GetBinCenter(b)))

                    #print x, h1, h2
                    #print (1./np.correlate(h1, h2))
                    #sys.exit()
                    hfcorr = 1./(np.correlate(h1, h2)[0])

#                    if GENERATE or ((chisquare < pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][0]) and (abs(hint-fint) < abs(pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][1]))):
                    #if GENERATE or ((energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode) in REDO_LIST) or (chisquare * abs(hint-fint) < pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][0] * abs(pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][1])):
                    #if GENERATE or ((energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode) in REDO_LIST) or (abs(hint-fint) * hfcorr < abs(pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][1]) * pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][2]):
                    if GENERATE or ((energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode) in REDO_LIST) or (chisquare * abs(hint-fint) * hfcorr < pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][0] * abs(pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][1]) * pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][2]):
                    # (chisquare * abs(fns[-1].Integral(-1.0, 1.0) - hint) < pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][0] * pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][1]):
                        #del pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0][:]
                        #for j in xrange(0, Ngs):
                        #    pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0].append([fns[-1].GetParameter(3*j+0), fns[-1].GetParameter(3*j+1), fns[-1].GetParameter(3*j+2)])
                        #del pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][:]
                        #pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode] = [[], []]
                        #for j in xrange(0, Ngs):
                        #   pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0].append([fns[-1].GetParameter(3*j+0), fns[-1].GetParameter(3*j+1), fns[-1].GetParameter(3*j+2)])
                        #pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(chisquare)
                        ##pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(hint)
                        #pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(fint-hint)
                        fs_temp = []
                        for j in xrange(0, Ngs):
                            f_temp = TF1(energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode+"_"+str(j), gfs_1 % ("0", "1", "2", "1"), -1.0, 1.0)
                            f_temp.SetLineWidth(3)
                            f_temp.SetParameter(0, fns[-1].GetParameter(3*j+0))
                            f_temp.SetParameter(1, fns[-1].GetParameter(3*j+1))
                            f_temp.SetParameter(2, fns[-1].GetParameter(3*j+2))
                            fs_temp.append((f_temp, f_temp.Integral(-1.0, 1.0)))
                        fs_temp = sorted(fs_temp, key=lambda x: x[1], reverse=True)
                        pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode] = [[], []]
                        for j in xrange(0, Ngs):
                           pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0].append([fs_temp[j][0].GetParameter(0), fs_temp[j][0].GetParameter(1), fs_temp[j][0].GetParameter(2)])
                        pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(chisquare)
                        #pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(hint)
                        pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(fint-hint)
                        pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(hfcorr)
                        for j in xrange(0, Ngs):
                            fs_temp[j][0].SetLineColor(fgs_cols[j])
                            fs_temp[j][0].Draw("SAME")
                        cs[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode].Print(WWW+energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode+".png")
    
pprint(pars)
with open(OUTPUT, 'w') as outfile:
    json.dump(pars, outfile)

