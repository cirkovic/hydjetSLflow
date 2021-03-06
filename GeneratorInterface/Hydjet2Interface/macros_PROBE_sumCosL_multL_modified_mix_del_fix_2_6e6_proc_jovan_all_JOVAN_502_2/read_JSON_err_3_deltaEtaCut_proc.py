from ROOT import *
import json
import sys

from multiprocessing import Process

gROOT.SetBatch(True)

ENABLE_M1_ABS = True
COMPARE_WITH_ERR = True
ERR_SQRT = True
err_scale = {'n2' : 0.7, 'n3' : 0.85}

options = "nostack c hist"
#options = "nostack l hist"
#options = "nostackb e0"
if COMPARE_WITH_ERR:
    optionse1 = "nostack e5"
else:
    optionse1 = "nostack c hist"
#optionse2 = "nostack e5"
optionse2 = "nostack hist e0"
#transparency = 0.35

#switches = [0, 1, 2, 3, 4]
#switches = [0, 2]
switches = [2]

#deltaEtaCuts = [1.0, 1.5, 2.0, 2.5, 3.0]
deltaEtaCuts = [ 2.0 ]

centralities = ['00_05', '05_10', '10_15', '15_20', '20_25', '25_30', '30_35', '35_40', '40_50', '50_60', '60_70', '70_80']
#centralities = ['40_50', '50_60']
#centralities = ['00_05', '00_10', '30_40', '40_50', '50_60']
#centralities = ['00_05', '30_40', '50_60']
#centralities = ['30_40']
#centralities = ['50_60']

centralities.reverse() 

#outdir = '~/www/21-05-2016/hydjet/3'
#outdir = '~/www/27-05-2016/hydjet/3'
indir=''
with open('INPUT.txt', 'r') as myfile:
    indir = myfile.read().replace('\n', '')
outdir=''
with open(indir+'OPATH.txt', 'r') as myfile:
    outdir = myfile.read().replace('\n', '')
outdir = outdir + '3/'
#print outdir

