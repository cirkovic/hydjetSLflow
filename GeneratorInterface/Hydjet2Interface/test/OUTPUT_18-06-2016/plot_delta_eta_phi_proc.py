from ROOT import *
import sys

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
#centralities = ["0-02", "0-5", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
centralities = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-50', '50-60', '60-70', '70-80']
#centralities = ['0-5', '10-15', '15-20', '25-30', '30-35', '50-60']
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

    #for i in xrange(0, 28):
    for i in xrange(0, 66):
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
        cs.append(TCanvas())
        h3.Draw("lego2")
        h3.SetTitle("")
        h3.GetXaxis().SetTitle('#Delta#eta')
        h3.GetXaxis().CenterTitle(True)
        h3.GetXaxis().SetTitleOffset(1.5)
        h3.GetYaxis().SetTitle('#Delta#phi (radians)')
        h3.GetYaxis().CenterTitle(True)
        h3.GetYaxis().SetTitleOffset(1.5)
        cs[-1].SetTheta(45)
        cs[-1].SetPhi(30)
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

