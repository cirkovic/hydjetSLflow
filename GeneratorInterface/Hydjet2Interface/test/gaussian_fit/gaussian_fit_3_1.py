from ROOT import *
import sys
import random
import json
from pprint import pprint

gROOT.SetBatch(True)

with open('pars3.json') as pars_file:
    pars = json.load(pars_file)

fs = []
hs = []
fns = []
cs = {}

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
f.SetParameters(1.0, 0.1, 0.0, 1.0, 0.2, 0.6, 1.0, 0.2, -0.6)
#f.SetParameter(0, 1.0)
#for i in xrange(0, Ngs):
#    f.SetParameter(3*i+0, random.uniform(0.0, 1.0))
#    f.SetParameter(3*i+1, random.uniform(0.0, 1.0))
#    f.SetParameter(3*i+2, random.uniform(-1.0, 1.0))
#cs.append(TCanvas())
#f.Draw()

#raw_input("Press enter to finish...")

#sys.exit()

pars = {}

for energy in ['2.76TeV', '5.02TeV']:
    for centrality in ['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']:
        for n in ['n2', 'n3']:
            for mode in ['mode_2']:
                fs.append(TFile.Open("/afs/cern.ch/user/c/cirkovic/public/Jovan_24-07-2016/"+energy+"/"+centrality+"/data_"+n+"/pca_data.root"))
                #fs[-1].cd("mode_2")
                fs[-1].ls()
                #pars = {}
                Ntry = 1
                for i in xrange(0, 7):
                #for i in xrange(3, 4):
                    hs.append(fs[-1].Get(mode+"/ei_histo_1D"+str(i)))
                    hs[-1].Rebin(200)
                    #hs[-1].Scale(1./hs[-1].Integral())
                    hint = 0
                    for b in xrange(1, hs[-1].GetXaxis().GetNbins()+1):
                        hint += hs[-1].GetBinContent(b)*hs[-1].GetBinWidth(b)
                    fns.append(TF1(energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode, gfs, -1.0, 1.0))
                    #f.SetParameters(1.0, 0.1, 0.0, 0.2, 0.6, 0.2, -0.6)
                    #fns[-1].SetParameters(1.0, 0.1, 0.0, 1.0, 0.2, 0.6, 1.0, 0.2, -0.6)
                    #pars["gfs_"+str(i)] = []
                    pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode] = [[], []]
                    #PARS = [[1.0, 0.1, 0.0], [1.0, 0.2, 0.6], [1.0, 0.2, -0.6]]
                    #for t in xrange(0, 10):
                    if True:
                        if True:
                            for j in xrange(0, Ngs):
                                pars_temp = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(-1.0, 1.0)]
                                #pars_temp = [PARS[j][0], PARS[j][1], PARS[j][2]]
                                #print "gfs_"+str(i), 0, j
                                #print pars["gfs_"+str(i)][0][j]
                        #        fns[-1].SetParameter(3*j+0, pars["gfs_"+str(i)][0][j][0])
                        #        fns[-1].SetParameter(3*j+1, pars["gfs_"+str(i)][0][j][1])
                        #        fns[-1].SetParameter(3*j+2, pars["gfs_"+str(i)][0][j][2])
                                fns[-1].SetParameter(3*j+0, pars_temp[0])
                                fns[-1].SetParameter(3*j+1, pars_temp[1])
                                fns[-1].SetParameter(3*j+2, pars_temp[2])
                                pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0].append(pars_temp)
                        #if True:
                        if False:
                            for j in xrange(0, Ngs):
                                #pars_temp = [PARS[j][0], PARS[j][1], PARS[j][2]]
                                #print "gfs_"+str(i), 0, j
                                #print pars["gfs_"+str(i)][0][j]
                        #        fns[-1].SetParameter(3*j+0, pars["gfs_"+str(i)][0][j][0])
                        #        fns[-1].SetParameter(3*j+1, pars["gfs_"+str(i)][0][j][1])
                        #        fns[-1].SetParameter(3*j+2, pars["gfs_"+str(i)][0][j][2])
                                fns[-1].SetParameter(3*j+0, pars["gfs_"+str(i)][0][j][0])
                                fns[-1].SetParameter(3*j+1, pars["gfs_"+str(i)][0][j][1])
                                fns[-1].SetParameter(3*j+2, pars["gfs_"+str(i)][0][j][2])
                                #pars[-1][-1][0].append(pars_temp)
                        cs[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode] = TCanvas()
                        #hs[-1].Draw("HIST E0")
                        hs[-1].Fit(energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode, "M")
                        #pars[-1][-1][1].append(fns[-1].GetNDF())
                        chisquare = fns[-1].GetChisquare()
                        #if (chisquare * abs(fns[-1].Integral(-1.0, 1.0) - hint) < pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][0] * pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][1]) and True: #and (i in [0]):
                        #if True:
                        #if False:
                        if i in [
"2.76TeV_00_02_n2_gfs_0", "2.76TeV_00_02_n2_gfs_1", "2.76TeV_00_02_n2_gfs_2", "2.76TeV_00_02_n2_gfs_3", "2.76TeV_00_02_n2_gfs_4", "2.76TeV_00_02_n2_gfs_5", "2.76TeV_00_02_n2_gfs_6",
"2.76TeV_00_02_n3_gfs_0", "2.76TeV_00_02_n3_gfs_1", "2.76TeV_00_02_n3_gfs_2", "2.76TeV_00_02_n3_gfs_3", "2.76TeV_00_02_n3_gfs_4", "2.76TeV_00_02_n3_gfs_5", "2.76TeV_00_02_n3_gfs_6",
"2.76TeV_00_05_n2_gfs_0", "2.76TeV_00_05_n2_gfs_1", "2.76TeV_00_05_n2_gfs_2", "2.76TeV_00_05_n2_gfs_3", "2.76TeV_00_05_n2_gfs_4", "2.76TeV_00_05_n2_gfs_5", "2.76TeV_00_05_n2_gfs_6",
"2.76TeV_00_05_n3_gfs_0", "2.76TeV_00_05_n3_gfs_1", "2.76TeV_00_05_n3_gfs_2", "2.76TeV_00_05_n3_gfs_3", "2.76TeV_00_05_n3_gfs_4", "2.76TeV_00_05_n3_gfs_5", "2.76TeV_00_05_n3_gfs_6",
"2.76TeV_00_10_n2_gfs_0", "2.76TeV_00_10_n2_gfs_1", "2.76TeV_00_10_n2_gfs_2", "2.76TeV_00_10_n2_gfs_3", "2.76TeV_00_10_n2_gfs_4", "2.76TeV_00_10_n2_gfs_5", "2.76TeV_00_10_n2_gfs_6",
"2.76TeV_00_10_n3_gfs_0", "2.76TeV_00_10_n3_gfs_1", "2.76TeV_00_10_n3_gfs_2", "2.76TeV_00_10_n3_gfs_3", "2.76TeV_00_10_n3_gfs_4", "2.76TeV_00_10_n3_gfs_5", "2.76TeV_00_10_n3_gfs_6",
"2.76TeV_10_20_n2_gfs_0", "2.76TeV_10_20_n2_gfs_1", "2.76TeV_10_20_n2_gfs_2", "2.76TeV_10_20_n2_gfs_3", "2.76TeV_10_20_n2_gfs_4", "2.76TeV_10_20_n2_gfs_5", "2.76TeV_10_20_n2_gfs_6",
"2.76TeV_10_20_n3_gfs_0", "2.76TeV_10_20_n3_gfs_1", "2.76TeV_10_20_n3_gfs_2", "2.76TeV_10_20_n3_gfs_3", "2.76TeV_10_20_n3_gfs_4", "2.76TeV_10_20_n3_gfs_5", "2.76TeV_10_20_n3_gfs_6",
"2.76TeV_20_30_n2_gfs_0", "2.76TeV_20_30_n2_gfs_1", "2.76TeV_20_30_n2_gfs_2", "2.76TeV_20_30_n2_gfs_3", "2.76TeV_20_30_n2_gfs_4", "2.76TeV_20_30_n2_gfs_5", "2.76TeV_20_30_n2_gfs_6",
"2.76TeV_20_30_n3_gfs_0", "2.76TeV_20_30_n3_gfs_1", "2.76TeV_20_30_n3_gfs_2", "2.76TeV_20_30_n3_gfs_3", "2.76TeV_20_30_n3_gfs_4", "2.76TeV_20_30_n3_gfs_5", "2.76TeV_20_30_n3_gfs_6",
"2.76TeV_30_40_n2_gfs_0", "2.76TeV_30_40_n2_gfs_1", "2.76TeV_30_40_n2_gfs_2", "2.76TeV_30_40_n2_gfs_3", "2.76TeV_30_40_n2_gfs_4", "2.76TeV_30_40_n2_gfs_5", "2.76TeV_30_40_n2_gfs_6",
"2.76TeV_30_40_n3_gfs_0", "2.76TeV_30_40_n3_gfs_1", "2.76TeV_30_40_n3_gfs_2", "2.76TeV_30_40_n3_gfs_3", "2.76TeV_30_40_n3_gfs_4", "2.76TeV_30_40_n3_gfs_5", "2.76TeV_30_40_n3_gfs_6",
"2.76TeV_40_50_n2_gfs_0", "2.76TeV_40_50_n2_gfs_1", "2.76TeV_40_50_n2_gfs_2", "2.76TeV_40_50_n2_gfs_3", "2.76TeV_40_50_n2_gfs_4", "2.76TeV_40_50_n2_gfs_5", "2.76TeV_40_50_n2_gfs_6",
"2.76TeV_40_50_n3_gfs_0", "2.76TeV_40_50_n3_gfs_1", "2.76TeV_40_50_n3_gfs_2", "2.76TeV_40_50_n3_gfs_3", "2.76TeV_40_50_n3_gfs_4", "2.76TeV_40_50_n3_gfs_5", "2.76TeV_40_50_n3_gfs_6",
"2.76TeV_50_60_n2_gfs_0", "2.76TeV_50_60_n2_gfs_1", "2.76TeV_50_60_n2_gfs_2", "2.76TeV_50_60_n2_gfs_3", "2.76TeV_50_60_n2_gfs_4", "2.76TeV_50_60_n2_gfs_5", "2.76TeV_50_60_n2_gfs_6",
"2.76TeV_50_60_n3_gfs_0", "2.76TeV_50_60_n3_gfs_1", "2.76TeV_50_60_n3_gfs_2", "2.76TeV_50_60_n3_gfs_3", "2.76TeV_50_60_n3_gfs_4", "2.76TeV_50_60_n3_gfs_5", "2.76TeV_50_60_n3_gfs_6",
"5.02TeV_00_02_n2_gfs_0", "5.02TeV_00_02_n2_gfs_1", "5.02TeV_00_02_n2_gfs_2", "5.02TeV_00_02_n2_gfs_3", "5.02TeV_00_02_n2_gfs_4", "5.02TeV_00_02_n2_gfs_5", "5.02TeV_00_02_n2_gfs_6",
"5.02TeV_00_02_n3_gfs_0", "5.02TeV_00_02_n3_gfs_1", "5.02TeV_00_02_n3_gfs_2", "5.02TeV_00_02_n3_gfs_3", "5.02TeV_00_02_n3_gfs_4", "5.02TeV_00_02_n3_gfs_5", "5.02TeV_00_02_n3_gfs_6",
"5.02TeV_00_05_n2_gfs_0", "5.02TeV_00_05_n2_gfs_1", "5.02TeV_00_05_n2_gfs_2", "5.02TeV_00_05_n2_gfs_3", "5.02TeV_00_05_n2_gfs_4", "5.02TeV_00_05_n2_gfs_5", "5.02TeV_00_05_n2_gfs_6",
"5.02TeV_00_05_n3_gfs_0", "5.02TeV_00_05_n3_gfs_1", "5.02TeV_00_05_n3_gfs_2", "5.02TeV_00_05_n3_gfs_3", "5.02TeV_00_05_n3_gfs_4", "5.02TeV_00_05_n3_gfs_5", "5.02TeV_00_05_n3_gfs_6",
"5.02TeV_00_10_n2_gfs_0", "5.02TeV_00_10_n2_gfs_1", "5.02TeV_00_10_n2_gfs_2", "5.02TeV_00_10_n2_gfs_3", "5.02TeV_00_10_n2_gfs_4", "5.02TeV_00_10_n2_gfs_5", "5.02TeV_00_10_n2_gfs_6",
"5.02TeV_00_10_n3_gfs_0", "5.02TeV_00_10_n3_gfs_1", "5.02TeV_00_10_n3_gfs_2", "5.02TeV_00_10_n3_gfs_3", "5.02TeV_00_10_n3_gfs_4", "5.02TeV_00_10_n3_gfs_5", "5.02TeV_00_10_n3_gfs_6",
"5.02TeV_10_20_n2_gfs_0", "5.02TeV_10_20_n2_gfs_1", "5.02TeV_10_20_n2_gfs_2", "5.02TeV_10_20_n2_gfs_3", "5.02TeV_10_20_n2_gfs_4", "5.02TeV_10_20_n2_gfs_5", "5.02TeV_10_20_n2_gfs_6",
"5.02TeV_10_20_n3_gfs_0", "5.02TeV_10_20_n3_gfs_1", "5.02TeV_10_20_n3_gfs_2", "5.02TeV_10_20_n3_gfs_3", "5.02TeV_10_20_n3_gfs_4", "5.02TeV_10_20_n3_gfs_5", "5.02TeV_10_20_n3_gfs_6",
"5.02TeV_20_30_n2_gfs_0", "5.02TeV_20_30_n2_gfs_1", "5.02TeV_20_30_n2_gfs_2", "5.02TeV_20_30_n2_gfs_3", "5.02TeV_20_30_n2_gfs_4", "5.02TeV_20_30_n2_gfs_5", "5.02TeV_20_30_n2_gfs_6",
"5.02TeV_20_30_n3_gfs_0", "5.02TeV_20_30_n3_gfs_1", "5.02TeV_20_30_n3_gfs_2", "5.02TeV_20_30_n3_gfs_3", "5.02TeV_20_30_n3_gfs_4", "5.02TeV_20_30_n3_gfs_5", "5.02TeV_20_30_n3_gfs_6",
"5.02TeV_30_40_n2_gfs_0", "5.02TeV_30_40_n2_gfs_1", "5.02TeV_30_40_n2_gfs_2", "5.02TeV_30_40_n2_gfs_3", "5.02TeV_30_40_n2_gfs_4", "5.02TeV_30_40_n2_gfs_5", "5.02TeV_30_40_n2_gfs_6",
"5.02TeV_30_40_n3_gfs_0", "5.02TeV_30_40_n3_gfs_1", "5.02TeV_30_40_n3_gfs_2", "5.02TeV_30_40_n3_gfs_3", "5.02TeV_30_40_n3_gfs_4", "5.02TeV_30_40_n3_gfs_5", "5.02TeV_30_40_n3_gfs_6",
"5.02TeV_40_50_n2_gfs_0", "5.02TeV_40_50_n2_gfs_1", "5.02TeV_40_50_n2_gfs_2", "5.02TeV_40_50_n2_gfs_3", "5.02TeV_40_50_n2_gfs_4", "5.02TeV_40_50_n2_gfs_5", "5.02TeV_40_50_n2_gfs_6",
"5.02TeV_40_50_n3_gfs_0", "5.02TeV_40_50_n3_gfs_1", "5.02TeV_40_50_n3_gfs_2", "5.02TeV_40_50_n3_gfs_3", "5.02TeV_40_50_n3_gfs_4", "5.02TeV_40_50_n3_gfs_5", "5.02TeV_40_50_n3_gfs_6",
"5.02TeV_50_60_n2_gfs_0", "5.02TeV_50_60_n2_gfs_1", "5.02TeV_50_60_n2_gfs_2", "5.02TeV_50_60_n2_gfs_3", "5.02TeV_50_60_n2_gfs_4", "5.02TeV_50_60_n2_gfs_5", "5.02TeV_50_60_n2_gfs_6",
"5.02TeV_50_60_n3_gfs_0", "5.02TeV_50_60_n3_gfs_1", "5.02TeV_50_60_n3_gfs_2", "5.02TeV_50_60_n3_gfs_3", "5.02TeV_50_60_n3_gfs_4", "5.02TeV_50_60_n3_gfs_5", "5.02TeV_50_60_n3_gfs_6"
                        ]:
                            del pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0][:]
                            del pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1][:]
                            for j in xrange(0, Ngs):
                                pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][0].append([fns[-1].GetParameter(3*j+0), fns[-1].GetParameter(3*j+1), fns[-1].GetParameter(3*j+2)])
                            #pars["gfs_"+str(i)][1].append(fns[-1].Integral(-1.0, 1.0))
                            #pars["gfs_"+str(i)][1].append(hint)
                            pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(chisquare)
                            pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(hint)
                            pars[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode][1].append(fns[-1].Integral(-1.0, 1.0) - hint)
                            #pars[-1][-1][1].append(fns[-1].GetProb())
                        if True:
                            cs[energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+"_"+mode].Print("/afs/cern.ch/user/c/cirkovic/www/28-07-2016_temp1/"+energy+"_"+centrality+"_"+n+"_gfs_"+str(i)+".png")
                            #break