def loop(s, n, d):

    N = 11

    hs = []
    hss = []
    ls = []
    cs = []


    hss.append(THStack('evs_'+n, 'evs_'+n))
    ls.append(TLegend(0.7,0.7,0.9,0.9))

    for col, c in enumerate(centralities):
        with open(str(s)+'/'+str(d)+'/'+c+'/'+c+'/data_'+n+'/clean_eigenvalues_11x11.json') as df:
            data = json.load(df)
            hs.append(TH1F(c+'_'+n, c+'_'+n, N, -0.5, N-0.5))
            for i in xrange(0,N):
                #print data[str(i+1)]
                hs[-1].SetBinContent(i+1, data[str(i+1)])
            #print
            hs[-1].SetLineColor(col+1)
            hs[-1].SetLineWidth(2)
            hss[-1].Add(hs[-1])
            ls[-1].AddEntry(hs[-1], c)

    cs.append(TCanvas())
    hss[-1].Draw(options)
    ls[-1].Draw()
    cs[-1].SetLogy()
    cs[-1].Print(outdir+'/'+str(s)+'/'+str(d)+'/'+n+'/evs_'+n+'.png')

    hss_hs = []

    for mode in ['mode1', 'mode2']:
        if ERR_SQRT and mode == 'mode1':
            hss.append(THStack(mode+'_'+n, mode+'_'+n+'_E^'+str(err_scale[n])))
        else:
            hss.append(THStack(mode+'_'+n, mode+'_'+n))
        ls.append(TLegend(0.1,0.7,0.3,0.9))
        for col, c in enumerate(centralities):
            mlines = None
            #elines = None
            with open(str(s)+'/'+str(d)+'/'+c+'/'+c+'/data_'+n+'/modes/'+mode+'.dat') as fm:
                mlines = fm.read().splitlines()
            with open(str(s)+'/'+str(d)+'/'+c+'/'+c+'/data_'+n+'/errors/'+mode+'_error.dat') as fe:
                elines = fe.read().splitlines()
            #print c, mlines, elines
            hs.append(TH1F(mode+'_'+c+'_'+n, mode+'_'+c+'_'+n, N, -0.5, N-0.5))
            for mi, mv in enumerate(mlines):
                #print data[str(i+1)]
                setv = float(mv)
                sete = float(elines[mi])
                if ENABLE_M1_ABS:
                    if mode == 'mode1':
                        setv = abs(setv)
                hs[-1].SetBinContent(mi+1, setv)
                if ERR_SQRT and mode == 'mode1':
                    hs[-1].SetBinError(mi+1, sete**err_scale[n])
                else:
                    hs[-1].SetBinError(mi+1, sete)
                
            hs[-1].SetLineColor(col+1)
            if COMPARE_WITH_ERR:
                hs[-1].SetFillColor(col+1)
                #hs[-1].SetFillColorAlpha(col+1, transparency)
                if mode == 'mode2':
                    hs[-1].SetFillStyle(col+3001)
            else:
                #hs[-1].SetLineColor(col+1)
                hs[-1].SetLineWidth(2)
            hss[-1].Add(hs[-1])
            hss_hs.append(hs[-1])
            ls[-1].AddEntry(hs[-1], c)

        cs.append(TCanvas())
        hss[-1].Draw(optionse1)
        ls[-1].Draw()
        cs[-1].Print(outdir+'/'+str(s)+'/'+str(d)+'/'+n+'/'+mode+'_'+n+'.png')


    for col, c in enumerate(centralities):
        #hss.append(THStack(mode+'_'+n, mode+'_'+n))
        hss.append(THStack('m1_vs_m2_'+n+'_'+c, 'm1_vs_m2_'+n+'_'+c))
        ls.append(TLegend(0.1,0.7,0.3,0.9))
        for mode in ['mode1', 'mode2']:
            mlines = None
            #elines = None
            with open(str(s)+'/'+str(d)+'/'+c+'/'+c+'/data_'+n+'/modes/'+mode+'.dat') as fm:
                mlines = fm.read().splitlines()
            with open(str(s)+'/'+str(d)+'/'+c+'/'+c+'/data_'+n+'/errors/'+mode+'_error.dat') as fe:
                elines = fe.read().splitlines()
            #print c, mlines, elines
            hs.append(TH1F(mode+'_'+c+'_'+n+'_1', mode+'_'+c+'_'+n+'_1', N, -0.5, N-0.5))
            for mi, mv in enumerate(mlines):
                #print data[str(i+1)]
                setv = float(mv)
                if float(mlines[-1]) < 0:
                    setv = -setv
                sete = float(elines[mi])
                if ENABLE_M1_ABS:
                    if mode == 'mode1':
                        setv = abs(setv)
                hs[-1].SetBinContent(mi+1, setv)
                hs[-1].SetBinError(mi+1, sete)
                
            hs[-1].SetLineColor(kBlue)
            #hs[-1].SetFillColor(col+1)
            #hs[-1].SetFillColorAlpha(col+1, transparency)
            #hs[-1].SetFillStyle(col+3001)
            #hs[-1].SetLineWidth(2)
            hss[-1].Add(hs[-1])
            hss_hs.append(hs[-1])
            ls[-1].AddEntry(hs[-1], c)

        cs.append(TCanvas())
        hss[-1].Draw(optionse2)
        ls[-1].Draw()
        cs[-1].Print(outdir+'/'+str(s)+'/'+str(d)+'/'+n+'/m1_vs_m2_'+n+'_'+c+'.png')

    for c in centralities:
        with open(str(s)+'/'+str(d)+'/'+c+'/'+c+'/data_'+n+'/Matrix_'+n+'_'+c+'_11x11.json') as df:
            data = json.load(df)
            hs.append(TH2F('M_'+c+'_'+n, 'M_'+c+'_'+n, N, -0.5, N-0.5, N, -0.5, N-0.5))
            for i in xrange(0, N):
                for j in xrange(0, N):
                    hs[-1].SetBinContent(i+1, j+1, data['V_'+str(i+1)+"_"+str(j+1)])
            cs.append(TCanvas())
            hs[-1].SetStats(False)
            hs[-1].Draw("COLZ TEXT")
            cs[-1].Print(outdir+'/'+str(s)+'/'+str(d)+'/'+n+'/M_'+n+'_'+c+'.png')

    #raw_input('Press enter to continue...')


if __name__ == "__main__":

    ps = []

    for s in switches:
        for d in deltaEtaCuts:
            for n in ['n2', 'n3']:
                ps.append(Process(target=loop, args=(s, n, d)))
                ps[-1].start()

    for p in ps:
        p.join()

