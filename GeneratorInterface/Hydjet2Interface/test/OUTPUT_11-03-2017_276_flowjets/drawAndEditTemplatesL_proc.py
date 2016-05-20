from ROOT import *
import sys
from subprocess import call

from multiprocessing import Process

#call('rm FORMOUT_*.root', shell=True)
#call('python editTree.py', shell=True)
call("cp -f ./TEMPLATES/out_*.root .", shell=True)

binsns = []
#Na = 7
Na = 14
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
OPATH=''
with open('OPATH.txt', 'r') as myfile:
    OPATH = myfile.read().replace('\n', '')
OPATH = OPATH + '1/'
#print OPATH

IPATH=''
with open('IPATH.txt', 'r') as myfile:
    IPATH = myfile.read().replace('\n', '')

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
#centralities = ["0-02", "0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
centralities = ["0-02", "50-60"]
#centralities = ["0-02"]
#centralities = ["30-40"]
#ocentralities = ["00_05", "00_10", "10_20", "20_30", "30_40", "40_50", "50_60"]
#ocentralities = ["00_02", "00_05", "00_10", "10_20", "20_30", "30_40", "40_50", "50_60"]
ocentralities = ["00_02", "50_60"]
#ocentralities = ["00_02"]
#ocentralities = ["30_40"]
deltaEtaCut = 2.0

#farr = [21, 0, 1, 2, 3, 4, 5, 22, 6, 7, 8, 9, 10, 23, 11, 12, 13, 14, 24, 15, 16, 17, 25, 18, 19, 26, 20, 27]
farr = [91, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 92, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 93, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 94, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 95, 46, 47, 48, 49, 50, 51, 52, 53, 54, 96, 55, 56, 57, 58, 59, 60, 61, 62, 97, 63, 64, 65, 66, 67, 68, 69, 98, 70, 71, 72, 73, 74, 75, 99, 76, 77, 78, 79, 80, 100, 81, 82, 83, 84, 101, 85, 86, 87, 102, 88, 89, 103, 90, 104]
#farr_rev = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 19, 20, 21, 23, 24, 26, 0, 7, 13, 18, 22, 25, 27]
farr_rev = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 55, 56, 57, 58, 59, 61, 62, 63, 64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 85, 86, 87, 88, 89, 91, 92, 93, 94, 96, 97, 98, 100, 101, 103, 0, 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 102, 104]
#mp = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)]
#mp = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (3, 5), (3, 6), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 6)]
mp = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (10, 10), (10, 11), (10, 12), (10, 13), (11, 11), (11, 12), (11, 13), (12, 12), (12, 13), (13, 13)]


def loop(case, ci, cent):
    fout = TFile.Open("g1ds_"+str(case)+"_"+str(cent)+".root", "RECREATE")
    fout.Close()

    cs = []
    hs = {}
    g1hs = {}

    opath = OPATH+str(case)+'/'+str(cent)+'/'

    #ftmp = TFile.Open('output_'+str(N)+'_'+str(case)+'_'+str(cent)+'_'+str(deltaEtaCut)+'.root')
    ftmp = TFile.Open(IPATH+'output_all_'+str(case)+'_'+str(cent)+'_'+str(deltaEtaCut)+'.root')

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
    #for i in xrange(0, 28):
    for i in xrange(0, 105):
        for hni, hn in enumerate([ "hmult1L", "hmult2L" ]):
            hname = hn+str(mp[farr_rev[i]][hni])
            hs[hname] = ftmp.Get(hname.replace("hmult2L", "hmult1L"))
            cs.append(TCanvas())
            #print hname
            hs[hname].Draw()
            ### WRITING PART
            #if i in [21, 22, 23, 24, 25, 26, 27] and hn == "hmult1L":
            if i in [91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104] and hn == "hmult1L":
                formout = TFile.Open('out_'+str(case)+'_'+ocentralities[ci]+'.root', "UPDATE")
                formout.cd("PCA/Q_VALUES/"+ocentralities[ci]+"/Multiplicity")
                hw = hs[hname].Clone()
                #wn = "P"+str(i-20)+"_multiplicity"
                wn = "P"+str(i-90)+"_multiplicity"
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
                cs[-1].Print(opath+hname+'.pdf')

    #for i in [x for x in xrange(0, 28)]:
    #for i in xrange(0, 28):
    for i in xrange(0, 105):
        for hni, hn in enumerate([ "hpt1L", "hpt2L" ]):
            hname = hn+str(mp[farr_rev[i]][hni])
            hs[hname] = ftmp.Get(hname.replace("hpt2L", "hpt1L"))
            cs.append(TCanvas())
            #print hname
            hs[hname].Draw()
