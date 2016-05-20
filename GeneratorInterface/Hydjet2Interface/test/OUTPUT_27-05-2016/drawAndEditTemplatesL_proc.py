from ROOT import *
import sys
from subprocess import call

from multiprocessing import Process

#call('rm FORMOUT_*.root', shell=True)
#call('python editTree.py', shell=True)
call("cp -f ./TEMPLATES/out_*.root .", shell=True)

binsns = []
Na = 7
for i in xrange(1, Na+1):
    for j in xrange(1, Na+1):
        if ((i, j) in binsns) or ((j, i) in binsns):
            continue
        else:
            binsns.append((i, j))

gROOT.ForceStyle(True)
gStyle.SetOptStat(1000000211)
gStyle.SetStatW(0.3)

gROOT.SetBatch(True)

#OPATH = '/afs/cern.ch/user/c/cirkovic/www/21-05-2016/hydjet/1/'
OPATH = '/afs/cern.ch/user/c/cirkovic/www/27-05-2016/hydjet/1/'

DOHADD = False
DOPLOTS = True
ALL = True
#Nevt = 16
Nevt = 5000
#N=6000000
N=12000000
#NJOBS = 1#200
#NJOBS = 300
#NJOBS = 10
#NJOBS = 1500

#cases = [0, 1, 2, 3, 4]
cases = [2]
#cases = [0]
#centralities = ["0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
centralities = ["0-02", "0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
#centralities = ["0-02"]
#centralities = ["30-40"]
#ocentralities = ["00_05", "00_10", "10_20", "20_30", "30_40", "40_50", "50_60"]
ocentralities = ["00_02", "00_05", "00_10", "10_20", "20_30", "30_40", "40_50", "50_60"]
#ocentralities = ["00_02"]
#ocentralities = ["30_40"]
deltaEtaCut = 2.0

farr = [21, 0, 1, 2, 3, 4, 5, 22, 6, 7, 8, 9, 10, 23, 11, 12, 13, 14, 24, 15, 16, 17, 25, 18, 19, 26, 20, 27]
farr_rev = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 19, 20, 21, 23, 24, 26, 0, 7, 13, 18, 22, 25, 27]


