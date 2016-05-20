from ROOT import *
from subprocess import call
import sys

gROOT.SetBatch(True)
gStyle.SetOptStat(211)

odir = '~/www/03-04-2016/hydjet/3'
odir = '~/www/04-04-2016/hydjet/3'

cmbs = []
for i in xrange(1, 8):
    for j in xrange(1, 8):
        if (i, j) not in cmbs and (j, i) not in cmbs:
            cmbs.append((i, j))

#call(['cp', '-f', '30_40/out_30_40.root', 'out_30_40_test.root'])

centralities = ["30_40"]
sufxs = ["default", "my"]

fs = []
hs = []
cs = []
shs = []
Hs = {}

for sufx in sufxs:
    for cent in centralities:
        fs.append(TFile.Open(cent+'_'+sufx+'/out_'+cent+'.root', 'UPDATE'))
        f = fs[-1]

        hns = []
        hns += ['PCA/Q_VALUES/'+cent+'/Signal/n2/COS_NOT_NORMED/cosDelta_P'+str(i)+'P'+str(j) for (i, j) in cmbs]
        hns += ['PCA/Q_VALUES/'+cent+'/Signal/n2/COS_NORMED/cosDelta_P'+str(i)+'P'+str(j) for (i, j) in cmbs]
        hns += ['PCA/Q_VALUES/'+cent+'/Signal/n3/COS_NOT_NORMED/cosDelta_P'+str(i)+'P'+str(j) for (i, j) in cmbs]
        hns += ['PCA/Q_VALUES/'+cent+'/Signal/n3/COS_NORMED/cosDelta_P'+str(i)+'P'+str(j) for (i, j) in cmbs]

        #hns += ['PCA/Q_VALUES/'+cent+'/Background/n2/COS_NOT_NORMED/cosDelta_P'+str(i)+'P'+str(j) for (i, j) in cmbs]
        #hns += ['PCA/Q_VALUES/'+cent+'/Background/n2/COS_NORMED/cosDelta_P'+str(i)+'P'+str(j) for (i, j) in cmbs]
        #hns += ['PCA/Q_VALUES/'+cent+'/Background/n3/COS_NOT_NORMED/cosDelta_P'+str(i)+'P'+str(j) for (i, j) in cmbs]
        #hns += ['PCA/Q_VALUES/'+cent+'/Background/n3/COS_NORMED/cosDelta_P'+str(i)+'P'+str(j) for (i, j) in cmbs]

        hns += ['PCA/Q_VALUES/'+cent+'/Multiplicity/P'+str(j)+'_multiplicity' for j in xrange(1, 8)]

        vals = {
            cent+"/Signal/n2/COS_NOT_NORMED" : [['P'+str(i)+'P'+str(j), 0.0, 0.0] for (i, j) in cmbs],
            cent+"/Signal/n2/COS_NORMED" : [['P'+str(i)+'P'+str(j), 0.0, 0.0] for (i, j) in cmbs],
            cent+"/Signal/n3/COS_NOT_NORMED" : [['P'+str(i)+'P'+str(j), 0.0, 0.0] for (i, j) in cmbs],
            cent+"/Signal/n3/COS_NORMED" : [['P'+str(i)+'P'+str(j), 0.0, 0.0] for (i, j) in cmbs],
            cent+"/Multiplicity" : [['P'+str(j), 0.0, 0.0] for j in xrange(1, 8)],
        }

        #print len(hns)
        for hn in hns:
            hs.append(f.Get(hn))
            h = hs[-1]
            
            for key, value in vals.iteritems():
                if key in hn:
                    for vi, v in enumerate(value):
                        if v[0] in hn:
                            vals[key][vi][1] = h.GetMean()
                            vals[key][vi][2] = h.GetMeanError()

            cs.append(TCanvas())
            h.Draw()
            #cs[-1].Print(odir+'/'+sufx+'__'+cent+'__'+hn.replace('/', '__')+'.png')
            cs[-1].Print(odir+'/'+hn+'_'+cent+'_'+sufx+'.png')

        print vals

        for key, value in vals.iteritems():
            if sufx == 'default':
                Hs[key] = THStack(key, '')
            shs.append(TH1F(sufx+'/'+key, 'summary', len(value), 0.5, len(value)+0.5))
            ht = shs[-1]
            for vi, v in enumerate(value):
                ht.SetBinContent(vi+1, v[1])
                ht.SetBinError(vi+1, v[2])
            if sufx == 'default': ht.SetLineColor(2)
            elif sufx == 'my': ht.SetLineColor(3)
            Hs[key].Add(ht)

        hns = ['PCA/Q_VALUES/'+cent+'/'+i for i in ['Event_count', 'pair_fraction', 'Event_count_back', 'pair_fraction_back']]
        #print len(hns)
        for hn in hns:
            hs.append(f.Get(hn))
            h = hs[-1]
            hx = h.ProjectionX()
            hy = h.ProjectionY()

            cs.append(TCanvas())
            cs[-1].Divide(2, 1, 0, 0)
            cs[-1].cd(1)
            hx.Draw()
            cs[-1].cd(2)
            hy.Draw()
            cs[-1].Print(odir+'/'+hn+'_'+cent+'_'+sufx+'.png')


for key, H in Hs.iteritems():
    cs.append(TCanvas())
    H.Draw("nostack hist c")
    cs[-1].Print(odir+'/PCA/Q_VALUES/'+key+'/summary.png')

#raw_input("Press enter to finish...")

