from ROOT import *
from subprocess import call
import sys, os

#orking_dir = os.getcwd()

#print working_dir

#sys.exit()

call("cp -f ./TEMPLATES/out_*.root .", shell=True)

arr = []
Na = 7
for i in xrange(1, Na+1):
    for j in xrange(1, Na+1):
        if ((i, j) in arr) or ((j, i) in arr):
            continue
        else:
            arr.append((i, j))

#print arr

fs = []

centralities = ["00_05", "00_10", "10_20", "20_30", "30_40", "40_50", "50_60"]

for cent in centralities:

    fs.append(TFile.Open('out_'+cent+'.root'))
    f = fs[-1]

    gDirectory.cd("PCA/Q_VALUES/"+cent+"/Signal")
    #for i in ["n0", "n2", "n3"]:
    for i in ["n2", "n3"]:
        gDirectory.cd(i+"/COS_NORMED")
        #f.ls()
        for com in arr:
            h = gDirectory.Get("cosDelta_P"+str(com[0])+"P"+str(com[1]))
            print "cosDelta_P"+str(com[0])+"P"+str(com[1]), h.GetXaxis().GetNbins(), h.GetMean(), h.GetMeanError()
        #gDirectory.cd("..")
        gDirectory.cd("../..")
        print

raw_input('Press enter to finish...')

