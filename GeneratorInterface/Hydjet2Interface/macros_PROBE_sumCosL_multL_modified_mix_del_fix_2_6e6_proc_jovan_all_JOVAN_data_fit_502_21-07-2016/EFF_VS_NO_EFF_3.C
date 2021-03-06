#include <iostream>
#include <sstream>
#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TMath.h"
#include <iterator>
#include "TFile.h"
#include "TClassTable.h"
#include <vector>
#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TKey.h"
#include "TCanvas.h"
#include <math.h>
#include <fstream>
#include <string>
#include <streambuf>

#include "rapidjson/document.h"     // rapidjson's DOM-style API
#include "rapidjson/prettywriter.h" // for stringify JSON
#include "rapidjson/filereadstream.h"
#include <cstdio>


using namespace rapidjson;
using namespace std;

double maximum = 0.29;
//double lvpos = 0.13/0.29*maximum;
double lvpos = 0.8*maximum;

double* GetArray(Document& document, const Value& a){

   //const Value& a = document[Key]; // Using a reference for consecutive access is handy and faster.
   assert(a.IsArray());

   int count=-1;
   double* array=new double[10];

   for (Value::ConstValueIterator itr = a.Begin(); itr != a.End(); ++itr){

        count++;
        array[count]=itr->GetDouble();

    }

    return array;

}


TH1D* DefineHist(TString check){

   TH1D* hist = new TH1D("hist","",100,0.01,3.5);
   hist->SetMinimum(-0.05);
   hist->SetMaximum(maximum);
   hist->SetStats(0);
   hist->SetLineStyle(0);
   hist->SetLineWidth(0);
   hist->SetMarkerStyle(20);
   hist->SetMarkerSize(1.0);
   hist->GetXaxis()->SetNdivisions(505);
   hist->GetXaxis()->SetLabelFont(43);
   hist->GetXaxis()->SetLabelOffset(0.015);
   hist->GetXaxis()->SetLabelSize(16);
   hist->GetXaxis()->SetTitleSize(20);
   hist->GetXaxis()->SetTitleFont(43);
   hist->GetYaxis()->SetLabelOffset(0.015);
   
   if (check=="P5"|| check=="P6" || check=="P7" || check=="P8") {

       hist->GetXaxis()->SetTitle("p_{T} (GeV/c)");
       hist->GetXaxis()->CenterTitle(true);
       hist->GetXaxis()->SetTitleOffset(2.47);

   }

   if (check=="P1"|| check=="P5" ) {
      hist->GetYaxis()->SetTitle("v^{(#alpha)}_{3}");
      hist->GetYaxis()->CenterTitle(true);
      hist->GetYaxis()->SetTitleOffset(2.14);
      hist->GetYaxis()->SetTitleSize(25.5);
      hist->GetYaxis()->SetTitleFont(43);
   }
   hist->GetYaxis()->SetNdivisions(505);
   hist->GetYaxis()->SetLabelFont(43);
   hist->GetYaxis()->SetLabelSize(15);

   return hist;


}

