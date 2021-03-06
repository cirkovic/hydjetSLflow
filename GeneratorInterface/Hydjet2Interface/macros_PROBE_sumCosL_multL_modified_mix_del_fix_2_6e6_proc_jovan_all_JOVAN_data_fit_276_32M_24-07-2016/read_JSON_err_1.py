from ROOT import *
import json
import sys

gROOT.SetBatch(True)

ENABLE_M1_ABS = True
COMPARE_WITH_ERR = True

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

centralities = ['00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']
#centralities = ['40_50', '50_60']
#centralities = ['00_05', '00_10', '30_40', '40_50', '50_60']
#centralities = ['00_05', '30_40', '50_60']
#centralities = ['30_40']

centralities.reverse() 

#outdir = '~/www/27-03-2016/hydjet/1'
#outdir = '~/www/28-03-2016/hydjet/1'
#outdir = '~/www/28-03-2016/hydjet/2'
#outdir = '~/www/28-03-2016/hydjet/3'
#outdir = '~/www/31-03-2016/hydjet/2'
outdir = '~/www/31-03-2016/hydjet/3'
outdir = '~/www/01-04-2016/hydjet/1'
outdir = '~/www/02-04-2016/hydjet/1'
outdir = '~/www/02-04-2016/hydjet_test/1'
outdir = '~/www/03-04-2016/hydjet/1'
outdir = '~/www/04-04-2016/hydjet/1'
outdir = '~/www/11-04-2016/hydjet/1'
outdir = '~/www/13-04-2016/hydjet/1'
outdir = '~/www/16-04-2016/hydjet/1'
outdir = '~/www/17-04-2016/hydjet/1'

#infs = ['00_05/00_05/data_n2/clean_eigenvalues_7x7.json', '00_10/00_10/data_n2/clean_eigenvalues_7x7.json', '10_20/10_20/data_n2/clean_eigenvalues_7x7.json', '20_30/20_30/data_n2/clean_eigenvalues_7x7.json', '30_40/30_40/data_n2/clean_eigenvalues_7x7.json', '40_50/40_50/data_n2/clean_eigenvalues_7x7.json', '50_60/50_60/data_n2/clean_eigenvalues_7x7.json']

N = 7

hs = []
hss = []
ls = []
cs = []

for n in ['n2', 'n3']:

    hss.append(THStack('evs_'+n, 'evs_'+n))
    ls.append(TLegend(0.7,0.7,0.9,0.9))

    for col, c in enumerate(centralities):
        with open(c+'/'+c+'/data_'+n+'/clean_eigenvalues_7x7.json') as df:
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
    cs[-1].Print(outdir+'/'+n+'/evs_'+n+'.png')

    hss_hs = []

    for mode in ['mode1', 'mode2']:
        hss.append(THStack(mode+'_'+n, mode+'_'+n))
        ls.append(TLegend(0.1,0.7,0.3,0.9))
        for col, c in enumerate(centralities):
            mlines = None
            #elines = None
            with open(c+'/'+c+'/data_'+n+'/modes/'+mode+'.dat') as fm:
                mlines = fm.read().splitlines()
            with open(c+'/'+c+'/data_'+n+'/errors/'+mode+'_error.dat') as fe:
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
        cs[-1].Print(outdir+'/'+n+'/'+mode+'_'+n+'.png')


    for col, c in enumerate(centralities):
        #hss.append(THStack(mode+'_'+n, mode+'_'+n))
        hss.append(THStack('m1_vs_m2_'+n+'_'+c, 'm1_vs_m2_'+n+'_'+c))
        ls.append(TLegend(0.1,0.7,0.3,0.9))
        for mode in ['mode1', 'mode2']:
            mlines = None
            #elines = None
            with open(c+'/'+c+'/data_'+n+'/modes/'+mode+'.dat') as fm:
                mlines = fm.read().splitlines()
            with open(c+'/'+c+'/data_'+n+'/errors/'+mode+'_error.dat') as fe:
                elines = fe.read().splitlines()
            #print c, mlines, elines
            hs.append(TH1F(mode+'_'+c+'_'+n+'_1', mode+'_'+c+'_'+n+'_1', N, -0.5, N-0.5))
            for mi, mv in enumerate(mlines):
                #print data[str(i+1)]
                setv = float(mv)
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
        cs[-1].Print(outdir+'/'+n+'/m1_vs_m2_'+n+'_'+c+'.png')

    for c in centralities:
        with open(c+'/'+c+'/data_'+n+'/Matrix_'+n+'_'+c+'_7x7.json') as df:
            data = json.load(df)
            hs.append(TH2F('M_'+c+'_'+n, 'M_'+c+'_'+n, N, -0.5, N-0.5, N, -0.5, N-0.5))
            for i in xrange(0, N):
                for j in xrange(0, N):
                    hs[-1].SetBinContent(i+1, j+1, data['V_'+str(i+1)+str(j+1)])
            cs.append(TCanvas())
            hs[-1].SetStats(False)
            hs[-1].Draw("COLZ TEXT")
            cs[-1].Print(outdir+'/'+n+'/M_'+n+'_'+c+'.png')

#raw_input('Press enter to continue...')