def loop(case, ci, cent):
    fout = TFile.Open("g1ds_"+str(case)+"_"+str(cent)+".root", "RECREATE")
    fout.Close()

    cs = []
    hs = {}
    g1hs = {}

    opath = OPATH+str(case)+'/'+str(cent)+'/'

    #ftmp = TFile.Open('output_'+str(N)+'_'+str(case)+'_'+str(cent)+'_'+str(deltaEtaCut)+'.root')
    ftmp = TFile.Open('output_all_'+str(case)+'_'+str(cent)+'_'+str(deltaEtaCut)+'.root')

    for hni, hn in enumerate([ "pair_fraction_S", "pair_fraction_B", "event_count_S", "event_count_B" ]):
        hs[hn] = ftmp.Get(hn)
        formout = TFile.Open('out_'+str(case)+'_'+ocentralities[ci]+'.root', "UPDATE")
        formout.cd("PCA/Q_VALUES/"+ocentralities[ci])
        #print hn
        hw = hs[hn].Clone()
        wn = ["pair_fraction", "pair_fraction_back", "Event_count", "Event_count_back"][hni]
        hw.SetTitle(wn)
        hw.Write(wn, TObject.kOverwrite)
        formout.cd("../../..")
        formout.Close()
    
    #for i in [x for x in xrange(0, 28)]:
    for i in xrange(0, 28):
        for hn in [ "hmult1L", "hmult2L" ]:
            hname = hn+str(i)
            hs[hname] = ftmp.Get(hname)
            cs.append(TCanvas())
            #print hname
            hs[hname].Draw()
            ### WRITING PART
            if i in [21, 22, 23, 24, 25, 26, 27] and hn == "hmult1L":
                formout = TFile.Open('out_'+str(case)+'_'+ocentralities[ci]+'.root', "UPDATE")
                formout.cd("PCA/Q_VALUES/"+ocentralities[ci]+"/Multiplicity")
                hw = hs[hname].Clone()
                wn = "P"+str(i-20)+"_multiplicity"
                hw.SetName(wn)
                hw.SetTitle(wn)
                hw.Write(wn, TObject.kOverwrite)
                formout.cd("../../../..")
                formout.Close()
            ### END OF THE WRITING
            #hname = hn+str(case)+str(i)
            hname = hn+str(i)
            if DOPLOTS:
                cs[-1].Print(opath+hname+'.png')

        for hn in [ "hsum_cosL" ]:
            for j in xrange(0, 2):
                hname = hn+str(i*2+j)
                hs[hname] = ftmp.Get(hname)
                hname = hn+str(i*2+j)
                cs.append(TCanvas())
                hs[hname].Draw()
                ### WRITING PART
                #if j in [1, 2]:
                if True:
                    #formout = TFile.Open('FORMOUT_'+str(case)+'_'+ocentralities[ci]+'.root', "UPDATE")
                    #formout.mkdir("n"+str(j+1))
                    #formout.cd("n"+str(j+1))
                    formout = TFile.Open('out_'+str(case)+'_'+ocentralities[ci]+'.root', "UPDATE")
                    formout.cd("PCA/Q_VALUES/"+ocentralities[ci]+"/Signal/"+"n"+str(j+2)+"/COS_NOT_NORMED")
                    hw = hs[hname].Clone()
                    #wn = "cosDelta_"+"P"+str(binsns[i][0])+"P"+str(binsns[i][1])
                    wn = "cosDelta_"+"P"+str(binsns[farr_rev[i]][0])+"P"+str(binsns[farr_rev[i]][1])
                    hw.SetName(wn)
                    hw.SetTitle(wn)
                    hw.Write(wn, TObject.kOverwrite)
                    formout.cd("../../../../../..")
                    #formout.cd("..")
                    formout.Close()
                ### END OF THE WRITING
                #hname = hn+str(case)+str(i*3+j)
                hname = hn+str(i*2+j)
                if DOPLOTS:
                    cs[-1].Print(opath+hname+'.png')
    
        for hn in [ "hsum_cos_normL" ]:
            for j in xrange(0, 2):
                hname = hn+str(i*2+j)
                hs[hname] = ftmp.Get(hname)
                hname = hn+str(i*2+j)
                cs.append(TCanvas())
                hs[hname].Draw()
                ### WRITING PART
                #if j in [1, 2]:
                if True:
                    #formout = TFile.Open('FORMOUT_'+str(case)+'_'+ocentralities[ci]+'.root', "UPDATE")
                    #formout.mkdir("n"+str(j+1))
                    #formout.cd("n"+str(j+1))
                    formout = TFile.Open('out_'+str(case)+'_'+ocentralities[ci]+'.root', "UPDATE")
                    formout.cd("PCA/Q_VALUES/"+ocentralities[ci]+"/Signal/"+"n"+str(j+2)+"/COS_NORMED")
                    hw = hs[hname].Clone()
                    #wn = "cosDelta_"+"P"+str(binsns[i][0])+"P"+str(binsns[i][1])
                    wn = "cosDelta_"+"P"+str(binsns[farr_rev[i]][0])+"P"+str(binsns[farr_rev[i]][1])
                    hw.SetName(wn)
                    hw.SetTitle(wn)
                    hw.Write(wn, TObject.kOverwrite)
                    formout.cd("../../../../../..")
                    #formout.cd("..")
                    formout.Close()
                ### END OF THE WRITING
                #hname = hn+str(case)+str(i*3+j)
                hname = hn+str(i*2+j)
                if DOPLOTS:
                    cs[-1].Print(opath+hname+'.png')
    
    m2d2 = TH2F("m2d2", "m2d2", 7, -0.5, 6.5, 7, -0.5, 6.5)
    m2d3 = TH2F("m2d3", "m2d3", 7, -0.5, 6.5, 7, -0.5, 6.5)
    
    g1d2 = TH1F("g1d2", "g1d2", 7, -0.5, 6.5)
    g1d3 = TH1F("g1d3", "g1d3", 7, -0.5, 6.5)
    
    occs = []
    #farr = [21, 0, 1, 2, 3, 4, 5, 22, 6, 7, 8, 9, 10, 23, 11, 12, 13, 14, 24, 15, 16, 17, 25, 18, 19, 26, 20, 27]
    for i in xrange(0, 7):
        for j in xrange(0, 7):
            if (i, j) in occs or (j, i) in occs:
                continue
            else:
                k = len(occs)
                occs.append((i, j))
                hname = 'hsum_cos_normL'+str(farr[k]*2+0)
                m2d2.SetBinContent(i+1, j+1, hs[hname].GetMean())
                m2d2.SetBinContent(j+1, i+1, hs[hname].GetMean())
                m2d2.SetBinError(i+1, j+1, hs[hname].GetMeanError())
                m2d2.SetBinError(j+1, i+1, hs[hname].GetMeanError())
    
                hname = 'hsum_cos_normL'+str(farr[k]*2+1)
                m2d3.SetBinContent(i+1, j+1, hs[hname].GetMean())
                m2d3.SetBinContent(j+1, i+1, hs[hname].GetMean())
    
    
    for i in xrange(0, 7):
        hname = 'hsum_cos_normL'+str((21+i)*2+0)
        g1d2.SetBinContent(i+1, hs[hname].GetMean())
        g1d2.SetBinError(i+1, hs[hname].GetMeanError())
        hname = 'hsum_cos_normL'+str((21+i)*2+1)
        g1d3.SetBinContent(i+1, hs[hname].GetMean())
        g1d3.SetBinError(i+1, hs[hname].GetMeanError())
    
    cs.append(TCanvas())
    m2d2.Draw("COLZ TEXT")
    m2d2.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+m2d2.GetName()+'.png')
    cs.append(TCanvas())
    m2d3.Draw("COLZ TEXT")
    m2d3.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+m2d3.GetName()+'.png')
    
    cs.append(TCanvas())
    g1d2.Draw("E0")
    g1d2.SetStats(False)
    if DOPLOTS:
       cs[-1].Print(opath+g1d2.GetName()+'.png')
    cs.append(TCanvas())
    g1d3.Draw("E0")
    g1d3.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+g1d3.GetName()+'.png')
    
    cs.append(TCanvas())
    g1d2.SetName(g1d2.GetName()+"h")
    g1d2.SetTitle(g1d2.GetTitle()+"h")
    g1d2.Draw("HIST TEXT")
    g1d2.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+g1d2.GetName()+'.png')
    cs.append(TCanvas())
    g1d3.SetName(g1d3.GetName()+"h")
    g1d3.SetTitle(g1d3.GetTitle()+"h")
    g1d3.Draw("HIST TEXT")
    g1d3.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+g1d3.GetName()+'.png')

    fout = TFile.Open("g1ds_"+str(case)+"_"+str(cent)+".root", "UPDATE")
    g1d2.SetName(g1d2.GetName()+"_"+cent)
    g1d2.SetTitle(g1d2.GetTitle()+"_"+cent)
    g1d2.Write()
    g1d3.SetName(g1d3.GetName()+"_"+cent)
    g1d3.SetTitle(g1d3.GetTitle()+"_"+cent)
    g1d3.Write()
    fout.Close()


if __name__ == "__main__":
    
    ps = []
    
    for case in cases:
        for ci, cent in enumerate(centralities):
            ps.append(Process(target=loop, args=(case, ci, cent)))
            ps[-1].start()

    for p in ps:
        p.join()