void DoLegend(){

   //TLegend *leg = new TLegend(0.7, 0.55, 0.9, 0.66, NULL,"brNDC");
   TLegend *leg = new TLegend(0.3, 0.3, 0.9, 0.6, NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextSize(0.06);
   leg->SetLineColor(1);
   leg->SetLineStyle(2);
   leg->SetLineWidth(1);
 
   TLegendEntry *entry;
   /*
   entry=leg->AddEntry("", "#alpha=1 n=2","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kBlue);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=2 n=2","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kRed);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1.2);
   */

   //entry=leg->AddEntry("", "v_{2}{|#Delta#eta|>0.8}, ALICE PLB 708 (2012) 249","p");
   entry=leg->AddEntry("", "v_{3}{|#Delta#eta|>0.8} ALICE","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kBlack);
   entry->SetMarkerStyle(24);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "UCC paper","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kOrange);
   entry->SetMarkerStyle(24);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=1","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   //entry->SetMarkerColor(kMagenta);
   //entry->SetMarkerStyle(25);
   entry->SetMarkerColor(kBlue);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=2","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   //entry->SetMarkerColor(kBlack);
   //entry->SetMarkerStyle(25);
   entry->SetMarkerColor(kRed);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "fit","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kGreen);
   entry->SetMarkerStyle(34);
   entry->SetMarkerSize(1.2);


   leg->Draw();


}

void DoLatex(double x, double y, TString text){

   TLatex *   tex = new TLatex(x, y, text);
   tex->SetNDC();
   tex->SetLineWidth(2);
   tex->Draw();

}

void DoText(TString text){

   //TText *t = new TText(2.45,lvpos, text);
   TText *t = new TText(0.3,lvpos, text);
   //t->SetTextAlign(22);
   //t->SetTextColor(kRed+2);
   t->SetTextFont(43);
   t->SetTextSize(15);
   //t->SetTextAngle(45);
   t->Draw();


}

void DoLine(){

   TLine *line1 = new TLine(0,0,3.5,0);
   line1->SetLineColor(1);
   line1->SetLineStyle(0);
   line1->Draw();


}

void PlotData(double* pt, double* data, double* data_error, Color_t color, int MarkerStyle, double MarkerSize, TString point){

   gre = new TGraphErrors(7);
   gre->SetTitle("Graph");
   gre->SetFillColor(1);
   gre->SetLineWidth(2);
   gre->SetLineColor(color);
   gre->SetMarkerColor(color);
   gre->SetMarkerStyle(MarkerStyle);
   gre->SetMarkerSize(MarkerSize);

   if (point=="2") gre->SetFillColor(kRed-9);

   for (int i=0; i<7; i++){
        
          if (pt[6] < 0 && data[6] < 0)
          {
              gre->SetPoint(i,-pt[i], -data[i]);
              if (point!="2") gre->SetPointError(i,0, data_error[i]);
              if (point=="2") gre->SetPointError(i,0.08, data_error[i]);
          }
          else if (pt[6] < 0 && data[6] >= 0)
          {
              gre->SetPoint(i,-pt[i], data[i]);
              if (point!="2") gre->SetPointError(i,0, data_error[i]);
              if (point=="2") gre->SetPointError(i,0.08, data_error[i]);
          }
          else if (pt[6] >= 0 && data[6] < 0)
          {
              gre->SetPoint(i,pt[i], -data[i]);
              if (point!="2") gre->SetPointError(i,0, data_error[i]);
              if (point=="2") gre->SetPointError(i,0.08, data_error[i]);
          }
          else if (pt[6] >= 0 && data[6] >= 0)
          {
              gre->SetPoint(i,pt[i], data[i]);
              if (point!="2") gre->SetPointError(i,0, data_error[i]);
              if (point=="2") gre->SetPointError(i,0.08, data_error[i]);
          }

   }

   gre->Draw(point);


}

void MakeHisto(TString plot,
               double x_min, 
               double y_min,
               double x_max,
               double y_max,
               double LeftMargin,
               double RightMargin,
               double TopMargin,
               double BottomMargin,
               bool REMOVE_Y_LABEL = false
              ){

   TPad *p_0_0 = new TPad(plot, plot, x_min, y_min, x_max, y_max);
   p_0_0->Draw();
   p_0_0->cd();
   p_0_0->SetFillColor(0);
   p_0_0->SetBorderMode(0);
   p_0_0->SetBorderSize(2);
   p_0_0->SetTickx(1);
   p_0_0->SetTicky(1);
   p_0_0->SetLeftMargin(LeftMargin);
   p_0_0->SetRightMargin(RightMargin);
   p_0_0->SetTopMargin(TopMargin);
   p_0_0->SetBottomMargin(BottomMargin);
   p_0_0->SetFrameFillStyle(0);
   p_0_0->SetFrameLineStyle(0);
   p_0_0->SetFrameBorderMode(0);
   p_0_0->SetFrameFillStyle(0);
   p_0_0->SetFrameLineStyle(0);
   p_0_0->SetFrameBorderMode(0);

   TH1D* hist1=DefineHist(plot);
   hist1->Draw("");
   if (REMOVE_Y_LABEL)
      hist1->GetYaxis()->SetLabelSize(0);

   //p_0_0->Modified();
   //return p_0_0;

}

Document READFILE(TString file){

   FILE * pFile = fopen (file , "r");
   char buffer[65536];
   FileReadStream is(pFile, buffer, sizeof(buffer));

   Document document;  // MAIN JSON OBJECT
   document.ParseStream<0>(is); //mandatory

   return document;

}


double* ReadData(Document& document, const char* data_name){

   double* temp_ptr;  
   const Value& input = document[data_name]; // Using a reference for consecutive access is handy and faster.
   temp_ptr=GetArray(document, input);
   
   return temp_ptr;
}


void EFF_VS_NO_EFF_3(const char *s, const char *deta){

   //////////////////////////////////////////////////////////////////////////////////////////////////////////
   // 10-20 20-30 30-40 40-50

   int Nbd = 12;

   // UCC paper
   double x20_arr[] = {0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.36, 4.38, 5.41, 6.75, 9.87};
   double y20_arr[] = {0.0074, 0.0129, 0.0204, 0.0387, 0.0488, 0.0584, 0.0685};
   double y20_err[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

   // ALICE
   double x31_arr[] = {0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.36, 4.38, 5.41, 6.75, 9.87};
   double y31_arr[] = {0.0116, 0.0223, 0.0332, 0.0475, 0.0673, 0.0862, 0.0996, 0.107, 0.0987, 0.0719, 0.0402, 0.0246};
   double y31_err[] = {0.0002, 0.0002, 0.0003, 0.0004, 0.0007, 0.0011, 0.0016, 0.001, 0.0027, 0.0058, 0.0096, 0.0144};

   double x32_arr[] = {0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.36, 4.39, 5.41, 6.75, 9.85};
   double y32_arr[] = {0.0129, 0.0249, 0.0371, 0.0529, 0.0744, 0.0928, 0.105, 0.111, 0.0961, 0.0721, 0.0437, 0.0284};
   double y32_err[] = {0.0002, 0.0002, 0.0003, 0.0005, 0.0009, 0.0013, 0.001, 0.002, 0.0031, 0.0057, 0.0081, 0.0126};

   double x33_arr[] = {0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.37, 4.39, 5.41, 6.75, 9.82};
   double y33_arr[] = {0.0138, 0.0266, 0.0399, 0.0566, 0.0788, 0.0964, 0.108, 0.108, 0.0933, 0.0684, 0.0504, 0.00768};
   double y33_err[] = {0.0002, 0.0002, 0.0003, 0.0005, 0.0009, 0.0014, 0.002, 0.002, 0.004, 0.0069, 0.0099, 0.01595};

   double x34_arr[] = {0.41, 0.614, 0.864, 1.21, 1.71, 2.21, 2.71, 3.37, 4.39, 5.42, 6.75, 9.81};
   double y34_arr[] = {0.0137, 0.0271, 0.0413, 0.0583, 0.0807, 0.0953, 0.102, 0.102, 0.0804, 0.0532, 0.0232, -0.0303};
   double y34_err[] = {0.0003, 0.0004, 0.0005, 0.0006, 0.0012, 0.0017, 0.002, 0.003, 0.0061, 0.0124, 0.0169, 0.0258};

   ///////////////////////////////////////////////////////////////////////////////////////////////////////////


   TCanvas *cc1 = new TCanvas("cc1", "cc1",40,40,935,648);
   gStyle->SetOptStat(0);
   cc1->SetFillColor(0);
   cc1->SetBorderMode(0);
   cc1->SetLeftMargin(0.2);
   cc1->SetRightMargin(0.5);
   cc1->SetBorderSize(10);
   cc1->SetTickx(1);
   cc1->SetTicky(1);

   Double_t W  = 0.233;          // Pad Width
   Int_t    Nx = 4;            // Number of pads along X
   Double_t Xm = (1-(Nx*W))/1; // X Margin
   Double_t dw = (W*0.043)/4;
   dw = 0;

   double pt[10]={ 0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.35, 4.38, 5.41 };

   /*
   double pt0[7] = {0.367850122006, 0.614553050236, 0.863917028825, 1.20556341166, 1.70588069195, 2.20702672323, 2.70906027866};
   double pt1[7] = {0.367789076797, 0.614440212591, 0.863774382049, 1.20497396307, 1.70537038651, 2.20670012485, 2.70894866411};
   double pt2[7] = {0.367796914371, 0.614432668315, 0.863750637999, 1.20483678996, 1.70523328057, 2.20660485754, 2.70894763508};
   double pt3[7] = {0.367851030135, 0.614436256806, 0.863711196986, 1.20453238944, 1.70490005831, 2.20634436218, 2.70883718808};
   double pt4[7] = {0.367918726804, 0.614478139367, 0.86371364551, 1.20440209632, 1.70471744755, 2.20620023648, 2.70873611329};
   double pt5[7] = {0.367995332409, 0.614539798206, 0.863728027417, 1.20433041005, 1.70455951288, 2.20603668523, 2.70869305523};
   double pt6[7] = {0.368082051659, 0.614610551417, 0.863757500473, 1.20425897304, 1.70442544288, 2.20586778518, 2.70862088234};
   double pt7[7] = {0.368157341209, 0.614676983232, 0.863784163449, 1.20420269284, 1.70427371105, 2.20566848697, 2.70839587821};

   double pt0[7] = {0.367850122006, 0.614553050236, 0.863917028825, 1.20556341166, 1.70588069195, 2.20702672323, 2.70906027866};
   double pt1[7] = {0.367789076797, 0.614440212591, 0.863774382049, 1.20497396307, 1.70537038651, 2.20670012485, 2.70894866411};
   double pt2[7] = {0.367796854217, 0.614432598536, 0.863750726563, 1.20483779977, 1.70523471249, 2.20660520464, 2.70894485981};
   double pt3[7] = {0.367851030135, 0.614436256806, 0.863711196986, 1.20453238944, 1.70490005831, 2.20634436218, 2.70883718808};
   double pt4[7] = {0.367918726804, 0.614478139367, 0.86371364551, 1.20440209632, 1.70471744755, 2.20620023648, 2.70873611329};
   double pt5[7] = {0.367995332409, 0.614539798206, 0.863728027417, 1.20433041005, 1.70455951288, 2.20603668523, 2.70869305523};
   double pt6[7] = {0.368082051659, 0.614610551417, 0.863757500473, 1.20425897304, 1.70442544288, 2.20586778518, 2.70862088234};
   double pt7[7] = {0.368157436648, 0.61467696524, 0.863784191443, 1.20420282507, 1.70427416416, 2.20566867545, 2.70839664995};
   */
   double pt0[7] = {0.367850469081, 0.614553223131, 0.863916876481, 1.20556266027, 1.70588341108, 2.2070326342, 2.70906628283};
   double pt1[7] = {0.36778876233, 0.614440626208, 0.86377433619, 1.20497205152, 1.70537019611, 2.20669931557, 2.70896090366};
   double pt2[7] = {0.367797681591, 0.614432491628, 0.863751747422, 1.2048404578, 1.70523710347, 2.20660745733, 2.70892877887};
   double pt3[7] = {0.367850530889, 0.614437765067, 0.863710638394, 1.20453141462, 1.70490080841, 2.20634349043, 2.70883047486};
   double pt4[7] = {0.367919840262, 0.614479264624, 0.863714305316, 1.20440169145, 1.70471910518, 2.20619392959, 2.70874416248};
   double pt5[7] = {0.367996246187, 0.614540616687, 0.863728509603, 1.20432995835, 1.70456340068, 2.20603889451, 2.70870029727};
   double pt6[7] = {0.36808157778, 0.614610360264, 0.86375529631, 1.20426184235, 1.70442856538, 2.20587781628, 2.70858511802};
   double pt7[7] = {0.368158639538, 0.614675145499, 0.863781855872, 1.20419791181, 1.7042597357, 2.20568334316, 2.7083552446};

   //////////////////////////////////////////////////

   map<string, double*> INPUT;
   Document document;

   //////////////////////////////
   // NO_Z_CUT_WITH_EFF

   string ext1="n2";
   string ext2="n3";

   // UCC
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n2/00_02.json")).c_str());
   INPUT["mode1_UCC"+ext1]=ReadData(document, "mode1");
   INPUT["mode1_UCC_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["mode2_UCC"+ext1]=ReadData(document, "mode2");
   INPUT["mode2_UCC_error"+ext1]=ReadData(document, "mode2_error");

   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n3/00_02.json")).c_str());
   INPUT["mode1_UCC"+ext2]=ReadData(document, "mode1");
   INPUT["mode1_UCC_error"+ext2]=ReadData(document, "mode1_error");
   INPUT["mode2_UCC"+ext2]=ReadData(document, "mode2");
   INPUT["mode2_UCC_error"+ext2]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT/")+string(s)+string("/")+string(deta)+string("/n3/00_02.json")).c_str());
   INPUT["fit_UCC"+ext1]=ReadData(document, "mode1");
   INPUT["fit_UCC_error"+ext1]=ReadData(document, "mode1_error");

   // 0-5
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n2/00_05.json")).c_str());
   INPUT["mode1_00_05"+ext1]=ReadData(document, "mode1");
   INPUT["mode1_00_05_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["mode2_00_05"+ext1]=ReadData(document, "mode2");
   INPUT["mode2_00_05_error"+ext1]=ReadData(document, "mode2_error");

   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n3/00_05.json")).c_str());
   INPUT["mode1_00_05"+ext2]=ReadData(document, "mode1");
   INPUT["mode1_00_05_error"+ext2]=ReadData(document, "mode1_error");
   INPUT["mode2_00_05"+ext2]=ReadData(document, "mode2");
   INPUT["mode2_00_05_error"+ext2]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT/")+string(s)+string("/")+string(deta)+string("/n3/00_05.json")).c_str());
   INPUT["fit_00_05"+ext1]=ReadData(document, "mode1");
   INPUT["fit_00_05_error"+ext1]=ReadData(document, "mode1_error");
   ////////////////////////////////////

   // 0-10
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n2/00_10.json")).c_str());
   INPUT["mode1_00_10"+ext1]=ReadData(document, "mode1");
   INPUT["mode1_00_10_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["mode2_00_10"+ext1]=ReadData(document, "mode2");
   INPUT["mode2_00_10_error"+ext1]=ReadData(document, "mode2_error");

   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n3/00_10.json")).c_str());
   INPUT["mode1_00_10"+ext2]=ReadData(document, "mode1");
   INPUT["mode1_00_10_error"+ext2]=ReadData(document, "mode1_error");
   INPUT["mode2_00_10"+ext2]=ReadData(document, "mode2");
   INPUT["mode2_00_10_error"+ext2]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT/")+string(s)+string("/")+string(deta)+string("/n3/00_10.json")).c_str());
   INPUT["fit_00_10"+ext1]=ReadData(document, "mode1");
   INPUT["fit_00_10_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////////////

   // 10-20
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n2/10_20.json")).c_str());
   INPUT["mode1_10_20"+ext1]=ReadData(document, "mode1");
   INPUT["mode1_10_20_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["mode2_10_20"+ext1]=ReadData(document, "mode2");
   INPUT["mode2_10_20_error"+ext1]=ReadData(document, "mode2_error");

   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n3/10_20.json")).c_str());
   INPUT["mode1_10_20"+ext2]=ReadData(document, "mode1");
   INPUT["mode1_10_20_error"+ext2]=ReadData(document, "mode1_error");
   INPUT["mode2_10_20"+ext2]=ReadData(document, "mode2");
   INPUT["mode2_10_20_error"+ext2]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT/")+string(s)+string("/")+string(deta)+string("/n3/10_20.json")).c_str());
   INPUT["fit_10_20"+ext1]=ReadData(document, "mode1");
   INPUT["fit_10_20_error"+ext1]=ReadData(document, "mode1_error");

   ////////////////////////////////////////////

   // 20-30
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n2/20_30.json")).c_str());
   INPUT["mode1_20_30"+ext1]=ReadData(document, "mode1");
   INPUT["mode1_20_30_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["mode2_20_30"+ext1]=ReadData(document, "mode2");
   INPUT["mode2_20_30_error"+ext1]=ReadData(document, "mode2_error");

   // 20-30 Z CUT
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n3/20_30.json")).c_str());
   INPUT["mode1_20_30"+ext2]=ReadData(document, "mode1");
   INPUT["mode1_20_30_error"+ext2]=ReadData(document, "mode1_error");
   INPUT["mode2_20_30"+ext2]=ReadData(document, "mode2");
   INPUT["mode2_20_30_error"+ext2]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT/")+string(s)+string("/")+string(deta)+string("/n3/20_30.json")).c_str());
   INPUT["fit_20_30"+ext1]=ReadData(document, "mode1");
   INPUT["fit_20_30_error"+ext1]=ReadData(document, "mode1_error");

   ////////////////////////////////////////////

   // 30-40
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n2/30_40.json")).c_str());
   INPUT["mode1_30_40"+ext1]=ReadData(document, "mode1");
   INPUT["mode1_30_40_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["mode2_30_40"+ext1]=ReadData(document, "mode2");
   INPUT["mode2_30_40_error"+ext1]=ReadData(document, "mode2_error");

   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n3/30_40.json")).c_str());
   INPUT["mode1_30_40"+ext2]=ReadData(document, "mode1");
   INPUT["mode1_30_40_error"+ext2]=ReadData(document, "mode1_error");
   INPUT["mode2_30_40"+ext2]=ReadData(document, "mode2");
   INPUT["mode2_30_40_error"+ext2]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT/")+string(s)+string("/")+string(deta)+string("/n3/30_40.json")).c_str());
   INPUT["fit_30_40"+ext1]=ReadData(document, "mode1");
   INPUT["fit_30_40_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////////////////////////////

   // 40-50
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n2/40_50.json")).c_str());
   INPUT["mode1_40_50"+ext1]=ReadData(document, "mode1");
   INPUT["mode1_40_50_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["mode2_40_50"+ext1]=ReadData(document, "mode2");
   INPUT["mode2_40_50_error"+ext1]=ReadData(document, "mode2_error");

   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n3/40_50.json")).c_str());
   INPUT["mode1_40_50"+ext2]=ReadData(document, "mode1");
   INPUT["mode1_40_50_error"+ext2]=ReadData(document, "mode1_error");
   INPUT["mode2_40_50"+ext2]=ReadData(document, "mode2");
   INPUT["mode2_40_50_error"+ext2]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT/")+string(s)+string("/")+string(deta)+string("/n3/40_50.json")).c_str());
   INPUT["fit_40_50"+ext1]=ReadData(document, "mode1");
   INPUT["fit_40_50_error"+ext1]=ReadData(document, "mode1_error");

   ///////////////////////////////////////////////////////

   // 50-60
   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n2/50_60.json")).c_str());
   INPUT["mode1_50_60"+ext1]=ReadData(document, "mode1");
   INPUT["mode1_50_60_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["mode2_50_60"+ext1]=ReadData(document, "mode2");
   INPUT["mode2_50_60_error"+ext1]=ReadData(document, "mode2_error");

   document=READFILE((string("./DATA/")+string(s)+string("/")+string(deta)+string("/n3/50_60.json")).c_str());
   INPUT["mode1_50_60"+ext2]=ReadData(document, "mode1");
   INPUT["mode1_50_60_error"+ext2]=ReadData(document, "mode1_error");
   INPUT["mode2_50_60"+ext2]=ReadData(document, "mode2");
   INPUT["mode2_50_60_error"+ext2]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT/")+string(s)+string("/")+string(deta)+string("/n3/50_60.json")).c_str());
   INPUT["fit_50_60"+ext1]=ReadData(document, "mode1");
   INPUT["fit_50_60_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////
   ///////////////////////////////////////////////////
  
   MakeHisto("P1", 0, 0.512, Xm+W+dw, 1, 0.23, 0, 0.25, 0);  // PLOT=1  UCC
   DoLine();
   DoText("0-0.2%");
   //DoLatex(0.28, 0.61, "PbPb  #sqrt{s_{NN}} = 5.02 TeV");//position, text
   //DoLatex(0.28, 0.50, "#scale[1.1]{Hydjet}");//position, text
   DoLatex(0.225, 0.81, "#scale[1.1]{HYDJET++}");//position, text
   DoLegend();

   //PlotData( pt0, INPUT["mode1_UCC"+ext1], INPUT["mode1_UCC_error"+ext1], kBlue, 21, 1.1, "p" );
   //PlotData( pt0, INPUT["mode2_UCC"+ext1], INPUT["mode2_UCC_error"+ext1], kRed, 21, 1.1, "p" );

   PlotData( pt0, INPUT["mode1_UCC"+ext2], INPUT["mode1_UCC_error"+ext2], kBlue, 21, 1.1, "p" );
   PlotData( pt0, INPUT["mode2_UCC"+ext2], INPUT["mode2_UCC_error"+ext2], kRed, 21, 1.1, "p" );
   PlotData( pt0, INPUT["fit_UCC"+ext1], INPUT["fit_UCC_error"+ext1], kGreen, 34, 1.1, "p" );

   PlotData( x20_arr, y20_arr, y20_err, kOrange, 24, 1.1, "p" );

   cc1->cd();
   ////////////////////////////////////////////////////

   MakeHisto("P2", Xm+W+dw, 0.512, Xm+2*W+dw, 1, 0, 0, 0.25, 0, 1);  //  PLOT=2  0-5
   DoLine();
   DoText("0-5%");

   //PlotData( pt1, INPUT["mode1_00_05"+ext1], INPUT["mode1_00_05_error"+ext1], kBlue, 21, 1.1, "p" );
   //PlotData( pt1, INPUT["mode2_00_05"+ext1], INPUT["mode2_00_05_error"+ext1], kRed, 21, 1.1, "p" );

   PlotData( pt1, INPUT["mode1_00_05"+ext2], INPUT["mode1_00_05_error"+ext2], kBlue, 21, 1.1, "p" );
   PlotData( pt1, INPUT["mode2_00_05"+ext2], INPUT["mode2_00_05_error"+ext2], kRed, 21, 1.1, "p" );
   PlotData( pt1, INPUT["fit_00_05"+ext1], INPUT["fit_00_05_error"+ext1], kGreen, 34, 1.1, "p" );

   cc1->cd();

   MakeHisto("P3", Xm+2*W+dw, 0.512, Xm+3*W+dw, 1, 0, 0, 0.25, 0, 1);  //  PLOT=3   0-10
   DoLine();
   DoText("0-10%");

   //PlotData( pt2, INPUT["mode1_00_10"+ext1], INPUT["mode1_00_10_error"+ext1], kBlue, 21, 1.1, "p" );
   //PlotData( pt2, INPUT["mode2_00_10"+ext1], INPUT["mode2_00_10_error"+ext1], kRed, 21, 1.1, "p" );

   PlotData( pt2, INPUT["mode1_00_10"+ext2], INPUT["mode1_00_10_error"+ext2], kBlue, 21, 1.1, "p" );
   PlotData( pt2, INPUT["mode2_00_10"+ext2], INPUT["mode2_00_10_error"+ext2], kRed, 21, 1.1, "p" );
   PlotData( pt2, INPUT["fit_00_10"+ext1], INPUT["fit_00_10_error"+ext1], kGreen, 34, 1.1, "p" );

   cc1->cd();

   MakeHisto("P4", Xm+3*W+dw, 0.512, Xm+4*W-dw, 1, 0, 0.01, 0.25, 0, 1);  //  PLOT=4  10-20
   DoLine();
   DoText("10-20%");
   DoLatex(0.34, 0.81, "#scale[1.3]{PbPb  #sqrt{s_{NN}} = 5.02 TeV}");//position, text

   //PlotData( pt3, INPUT["mode1_10_20"+ext1], INPUT["mode1_10_20_error"+ext1], kBlue, 21, 1.1, "p" );
   //PlotData( pt3, INPUT["mode2_10_20"+ext1], INPUT["mode2_10_20_error"+ext1], kRed, 21, 1.1, "p" );

   PlotData( pt3, INPUT["mode1_10_20"+ext2], INPUT["mode1_10_20_error"+ext2], kBlue, 21, 1.1, "p" );
   PlotData( pt3, INPUT["mode2_10_20"+ext2], INPUT["mode2_10_20_error"+ext2], kRed, 21, 1.1, "p" );
   PlotData( pt3, INPUT["fit_10_20"+ext1], INPUT["fit_10_20_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( x31_arr, y31_arr, y31_err, kBlack, 24, 1.1, "p" );

   cc1->cd();

   MakeHisto("P5", 0, 0.02, Xm+W+dw, 0.512, 0.23, 0, 0, 0.25);  //  PLOT=5
   DoLine();
   DoText("20-30%");

   //PlotData( pt4, INPUT["mode1_20_30"+ext1], INPUT["mode1_20_30_error"+ext1], kBlue, 21, 1.1, "p" );
   //PlotData( pt4, INPUT["mode2_20_30"+ext1], INPUT["mode2_20_30_error"+ext1], kRed, 21, 1.1, "p" );

   PlotData( pt4, INPUT["mode1_20_30"+ext2], INPUT["mode1_20_30_error"+ext2], kBlue, 21, 1.1, "p" );
   PlotData( pt4, INPUT["mode2_20_30"+ext2], INPUT["mode2_20_30_error"+ext2], kRed, 21, 1.1, "p" );
   PlotData( pt4, INPUT["fit_20_30"+ext1], INPUT["fit_20_30_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( x32_arr, y32_arr, y32_err, kBlack, 24, 1.1, "p" );

   cc1->cd();

   MakeHisto("P6", Xm+W+dw, 0.02, Xm+2*W+dw, 0.512, 0, 0, 0, 0.25, 1);  //  PLOT=6
   DoLine();
   DoText("30-40%");

   //PlotData( pt5, INPUT["mode1_30_40"+ext1], INPUT["mode1_30_40_error"+ext1], kBlue, 21, 1.1, "p" );
   //PlotData( pt5, INPUT["mode2_30_40"+ext1], INPUT["mode2_30_40_error"+ext1], kRed, 21, 1.1, "p" );

   PlotData( pt5, INPUT["mode1_30_40"+ext2], INPUT["mode1_30_40_error"+ext2], kBlue, 21, 1.1, "p" );
   PlotData( pt5, INPUT["mode2_30_40"+ext2], INPUT["mode2_30_40_error"+ext2], kRed, 21, 1.1, "p" );
   PlotData( pt5, INPUT["fit_30_40"+ext1], INPUT["fit_30_40_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( x33_arr, y33_arr, y33_err, kBlack, 24, 1.1, "p" );

   cc1->cd();

   MakeHisto("P7", Xm+2*W+dw, 0.02, Xm+3*W+dw, 0.512, 0, 0, 0, 0.25, 1);  //  PLOT=7
   DoLine();
   DoText("40-50%");

   //PlotData( pt6, INPUT["mode1_40_50"+ext1], INPUT["mode1_40_50_error"+ext1], kBlue, 21, 1.1, "p" );
   //PlotData( pt6, INPUT["mode2_40_50"+ext1], INPUT["mode2_40_50_error"+ext1], kRed, 21, 1.1, "p" );

   PlotData( pt6, INPUT["mode1_40_50"+ext2], INPUT["mode1_40_50_error"+ext2], kBlue, 21, 1.1, "p" );
   PlotData( pt6, INPUT["mode2_40_50"+ext2], INPUT["mode2_40_50_error"+ext2], kRed, 21, 1.1, "p" );
   PlotData( pt6, INPUT["fit_40_50"+ext1], INPUT["fit_40_50_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( x34_arr, y34_arr, y34_err, kBlack, 24, 1.1, "p" );

   cc1->cd();

   MakeHisto("P8", Xm+3*W+dw, 0.02, Xm+4*W-dw, 0.512, 0, 0.01, 0, 0.25, 1);  //  PLOT=8
   DoLine();
   DoText("50-60%");

   //PlotData( pt7, INPUT["mode1_50_60"+ext1], INPUT["mode1_50_60_error"+ext1], kBlue, 21, 1.1, "p" );
   //PlotData( pt7, INPUT["mode2_50_60"+ext1], INPUT["mode2_50_60_error"+ext1], kRed, 21, 1.1, "p" );

   PlotData( pt7, INPUT["mode1_50_60"+ext2], INPUT["mode1_50_60_error"+ext2], kBlue, 21, 1.1, "p" );
   PlotData( pt7, INPUT["mode2_50_60"+ext2], INPUT["mode2_50_60_error"+ext2], kRed, 21, 1.1, "p" );
   PlotData( pt7, INPUT["fit_50_60"+ext1], INPUT["fit_50_60_error"+ext1], kGreen, 34, 1.1, "p" );

   cc1->cd();

   ////////////////////////////////////////////////
   //
   //cc1->Print("~/www/09-05-2016/hydjet/4/2/cc1_1.png");
   //cc1->Print("~/www/10-05-2016/hydjet/4/2/cc1_1.png");
   //cc1->Print((string("~/www/14-05-2016/hydjet/4/")+string(s)+string("/")+string(deta)+string("/cc1_1.png")).c_str());
   std::ifstream t1("INPUT.txt");
   std::string str1((std::istreambuf_iterator<char>(t1)),
                    std::istreambuf_iterator<char>());
   std::ifstream t(str1.substr(0, str1.size()-1)+string("OPATH.txt").c_str());
   std::string str((std::istreambuf_iterator<char>(t)),
                    std::istreambuf_iterator<char>());
   cc1->Print((str.substr(0, str.size()-1)+string("4/")+string(s)+string("/")+string(deta)+string("/cc1_3.png")).c_str());
   cc1->Print((str.substr(0, str.size()-1)+string("4/")+string(s)+string("/")+string(deta)+string("/cc1_3.pdf")).c_str());
}
