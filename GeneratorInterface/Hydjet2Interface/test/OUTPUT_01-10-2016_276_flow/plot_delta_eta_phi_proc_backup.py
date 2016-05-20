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

    #fout = open('fout_'+str(case)+'_'+str(c)'.txt', 'w')
    #fout.close()

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
        h3.Divide(h1, h2, 1.0/h1.GetMaximum(), 1.0/h2.GetMaximum(), "B")
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

        #h3max = h3.GetMaximum()
        #h3.Rebin2D(3, 3)
        #h3.Scale(1.0/h3.GetMaximum()*h3max)
        #h3.Draw("surf1, fb")

        h3avg = 0.0
        n3avg = 0
        n3avgxy = [0, 0]
        for xi in xrange(1, h3.GetXaxis().GetNbins()+1):
            for yi in xrange(1, h3.GetYaxis().GetNbins()+1):
                if abs(h3.GetXaxis().GetBinCenter(xi)) >= 2.0:
                    h3avg += h3.GetBinContent(xi, yi)
                    n3avg += 1
                    if xi == 1: n3avgxy[1] += 1
                    if yi == 1: n3avgxy[0] += 1

        h3avg1 = h3avg
        h3avg /= n3avg
        for xi in xrange(1, h3.GetXaxis().GetNbins()+1):
            for yi in xrange(1, h3.GetYaxis().GetNbins()+1):
                if abs(h3.GetXaxis().GetBinCenter(xi)) < 2.0:
                    #h3.SetBinContent(xi, yi, h3avg)
                    h3.SetBinContent(xi, yi, 0.0)

        print "n3avgxy:", n3avgxy        
        hs.append(h3.Clone())
        hs[-1].Scale(1.0/n3avgxy[0])
        hs.append(h3.ProjectionX())
        h4 = hs[-1]
        hs.append(h3.ProjectionY())
        h5 = hs[-1]

        h3max = h3.GetMaximum()
        h3.Rebin2D(3, 3)
        h3.Scale(1.0/h3.GetMaximum()*h3max)
        h3.Draw("surf1, fb")

        if False:
            if c == "0-5":
                if i == 21:
                    #h3.SetMinimum()
                    h3.SetMaximum(0.9985)
                elif i == 25:
                    #h3.SetMinimum()
                    h3.SetMaximum(0.932)
                elif i == 3:
                    #h3.SetMinimum()
                    h3.SetMaximum(0.9985)
            elif c == "40-50":
                if i == 21:
                    #h3.SetMinimum()
                    h3.SetMaximum(0.991)
                elif i == 25:
                    #h3.SetMinimum()
                    h3.SetMaximum(0.69)
                elif i == 3:
                    #h3.SetMinimum()
                    h3.SetMaximum(0.998)
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

        #hs.append(h3.ProjectionX())
        #h4 = hs[-1]
        #print "n3avgxy:", n3avgxy
        #h4.Scale(1.0/n3avgxy[0])
        #hs.append(h3.ProjectionY())
        #h5 = hs[-1]
        #h5.Scale(1.0/n3avgxy[0])

        cs.append(TCanvas())
        cs[-1].Divide(2, 1, 0, 0)
        cs[-1].cd(1)
        h4.Draw()
        cs[-1].cd(2)
        h5.Draw()
        #fit = TF1("fit","[0]*(1+2*[1]*cos(x)+2*[2]*cos(2*x)+2*[3]*cos(3*x)+2*[4]*cos(4*x)+2*[5]*cos(5*x))", -1.5708, 4.712389)
        #fit = TF1("fit","[0]*(1+2*[1]*cos(x)+2*[2]*cos(2*x))", -1.5708, 4.712389)
        #fit = TF1("fit","[0]*(1+2*[1]*cos(x)+2*[2]*cos(2*x)+2*[3]*cos(3*x)+2*[4]*cos(4*x)+2*[5]*cos(5*x))", -1.5708, 4.712389)
        terms = []
        Nts = 5
        sarr = [1.0, 1e-4, 0.01, 0.01, 0.005, 0.005]
        for i in xrange(1, Nts+1):
            terms.append("2*["+str(i)+"]*cos("+str(i)+"*x)")
            #terms.append("["+str(i)+"]*cos("+str(i)+"*x)")
        terms = "+".join(terms)
        fit = TF1("fit","[0]*(1+"+terms+")", -math.pi/2, 3*math.pi/2)
        for i in xrange(0, Nts+1):
            fit.SetParameter(i, sarr[i])

        #cs[-1].Modified()
        #cs[-1].Update()

        h5.Fit("fit")

        #cs[-1].Modified()
        #cs[-1].Update()

        #pars = [fit.GetParameter(i),  for i in xrange(0, Nts+1)]
        #pares = [fit.GetParameterError(i) for i in xrange(0, Nts+1)]
        #if i in xrange(21, 28):
        #    with open('fout_'+str(case)+'_'+str(c)'.txt', 'wa') as fout:
        #        fout.write("%d\t%d\n" % (pars[1], pars[2]))
        #print "CIRKOVIC:", [fit.GetParameter(i) for i in xrange(0, 6)]

        #cs[-1].cd(1)
#        pt = TPaveText(.1, .1, .9, .9)
        #pt->AddText("A TPaveText can contain severals line of text.");
        #pt->AddText("They are added to the pave using the AddText method.");
        #pt->AddLine(.0,.5,1.,.5);
        #pt->AddText("Even complex TLatex formulas can be added:");
#        for i in xrange(0, 6):
#            pt.AddText(str(fit.GetParameter(i)))
#        pt.Draw("SAME")

        #cs[-1].Modified()
        #cs[-1].Update()

#        latex = TLatex()
#        latex.SetTextSize(0.025)
#        latex.SetTextAlign(13)
#        latex.DrawLatex(.2,.9,"K_{S}")
#        latex.DrawLatex(.3,.9,"K^{*0}")

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

