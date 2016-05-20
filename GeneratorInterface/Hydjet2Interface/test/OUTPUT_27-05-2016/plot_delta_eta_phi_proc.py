from ROOT import *
import sys

from multiprocessing import Process

gROOT.SetBatch(True)

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
outdir = '/afs/cern.ch/user/c/cirkovic/www/27-05-2016/hydjet/2'

def loop(case, ci, c):

    #fs.append(TFile.Open('output_'+str(N)+'_'+str(case)+'_'+c+'_'+str(deltaEtaCut)+'.root'))
    fs.append(TFile.Open('output_all_'+str(case)+'_'+c+'_'+str(deltaEtaCut)+'.root'))

    for i in xrange(0, 28):
        hs.append(fs[-1].Get('hdelta_eta_phiS'+str(i)))
        h1 = hs[-1]
        #cs.append(TCanvas())
        #h1.Draw("legoz")

        hs.append(fs[-1].Get('hdelta_eta_phiB'+str(i)))
        h2 = hs[-1]
        #cs.append(TCanvas())
        #h2.Draw("legoz")

        hs.append(h1.Clone())
        h3 = hs[-1]
        h3.Divide(h1, h2, 1.0, 1.0, "B")
        #cs.append(TCanvas())
        #h3.Draw("legoz")
        #raw_input('Press enter to finish...')
        #sys.exit()

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

