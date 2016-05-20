from ROOT import *
import sys
import math

from multiprocessing import Process

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gROOT.ForceStyle()

fs = []
hs = []
cs = []

Nevt = 5000
#N=6000000
#N=12000000

#centralities = ["0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
centralities = ["0-02", "0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
#centralities = ["0-02"]
#cases = [0, 1, 2, 3, 4]
cases = [2]

deltaEtaCut = 2.0

#outdir = '/afs/cern.ch/user/c/cirkovic/www/21-05-2016/hydjet/2'
#outdir = '/afs/cern.ch/user/c/cirkovic/www/27-05-2016/hydjet/2'
outdir=''
with open('OPATH.txt', 'r') as myfile:
    outdir = myfile.read().replace('\n', '')
outdir = outdir + '2/'
#print outdir

IPATH=''
with open('IPATH.txt', 'r') as myfile:
    IPATH = myfile.read().replace('\n', '')

def loop(case, ci, c):

    #fs.append(TFile.Open('output_'+str(N)+'_'+str(case)+'_'+c+'_'+str(deltaEtaCut)+'.root'))
    fs.append(TFile.Open(IPATH+'output_all_'+str(case)+'_'+c+'_'+str(deltaEtaCut)+'.root'))

    for i in xrange(0, 28):
    #for i in [21, 25, 3]:
        hs.append(fs[-1].Get('hdelta_eta_phiS'+str(i)))
        h1 = hs[-1]
        h1.GetXaxis().SetRangeUser(-4.0,4.0)
        #cs.append(TCanvas())
        #h1.Draw("legoz")

        hs.append(fs[-1].Get('hdelta_eta_phiB'+str(i)))
        h2 = hs[-1]
        h2.GetXaxis().SetRangeUser(-4.0,4.0)
        #cs.append(TCanvas())
        #h2.Draw("legoz")

        hs.append(h1.Clone())
        h3 = hs[-1]
        h3.Divide(h1, h2, 1.0, 1.0, "B")
        #for xi in xrange(1, h3.GetXaxis().GetNbins()+1):
        #    for yi in xrange(1, h3.GetYaxis().GetNbins()+1):
        #        h3.SetBinContent(xi, yi, math.log(h3.GetBinContent(xi, yi), 10))
        cs.append(TCanvas("c"+str(case)+c+str(i), "", 600, 550))
        cs[-1].SetLeftMargin(0.21)
        cs[-1].SetRightMargin(0.01)
        cs[-1].SetTopMargin(0.01)
        cs[-1].SetBottomMargin(0.05)
        #h3.Draw("lego2")
        #h3.SetLineColorAlpha(kBlue, 0.0)
        h3max = h3.GetMaximum()
        h3.Rebin2D(3, 3)
        h3.Scale(1.0/h3.GetMaximum()*h3max)
        h3.Draw("surf1, fb")
        #if True:
        if False:
            if c == "0-5":
                if i == 21:
                    h3.SetMinimum(1.006)
                    h3.SetMaximum(1.007)
                elif i == 25:
                    #h3.SetMinimum(1.005)
                    #h3.SetMaximum(1.009)
                    h3.SetMinimum(1.013)
                    h3.SetMaximum(1.032)
                elif i == 3:
                    #h3.SetMinimum(0.995)
                    #h3.SetMaximum(1.017)
                    h3.SetMinimum(1.005)
                    h3.SetMaximum(1.009)
            elif c == "40-50":
                if i == 21:
                    h3.SetMinimum(1.026)
                    h3.SetMaximum(1.04)
                elif i == 25:
                    #h3.SetMinimum(0.92)
                    #h3.SetMaximum(1.2)
                    h3.SetMinimum(1.0)
                    h3.SetMaximum(1.25)
                elif i == 3:
                    h3.SetMinimum(1.008)
                    h3.SetMaximum(1.06)
        h3.SetTitle("")
        h3.GetXaxis().SetTitle('#Delta#eta')
        h3.GetXaxis().SetTitleSize(0.045)
        h3.GetXaxis().CenterTitle(True)
        h3.GetXaxis().SetTitleOffset(1.5)
        h3.GetYaxis().SetTitle('#Delta#phi (radians)')
        h3.GetYaxis().SetTitleSize(0.045)
        h3.GetYaxis().CenterTitle(True)
        h3.GetYaxis().SetTitleOffset(1.5)
        #h3.GetZaxis().SetTitle('#frac{d^{2} N}{d #Delta #eta d #Delta #phi}')
        h3.GetZaxis().SetTitle('#frac{1}{N_{trig}} #frac{d^{2}N^{pair}}{d#Delta#eta d#Delta#phi}')
        h3.GetZaxis().SetTitleSize(0.045)
        h3.GetZaxis().CenterTitle(True)
        h3.GetZaxis().SetTitleOffset(2.2)
        #cs[-1].SetTheta(0)
        #cs[-1].SetPhi(-90)
        cs[-1].SetTheta(45)
        #cs[-1].SetPhi(30)
        cs[-1].SetPhi(45)
        #cs[-1].SetPhi(60)
        cs[-1].Update()
        cs[-1].Print(outdir+'/'+str(case)+'/2D_'+c+'_'+str(i)+'.png')
        cs[-1].Print(outdir+'/'+str(case)+'/2D_'+c+'_'+str(i)+'.pdf')

        hs.append(h3.ProjectionX())
        h4 = hs[-1]
        hs.append(h3.ProjectionY())
        h5 = hs[-1]
        cs.append(TCanvas())
        cs[-1].Divide(2, 1, 0, 0)
        cs[-1].cd(1)
        h4.Draw()
        cs[-1].cd(2)
        h5.Draw()
        cs[-1].Print(outdir+'/'+str(case)+'/proj_'+c+'_'+str(i)+'.png')
        cs[-1].Print(outdir+'/'+str(case)+'/proj_'+c+'_'+str(i)+'.pdf')
        #raw_input('Press enter to finish...')
        #sys.exit()

if __name__ == "__main__":

    ps = []

    for case in cases:
        for ci, cent in enumerate(centralities):
            ps.append(Process(target=loop, args=(case, ci, cent)))
            ps[-1].start()

    for p in ps:
        p.join()

    #raw_input('Press enter to finish...')

