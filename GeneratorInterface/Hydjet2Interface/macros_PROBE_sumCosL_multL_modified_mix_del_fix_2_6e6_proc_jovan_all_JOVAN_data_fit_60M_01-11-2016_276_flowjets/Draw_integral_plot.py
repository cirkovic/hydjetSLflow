from ROOT import *
import sys
#from subprocess import call
from subprocess import Popen, PIPE
from shlex import split

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

hs = []
cs = []
texs = []
legs = []
lns = []

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
            p1 = Popen(split("grep 2_np/2.0/"+s+"/"+s+"/data_"+n+"/modes/"+mode+".dat prompt.txt",), stdout=PIPE)
            out, err = p1.communicate()
            vals[n+", "+mode][s] = abs(float(out.split(' ')[1][:-1]))
            p1 = Popen(split("grep 2/2.0/"+s+"/"+s+"/data_"+n+"/errors/"+mode+"_error.dat prompt.txt",), stdout=PIPE)
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
        #hs.append(TH1F(n+"_"+mode, n+"_"+mode, 8, 0.5, 8.5))
        hs.append(TH1F(n+"_"+mode, n+"_"+mode, 1019, -2.05, 99.95))
        hs[-1].Sumw2()
        print n+"_"+mode
        #for si, s in enumerate(['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']):
        #    print "\t"+n+", "+mode+", "+s+": ", vals[n+", "+mode][s], vals[n+", "+mode+"_error"][s]
        #    hs[-1].SetBinContent(si+1, vals[n+", "+mode][s])
        #    hs[-1].SetBinError(si+1, vals[n+", "+mode+"_error"][s])
        xs = {
            '00_02': [0.0, 0.2],
            '00_05': [0.0, 5.0],
            '00_10': [0.0, 10.0],
            '10_20': [10.0, 20.0],
            '20_30': [20.0, 30.0],
            '30_40': [30.0, 40.0],
            '40_50': [40.0, 50.0],
            '50_60': [50.0, 60.0]
        }
        for si, s in enumerate(['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']):
            print "\t"+n+", "+mode+", "+s+": ", vals[n+", "+mode][s], vals[n+", "+mode+"_error"][s]
            #print (xs[s][0]+xs[s][1])/2, hs[-1].FindBin((xs[s][0]+xs[s][1])/2)
            nthbin = hs[-1].FindBin((xs[s][0]+xs[s][1])/2)
            hs[-1].SetBinContent(nthbin, vals[n+", "+mode][s])
            hs[-1].SetBinError(nthbin, vals[n+", "+mode+"_error"][s])
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

#gPad.SetMargin(
#    5.0*cs[-1].GetLeftMargin(),
#    5.0*cs[-1].GetRightMargin(),
#    5.0*cs[-1].GetBottomMargin(),
#    5.0*cs[-1].GetTopMargin()
#)
cs.append(TCanvas())
cs[-1].Divide(1, 2, 0, 0)