if True:
    pprint(pars)
    with open('pars3.json', 'w') as outfile:
        json.dump(pars, outfile)
                #for i in xrange(1, hs[-1].GetXaxis().GetNbins()):
                #    print hs[-1].GetBinCenter(i), hs[-1].GetBinContent(i)

                #fe = TFitEditor(cs[-1], hs[-1])

                #raw_input("Press enter to finish...")

sys.exit()

for i in xrange(0, 7):
    m = 0
    for k in xrange(1, Ntry):
        #if abs(pars[i][k][1][1] - pars[i][k][1][0]) * pars[i][k][1][2] < abs(pars[i][m][1][1] - pars[i][m][1][0]) * pars[i][m][1][2]:
        if pars[i][k][1][2] < pars[i][m][1][2]:
            m = k
    for j in xrange(0, Ngs):
        fns[i].SetParameter(3*j+0, pars[i][k][0][j][0])
        fns[i].SetParameter(3*j+1, pars[i][k][0][j][1])
        fns[i].SetParameter(3*j+2, pars[i][k][0][j][2])
    #fns[-1].SetParameters(1.0, 0.1, 0.0, 1.0, 0.2, 0.6, 1.0, 0.2, -0.6)
    cs.append(TCanvas())
    #if i in [4, 5, 6]:
    if True:
        hs[i].Fit("gfs"+str(i), "M")
    else:
        hs[i].Draw("HIST E0")

raw_input("Press enter to finish...")

