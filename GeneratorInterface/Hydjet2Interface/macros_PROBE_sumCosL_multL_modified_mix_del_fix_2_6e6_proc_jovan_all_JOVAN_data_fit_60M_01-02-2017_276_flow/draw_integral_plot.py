from ROOT import *
import sys
#from subprocess import call
from subprocess import Popen, PIPE
from shlex import split

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

hs = []
cs = []

#outdir = '~/www/27-05-2016/hydjet/3'
indir=''
with open('INPUT.txt', 'r') as myfile:
    indir = myfile.read().replace('\n', '')
outdir=''
with open(indir+'OPATH.txt', 'r') as myfile:
    outdir = myfile.read().replace('\n', '')
output = outdir + '5/'

vals = {

"n2, mode1": {
                    '00_02': 0.01979,
                    '00_05': 0.05402,
                    '00_10': 0.07384,
                    '10_20': 0.13324,
                    '20_30': 0.1752,
                    '30_40': 0.21045,
                    '40_50': 0.24416,
                    '50_60': 0.27771,
},
"n2, mode2": {
                    '00_02': 0.01069,
                    '00_05': 0.01581,
                    '00_10': 0.01555,
                    '10_20': 0.01965,
                    '20_30': 0.03129,
                    '30_40': 0.02757,
                    '40_50': 0.04948,
                    '50_60': 0.09857,
},
"n3, mode1": {
                    '00_02': 0.02562,
                    '00_05': 0.05899,
                    '00_10': 0.0658,
                    '10_20': 0.08187,
                    '20_30': 0.0892,
                    '30_40': 0.09417,
                    '40_50': 0.09831,
                    '50_60': 0.10097,
},
"n3, mode2": {
                    '00_02': 0.00847,
                    '00_05': 0.00334,
                    '00_10': 0.01185,
                    '10_20': 0.00449,
                    '20_30': 0.01043,
                    '30_40': 0.03184,
                    '40_50': 0.00099,
                    '50_60': 0.00116,
},
"n2, mode1_error": {
                    '00_02': 6.8e-05,
                    '00_05': 2e-06,
                    '00_10': 3.2e-05,
                    '10_20': 1e-06,
                    '20_30': 8.3e-05,
                    '30_40': 2.6e-05,
                    '40_50': 3e-06,
                    '50_60': 4e-06,
},
"n2, mode2_error": {
                    '00_02': 0.001093,
                    '00_05': 0.001589,
                    '00_10': 0.001476,
                    '10_20': 0.001267,
                    '20_30': 0.001929,
                    '30_40': 0.002292,
                    '40_50': 0.003346,
                    '50_60': 0.003134,
},
"n3, mode1_error": {
                    '00_02': 3.5e-05,
                    '00_05': 2.3e-05,
                    '00_10': 3.6e-05,
                    '10_20': 5.3e-05,
                    '20_30': 2e-05,
                    '30_40': 8.1e-05,
                    '40_50': 9e-05,
                    '50_60': 0.000122,
},
"n3, mode2_error": {
                    '00_02': 0.002998,
                    '00_05': 0.000912,
                    '00_10': 0.002145,
                    '10_20': 0.001226,
                    '20_30': 0.002527,
                    '30_40': 0.016783,
                    '40_50': 0.001359,
                    '50_60': 0.011256,
}

}

print vals

for n in ["n2", "n3"]:
    for mode in ["mode1", "mode2"]:
        for s in ['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']:
            p1 = Popen(split("grep 0_np/2.0/"+s+"/"+s+"/data_"+n+"/modes/"+mode+".dat prompt.txt",), stdout=PIPE)
            out, err = p1.communicate()
            vals[n+", "+mode][s] = abs(float(out.split(' ')[1][:-1]))
            p1 = Popen(split("grep 0/2.0/"+s+"/"+s+"/data_"+n+"/errors/"+mode+"_error.dat prompt.txt",), stdout=PIPE)
            out, err = p1.communicate()
            vals[n+", "+mode+"_error"][s] = abs(float(out.split(' ')[1][:-1]))

print vals

#sys.exit()

for n in ["n2", "n3"]:
    for mode in ["mode1", "mode2"]:
        for s in ['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']:
            print n+", "+mode+", "+s+": ", vals[n+", "+mode][s], vals[n+", "+mode+"_error"][s]

for n in ["n2", "n3"]:
    coli = 1
    for mode in ["mode1", "mode2"]:
        hs.append(TH1F(n+"_"+mode, n+"_"+mode, 8, 0.5, 8.5))
        hs[-1].Sumw2()
        print n+"_"+mode
        for si, s in enumerate(['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']):
            print "\t"+n+", "+mode+", "+s+": ", vals[n+", "+mode][s], vals[n+", "+mode+"_error"][s]
            hs[-1].SetBinContent(si+1, vals[n+", "+mode][s])
            hs[-1].SetBinError(si+1, vals[n+", "+mode+"_error"][s])
        hs[-1].SetMinimum(1e-4)
        hs[-1].SetMaximum(1.0)
        hs[-1].SetLineColor(coli)
        coli += 1
    hr = hs[-1].Clone()
    hr.SetName(n+"r")
    hr.Divide(hs[-1], hs[-2], 1.0, 1.0, "B")
    hr.SetLineColor(coli)
    hs.append(hr)
    hs[-1].SetMinimum(1e-4)
    hs[-1].SetMaximum(1.0)

#n1->Sumw2(); d1->Sumw2(); // store sum of squares of weights (if not already done)
#TH1F *rat = d1->Clone(); rat->SetName("Ratio"); // Clone one of the histograms
#rat->Divide(n1,d1,1.,1.,"B");

print hs

for ni, n in enumerate(["n2", "n3"]):
    cs.append(TCanvas())
    cs[-1].SetLogy()
    isDrawn = False
    for modi, mode in enumerate(["mode1", "mode2"]):
        if isDrawn:
            hs[ni*3+modi].Draw("SAME")
        else:
            hs[ni*3+modi].Draw()
            isDrawn = True
    hs[ni*3+2].Draw("SAME")

for ni, n in enumerate(["n2", "n3"]):
    cs.append(TCanvas())
    #cs[-1].SetLogy()
    hs[ni*3+2].SetMinimum(0)
    hs[ni*3+2].SetMaximum(0.6)
    hs[ni*3+2].Draw()
    cs[-1].Print(output+"/"+n+".png")

raw_input('Press enter to finish...')