#            ### WRITING PART
#            if i in [21, 22, 23, 24, 25, 26, 27] and hn == "hpt1L":
#                formout = TFile.Open('out_'+str(case)+'_'+ocentralities[ci]+'.root', "UPDATE")
#                formout.cd("PCA/Q_VALUES/"+ocentralities[ci]+"/Multiplicity")
#                hw = hs[hname].Clone()
#                wn = "P"+str(i-20)+"_multiplicity"
#                hw.SetName(wn)
#                hw.SetTitle(wn)
#                hw.Write(wn, TObject.kOverwrite)
#                formout.cd("../../../..")
#                formout.Close()
#            ### END OF THE WRITING
            #hname = hn+str(case)+str(i)
            hname = hn+str(i)
            if DOPLOTS:
                cs[-1].Print(opath+hname+'.png')
                cs[-1].Print(opath+hname+'.pdf')

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
                    cs[-1].Print(opath+hname+'.pdf')
    
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
                    cs[-1].Print(opath+hname+'.pdf')
    
#    m2d2 = TH2F("m2d2", "m2d2", 7, -0.5, 6.5, 7, -0.5, 6.5)
#    m2d3 = TH2F("m2d3", "m2d3", 7, -0.5, 6.5, 7, -0.5, 6.5)
    
#    g1d2 = TH1F("g1d2", "g1d2", 7, -0.5, 6.5)
#    g1d3 = TH1F("g1d3", "g1d3", 7, -0.5, 6.5)

    m2d2 = TH2F("m2d2", "m2d2", 14, -0.5, 13.5, 14, -0.5, 13.5)
    m2d3 = TH2F("m2d3", "m2d3", 14, -0.5, 13.5, 14, -0.5, 13.5)

    g1d2 = TH1F("g1d2", "g1d2", 14, -0.5, 13.5)
    g1d3 = TH1F("g1d3", "g1d3", 14, -0.5, 13.5)
    
    occs = []
    #farr = [21, 0, 1, 2, 3, 4, 5, 22, 6, 7, 8, 9, 10, 23, 11, 12, 13, 14, 24, 15, 16, 17, 25, 18, 19, 26, 20, 27]
    #for i in xrange(0, 7):
    for i in xrange(0, 14):
        #for j in xrange(0, 7):
        for j in xrange(0, 14):
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
    
    
    #for i in xrange(0, 7):
    for i in xrange(0, 14):
        #hname = 'hsum_cos_normL'+str((21+i)*2+0)
        hname = 'hsum_cos_normL'+str((91+i)*2+0)
        g1d2.SetBinContent(i+1, hs[hname].GetMean())
        g1d2.SetBinError(i+1, hs[hname].GetMeanError())
        #hname = 'hsum_cos_normL'+str((21+i)*2+1)
        hname = 'hsum_cos_normL'+str((91+i)*2+1)
        g1d3.SetBinContent(i+1, hs[hname].GetMean())
        g1d3.SetBinError(i+1, hs[hname].GetMeanError())
    
    cs.append(TCanvas())
    m2d2.Draw("COLZ TEXT")
    m2d2.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+m2d2.GetName()+'.png')
        cs[-1].Print(opath+m2d2.GetName()+'.pdf')
    cs.append(TCanvas())
    m2d3.Draw("COLZ TEXT")
    m2d3.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+m2d3.GetName()+'.png')
        cs[-1].Print(opath+m2d3.GetName()+'.pdf')
    
    cs.append(TCanvas())
    g1d2.Draw("E0")
    g1d2.SetStats(False)
    if DOPLOTS:
       cs[-1].Print(opath+g1d2.GetName()+'.png')
       cs[-1].Print(opath+g1d2.GetName()+'.pdf')
    cs.append(TCanvas())
    g1d3.Draw("E0")
    g1d3.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+g1d3.GetName()+'.png')
        cs[-1].Print(opath+g1d3.GetName()+'.pdf')
    
    cs.append(TCanvas())
    g1d2.SetName(g1d2.GetName()+"h")
    g1d2.SetTitle(g1d2.GetTitle()+"h")
    g1d2.Draw("HIST TEXT")
    g1d2.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+g1d2.GetName()+'.png')
        cs[-1].Print(opath+g1d2.GetName()+'.pdf')
    cs.append(TCanvas())
    g1d3.SetName(g1d3.GetName()+"h")
    g1d3.SetTitle(g1d3.GetTitle()+"h")
    g1d3.Draw("HIST TEXT")
    g1d3.SetStats(False)
    if DOPLOTS:
        cs[-1].Print(opath+g1d3.GetName()+'.png')
        cs[-1].Print(opath+g1d3.GetName()+'.pdf')

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