for ni, n in enumerate(["n2", "n3"]):
    #cs.append(TCanvas())
    cs[-1].cd(ni+1)

    pad = cs[-1].GetPad(ni+1)
    pad.SetLeftMargin(pad.GetLeftMargin()*1.8)
    pad.SetBottomMargin(pad.GetBottomMargin()*2.0)
    #pad.SetTopMargin(pad.GetTopMargin()*1.5)
    #pad.SetRightMargin(pad.GetRightMargin()*1.5)

    #cs[-1].SetLogy()
    hs[ni*3+2].SetMinimum(-0.05)
    hs[ni*3+2].SetMaximum(0.62)
    #hs[ni*3+2].GetYaxis().SetTitle("#frac{v^{(#alpha=2)}_{"+str(ni+2)+"}}{v^{(#alpha=1)}_{"+str(ni+2)+"}}")
    hs[ni*3+2].GetYaxis().SetTitle("#frac{v^{(2)}_{"+str(ni+2)+"}}{v^{(1)}_{"+str(ni+2)+"}}")
    hs[ni*3+2].GetYaxis().CenterTitle(True)
    #hs[ni*3+2].GetYaxis().SetTitleOffset(2.14)
    hs[ni*3+2].GetYaxis().SetTitleSize(1.5*hs[ni*3+2].GetYaxis().GetTitleSize())
    hs[ni*3+2].GetYaxis().SetTitleOffset(0.8)
    #hs[ni*3+2].GetYaxis().SetTitleFont(43)
    hs[ni*3+2].SetTitle("")
    hs[ni*3+2].SetLineColor(kBlack)
    hs[ni*3+2].SetMarkerStyle(21)
    hs[ni*3+2].SetMarkerSize(1.0)
    hs[ni*3+2].SetMarkerColor(kBlue)
    hs[ni*3+2].GetXaxis().SetNdivisions(507)
    hs[ni*3+2].GetYaxis().SetNdivisions(505)
    if ni == 1:
        hs[ni*3+2].GetXaxis().SetLabelSize(hs[ni*3+2].GetXaxis().GetLabelSize()*2.0)
    else:
        hs[ni*3+2].GetXaxis().SetLabelSize(0)
    hs[ni*3+2].GetYaxis().SetLabelSize(hs[ni*3+2].GetYaxis().GetLabelSize()*2.0)
    hs[ni*3+2].GetXaxis().SetTitleSize(hs[ni*3+2].GetXaxis().GetTitleSize()*3.0)
    hs[ni*3+2].GetYaxis().SetTitleSize(hs[ni*3+2].GetYaxis().GetTitleSize()*2.0)
    hs[ni*3+2].GetXaxis().SetTitleOffset(hs[ni*3+2].GetXaxis().GetTitleOffset()*0.9)
    hs[ni*3+2].GetYaxis().SetTitleOffset(hs[ni*3+2].GetYaxis().GetTitleOffset()*0.8)
    if ni == 1:
        hs[ni*3+2].GetXaxis().SetTitle("centrality (%)")
        hs[ni*3+2].GetXaxis().CenterTitle()
    hs[ni*3+2].Draw()
    if ni == 0:
        legs.append(TLegend(0.40, 0.85, 0.9, 0.95))
        leg = legs[-1]
        leg.SetBorderSize(0)
        leg.SetTextSize(0.06)
        leg.SetLineColor(1)
        leg.SetLineStyle(2)
        leg.SetLineWidth(1)

        entry=leg.AddEntry("", "#scale[1.5]{#bf{HYDJET++: PbPb #sqrt{s_{NN}} = 2.76 TeV}}", "p")
        entry.SetLineColor(1)
        entry.SetLineStyle(1)
        entry.SetLineWidth(4)
        entry.SetMarkerColor(kBlue)
        entry.SetMarkerStyle(21)
        entry.SetMarkerSize(1.5)

        leg.Draw("same")

        #texs.append(TLatex(0.7, 0.7, "#scale[1.1]{HYDJET++: PbPb #sqrt{s_{NN}} = 2.76 TeV}"))
        #texs.append(TLatex(0.76, 0.75, "#scale[1.5]{2.5 < p_{T} < 3.0 GeV/c}"))
        texs.append(TLatex(0.528, 0.75, "#scale[1.5]{2.5 < p_{T} < 3.0 GeV/c}"))
        texs[-1].SetNDC()
        texs[-1].SetLineWidth(2)
        texs[-1].Draw("same")

    #cs[-1].Print(output+"/"+n+".png")
    if ni == 1:
        fit0 = TF1("fit0", "[0]", -2.05, 99.95)
        fit0.SetParameter(0, 0.5)
        ############################################################
        #hs[ni*3+2].Fit("fit0")
        # vrednost za p0 iznosi 9.45499e-02, a za gresku 8.67712e-03
        ############################################################
        #fit1 = TF1("fit1", "[0]*x", 0.0, 100.0)
        #fit1.SetParameter(0, 0.5)
        #hs[ni*3+2].Fit("fit1")

    #hs[ni*3+2].GetXaxis().SetRangeUser(0, 99.9999)
    lns.append(TLine(-2.05, 0, 99.95, 0))
    lns[-1].Draw("same")

cs[-1].Print(output+"/n2n3.png")
cs[-1].Print(output+"/n2n3.pdf")


raw_input('Press enter to finish...')

