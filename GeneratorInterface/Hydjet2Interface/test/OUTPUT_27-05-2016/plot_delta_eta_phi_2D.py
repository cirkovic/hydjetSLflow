from ROOT import *
import sys

fs = []
hs = []
cs = []

centralities = ["0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
#outdir = '/afs/cern.ch/user/c/cirkovic/www/31-03-2016/hydjet/1'
outdir = '/afs/cern.ch/user/c/cirkovic/www/31-03-2016/hydjet/4'
outdir = '/afs/cern.ch/user/c/cirkovic/www/01-04-2016/hydjet/2'
outdir = '/afs/cern.ch/user/c/cirkovic/www/11-04-2016/hydjet/2'

for c in centralities:
    fs.append(TFile.Open('output_0_50_'+c+'_all.root'))
    for i in xrange(0, 27):
        hs.append(fs[-1].Get('hdelta_eta_phiS'+str(i)))
        h1 = hs[-1]
        cs.append(TCanvas())
        h1.Draw("legoz")

        hs.append(fs[-1].Get('hdelta_eta_phiB'+str(i)))
        h2 = hs[-1]
        cs.append(TCanvas())
        h2.Draw("legoz")

        hs.append(h1.Clone())
        h3 = hs[-1]
        h3.Divide(h1, h2, 1.0, 1.0, "B")
        cs.append(TCanvas())
        h3.Draw("legoz")
        raw_input('Press enter to finish...')
        sys.exit()

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
        cs[-1].Print(outdir+'/proj_'+c+'_'+str(i)+'.png')
        raw_input('Press enter to finish...')
        sys.exit()

raw_input('Press enter to finish...')

