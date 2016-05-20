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

double maximum = 0.42;
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
        //cout << array[count] << endl;

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
      hist->GetYaxis()->SetTitle("v^{(#alpha)}_{2}");
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
   TLegend *leg = new TLegend(0.3, 0.18, 0.9, 0.58, NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextSize(0.06);
   leg->SetLineColor(1);
   leg->SetLineStyle(2);
   leg->SetLineWidth(1);
 
   TLegendEntry *entry;

   entry=leg->AddEntry("", "UCC paper","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kOrange);
   entry->SetMarkerStyle(24);
   entry->SetMarkerSize(1.2);

   //entry=leg->AddEntry("", "v_{2}{|#Delta#eta|>0.8}, ALICE PLB 708 (2012) 249","p");
   entry=leg->AddEntry("", "v_{2}{|#Delta#eta|>0.8} ALICE","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kBlack);
   entry->SetMarkerStyle(24);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=1 f+j","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kBlue);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=1 flow","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kBlue);
   entry->SetMarkerStyle(25);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=2 f+j","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kRed);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=2 flow","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kRed);
   entry->SetMarkerStyle(25);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "fit f+j","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kGreen);
   entry->SetMarkerStyle(34);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "fit flow","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kCyan);
   entry->SetMarkerStyle(34);
   entry->SetMarkerSize(1.2);

   /*
   entry=leg->AddEntry("", "#alpha=1 n=3","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kRed);
   entry->SetMarkerStyle(25);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=2 n=3","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kBlack);
   entry->SetMarkerStyle(25);
   entry->SetMarkerSize(1.2);
   */
 

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


void EFF_VS_NO_EFF_2(const char *s1, const char *deta1, const char *s2, const char *deta2){

   //////////////////////////////////////////////////////////////////////////////////////////////////////////
   // 10-20 20-30 30-40 40-50

   int Nbd = 12;

   // UCC paper
   double x20_arr[] = {0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.36, 4.38, 5.41, 6.75, 9.87};
   double y20_arr[] = {0.0112, 0.0163, 0.0216, 0.0309, 0.0344, 0.0369, 0.0379};
   double y20_err[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

   // ALICE
   double x21_arr[] = {0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.36, 4.38, 5.41, 6.75, 9.87};
   double y21_arr[] = {0.0385, 0.0609, 0.0798, 0.101, 0.129, 0.152, 0.169, 0.174, 0.157, 0.127, 0.0962, 0.0751};
   double y21_err[] = {0.0001, 0.0003, 0.0005, 0.001, 0.001, 0.001, 0.002, 0.002, 0.003, 0.003, 0.004, 0.0061};

   double x22_arr[] = {0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.36, 4.39, 5.41, 6.75, 9.85};
   double y22_arr[] = {0.05, 0.0793, 0.104, 0.133, 0.168, 0.196, 0.214, 0.216, 0.189, 0.157, 0.125, 0.108};
   double y22_err[] = {0, 0.0004, 0.001, 0.001, 0.001, 0.002, 0.002, 0.002, 0.003, 0.003, 0.004, 0.007};

   double x23_arr[] = {0.411, 0.615, 0.865, 1.21, 1.71, 2.21, 2.71, 3.37, 4.39, 5.41, 6.75, 9.82};
   double y23_arr[] = {0.0572, 0.0912, 0.12, 0.153, 0.192, 0.221, 0.236, 0.235, 0.203, 0.173, 0.136, 0.111};
   double y23_err[] = {0.0002, 0.0004, 0.001, 0.001, 0.002, 0.002, 0.002, 0.002, 0.003, 0.004, 0.005, 0.007};

   double x24_arr[] = {0.41, 0.614, 0.864, 1.21, 1.71, 2.21, 2.71, 3.37, 4.39, 5.42, 6.75, 9.81};
   double y24_arr[] = {0.0606, 0.0974, 0.129, 0.163, 0.203, 0.229, 0.239, 0.234, 0.201, 0.174, 0.146, 0.12};
   double y24_err[] = {0.0002, 0.0006, 0.001, 0.001, 0.002, 0.002, 0.002, 0.002, 0.003, 0.006, 0.007, 0.01};

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
   double pt0[7] = {0.367191474465, 0.613625419578, 0.862896294128, 1.20156652253, 1.70206097761, 2.2035459948, 2.70599556838};
   double pt1[7] = {0.367155675615, 0.613565145985, 0.862818402482, 1.20125138857, 1.70180238872, 2.20340675207, 2.70603638857};
   double pt2[7] = {0.367112583908, 0.61349220935, 0.862723435025, 1.20086247702, 1.70147777574, 2.20322980022, 2.70608846797};
   double pt3[7] = {0.367136610758, 0.613480777639, 0.862674809429, 1.20056646338, 1.7011827101, 2.20305780065, 2.70618363669};
   double pt4[7] = {0.367167631241, 0.613505186632, 0.862678825719, 1.20051095936, 1.70110535462, 2.20301842592, 2.70624377457};
   double pt5[7] = {0.367239816737, 0.613561726985, 0.862688107441, 1.20038249873, 1.7009252699, 2.20292628343, 2.70638450228};
   double pt6[7] = {0.367301692148, 0.613615008975, 0.862709783296, 1.2003353008, 1.70083191171, 2.20286207922, 2.70637117753};
   double pt7[7] = {0.367359074961, 0.613673772886, 0.862724078386, 1.20024732957, 1.70069503476, 2.20265579258, 2.70615299918};
   
   double pt0[7] = {0.367191474465, 0.613625419578, 0.862896294128, 1.20156652253, 1.70206097761, 2.2035459948, 2.70599556838};
   double pt1[7] = {0.367113156529, 0.613503977264, 0.862748782292, 1.20098728851, 1.70158941421, 2.20328643642, 2.70606402668};
   double pt2[7] = {0.367112583908, 0.61349220935, 0.862723435025, 1.20086247702, 1.70147777574, 2.20322980022, 2.70608846797};
   double pt3[7] = {0.367136610758, 0.613480777639, 0.862674809429, 1.20056646338, 1.7011827101, 2.20305780065, 2.70618363669};
   double pt4[7] = {0.367182527684, 0.613514096481, 0.862673246448, 1.20044978994, 1.70104768964, 2.20298794576, 2.70630795493};
   double pt5[7] = {0.367239816737, 0.613561726985, 0.862688107441, 1.20038249873, 1.7009252699, 2.20292628343, 2.70638450228};
   double pt6[7] = {0.367301692148, 0.613615008975, 0.862709783296, 1.2003353008, 1.70083191171, 2.20286207922, 2.70637117753};
   double pt7[7] = {0.367359074961, 0.613673772886, 0.862724078386, 1.20024732957, 1.70069503476, 2.20265579258, 2.70615299918};

   double pt0[7] = {0.367191474465, 0.613625419578, 0.862896294128, 1.20156652253, 1.70206097761, 2.2035459948, 2.70599556838};
   double pt1[7] = {0.367113156529, 0.613503977264, 0.862748782292, 1.20098728851, 1.70158941421, 2.20328643642, 2.70606402668};
   double pt2[7] = {0.367112583908, 0.61349220935, 0.862723435025, 1.20086247702, 1.70147777574, 2.20322980022, 2.70608846797};
   double pt3[7] = {0.367136610758, 0.613480777639, 0.862674809429, 1.20056646338, 1.7011827101, 2.20305780065, 2.70618363669};
   double pt4[7] = {0.367182527684, 0.613514096481, 0.862673246448, 1.20044978994, 1.70104768964, 2.20298794576, 2.70630795493};
   double pt5[7] = {0.367239816737, 0.613561726985, 0.862688107441, 1.20038249873, 1.7009252699, 2.20292628343, 2.70638450228};
   double pt6[7] = {0.367301692148, 0.613615008975, 0.862709783296, 1.2003353008, 1.70083191171, 2.20286207922, 2.70637117753};
   double pt7[7] = {0.367359074961, 0.613673772886, 0.862724078386, 1.20024732957, 1.70069503476, 2.20265579258, 2.70615299918};
   */
   
   #include "pt_values.h"

   //////////////////////////////////////////////////

   map<string, double*> INPUT;
   Document document;

   //////////////////////////////
   // NO_Z_CUT_WITH_EFF

   string ext1="n2";
   string ext2="n3";

   // UCC
   document=READFILE((string("./DATA_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/00_02.json")).c_str());
   INPUT["flowjets_mode1_UCC"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_mode1_UCC_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flowjets_mode2_UCC"+ext1]=ReadData(document, "mode2");
   INPUT["flowjets_mode2_UCC_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/00_02.json")).c_str());
   INPUT["flowjets_fit_UCC"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_fit_UCC_error"+ext1]=ReadData(document, "mode1_error");

   // 0-5
   document=READFILE((string("./DATA_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/00_05.json")).c_str());
   INPUT["flowjets_mode1_00_05"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_mode1_00_05_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flowjets_mode2_00_05"+ext1]=ReadData(document, "mode2");
   INPUT["flowjets_mode2_00_05_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/00_05.json")).c_str());
   INPUT["flowjets_fit_00_05"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_fit_00_05_error"+ext1]=ReadData(document, "mode1_error");

   ////////////////////////////////////

   // 0-10
   document=READFILE((string("./DATA_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/00_10.json")).c_str());
   INPUT["flowjets_mode1_00_10"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_mode1_00_10_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flowjets_mode2_00_10"+ext1]=ReadData(document, "mode2");
   INPUT["flowjets_mode2_00_10_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/00_10.json")).c_str());
   INPUT["flowjets_fit_00_10"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_fit_00_10_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////////////

   // 10-20
   document=READFILE((string("./DATA_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/10_20.json")).c_str());
   INPUT["flowjets_mode1_10_20"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_mode1_10_20_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flowjets_mode2_10_20"+ext1]=ReadData(document, "mode2");
   INPUT["flowjets_mode2_10_20_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/10_20.json")).c_str());
   INPUT["flowjets_fit_10_20"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_fit_10_20_error"+ext1]=ReadData(document, "mode1_error");

   ////////////////////////////////////////////

   // 20-30
   document=READFILE((string("./DATA_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/20_30.json")).c_str());
   INPUT["flowjets_mode1_20_30"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_mode1_20_30_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flowjets_mode2_20_30"+ext1]=ReadData(document, "mode2");
   INPUT["flowjets_mode2_20_30_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/20_30.json")).c_str());
   INPUT["flowjets_fit_20_30"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_fit_20_30_error"+ext1]=ReadData(document, "mode1_error");

   ////////////////////////////////////////////

   // 30-40
   document=READFILE((string("./DATA_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/30_40.json")).c_str());
   INPUT["flowjets_mode1_30_40"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_mode1_30_40_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flowjets_mode2_30_40"+ext1]=ReadData(document, "mode2");
   INPUT["flowjets_mode2_30_40_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/30_40.json")).c_str());
   INPUT["flowjets_fit_30_40"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_fit_30_40_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////////////////////////////

   // 40-50
   document=READFILE((string("./DATA_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/40_50.json")).c_str());
   INPUT["flowjets_mode1_40_50"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_mode1_40_50_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flowjets_mode2_40_50"+ext1]=ReadData(document, "mode2");
   INPUT["flowjets_mode2_40_50_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/40_50.json")).c_str());
   INPUT["flowjets_fit_40_50"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_fit_40_50_error"+ext1]=ReadData(document, "mode1_error");

   ///////////////////////////////////////////////////////

   // 50-60
   document=READFILE((string("./DATA_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/50_60.json")).c_str());
   INPUT["flowjets_mode1_50_60"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_mode1_50_60_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flowjets_mode2_50_60"+ext1]=ReadData(document, "mode2");
   INPUT["flowjets_mode2_50_60_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flowjets/")+string(s1)+string("/")+string(deta1)+string("/n2/50_60.json")).c_str());
   INPUT["flowjets_fit_50_60"+ext1]=ReadData(document, "mode1");
   INPUT["flowjets_fit_50_60_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////
   ///////////////////////////////////////////////////

   // UCC
   document=READFILE((string("./DATA_flow/")+string(s1)+string("_np/")+string(deta1)+string("/n2/00_02.json")).c_str());
   INPUT["flow_mode1_UCC"+ext1]=ReadData(document, "mode1");
   INPUT["flow_mode1_UCC_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flow_mode2_UCC"+ext1]=ReadData(document, "mode2");
   INPUT["flow_mode2_UCC_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flow/")+string(s1)+string("/")+string(deta1)+string("/n2/00_02.json")).c_str());
   INPUT["flow_fit_UCC"+ext1]=ReadData(document, "mode1");
   INPUT["flow_fit_UCC_error"+ext1]=ReadData(document, "mode1_error");

   // 0-5
   document=READFILE((string("./DATA_flow/")+string(s1)+string("_np/")+string(deta1)+string("/n2/00_05.json")).c_str());
   INPUT["flow_mode1_00_05"+ext1]=ReadData(document, "mode1");
   INPUT["flow_mode1_00_05_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flow_mode2_00_05"+ext1]=ReadData(document, "mode2");
   INPUT["flow_mode2_00_05_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flow/")+string(s1)+string("/")+string(deta1)+string("/n2/00_05.json")).c_str());
   INPUT["flow_fit_00_05"+ext1]=ReadData(document, "mode1");
   INPUT["flow_fit_00_05_error"+ext1]=ReadData(document, "mode1_error");

   ////////////////////////////////////

   // 0-10
   document=READFILE((string("./DATA_flow/")+string(s1)+string("_np/")+string(deta1)+string("/n2/00_10.json")).c_str());
   INPUT["flow_mode1_00_10"+ext1]=ReadData(document, "mode1");
   INPUT["flow_mode1_00_10_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flow_mode2_00_10"+ext1]=ReadData(document, "mode2");
   INPUT["flow_mode2_00_10_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flow/")+string(s1)+string("/")+string(deta1)+string("/n2/00_10.json")).c_str());
   INPUT["flow_fit_00_10"+ext1]=ReadData(document, "mode1");
   INPUT["flow_fit_00_10_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////////////

   // 10-20
   document=READFILE((string("./DATA_flow/")+string(s1)+string("_np/")+string(deta1)+string("/n2/10_20.json")).c_str());
   INPUT["flow_mode1_10_20"+ext1]=ReadData(document, "mode1");
   INPUT["flow_mode1_10_20_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flow_mode2_10_20"+ext1]=ReadData(document, "mode2");
   INPUT["flow_mode2_10_20_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flow/")+string(s1)+string("/")+string(deta1)+string("/n2/10_20.json")).c_str());
   INPUT["flow_fit_10_20"+ext1]=ReadData(document, "mode1");
   INPUT["flow_fit_10_20_error"+ext1]=ReadData(document, "mode1_error");

   ////////////////////////////////////////////

   // 20-30
   document=READFILE((string("./DATA_flow/")+string(s1)+string("_np/")+string(deta1)+string("/n2/20_30.json")).c_str());
   INPUT["flow_mode1_20_30"+ext1]=ReadData(document, "mode1");
   INPUT["flow_mode1_20_30_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flow_mode2_20_30"+ext1]=ReadData(document, "mode2");
   INPUT["flow_mode2_20_30_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flow/")+string(s1)+string("/")+string(deta1)+string("/n2/20_30.json")).c_str());
   INPUT["flow_fit_20_30"+ext1]=ReadData(document, "mode1");
   INPUT["flow_fit_20_30_error"+ext1]=ReadData(document, "mode1_error");

   ////////////////////////////////////////////

   // 30-40
   document=READFILE((string("./DATA_flow/")+string(s1)+string("_np/")+string(deta1)+string("/n2/30_40.json")).c_str());
   INPUT["flow_mode1_30_40"+ext1]=ReadData(document, "mode1");
   INPUT["flow_mode1_30_40_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flow_mode2_30_40"+ext1]=ReadData(document, "mode2");
   INPUT["flow_mode2_30_40_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flow/")+string(s1)+string("/")+string(deta1)+string("/n2/30_40.json")).c_str());
   INPUT["flow_fit_30_40"+ext1]=ReadData(document, "mode1");
   INPUT["flow_fit_30_40_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////////////////////////////
   // 40-50
   document=READFILE((string("./DATA_flow/")+string(s1)+string("_np/")+string(deta1)+string("/n2/40_50.json")).c_str());
   INPUT["flow_mode1_40_50"+ext1]=ReadData(document, "mode1");
   INPUT["flow_mode1_40_50_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flow_mode2_40_50"+ext1]=ReadData(document, "mode2");
   INPUT["flow_mode2_40_50_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flow/")+string(s1)+string("/")+string(deta1)+string("/n2/40_50.json")).c_str());
   INPUT["flow_fit_40_50"+ext1]=ReadData(document, "mode1");
   INPUT["flow_fit_40_50_error"+ext1]=ReadData(document, "mode1_error");

   ///////////////////////////////////////////////////////

   // 50-60
   document=READFILE((string("./DATA_flow/")+string(s1)+string("_np/")+string(deta1)+string("/n2/50_60.json")).c_str());
   INPUT["flow_mode1_50_60"+ext1]=ReadData(document, "mode1");
   INPUT["flow_mode1_50_60_error"+ext1]=ReadData(document, "mode1_error");
   INPUT["flow_mode2_50_60"+ext1]=ReadData(document, "mode2");
   INPUT["flow_mode2_50_60_error"+ext1]=ReadData(document, "mode2_error");
   document=READFILE((string("./FIT_flow/")+string(s1)+string("/")+string(deta1)+string("/n2/50_60.json")).c_str());
   INPUT["flow_fit_50_60"+ext1]=ReadData(document, "mode1");
   INPUT["flow_fit_50_60_error"+ext1]=ReadData(document, "mode1_error");

   /////////////////////////////
   ///////////////////////////////////////////////////

   MakeHisto("P1", 0, 0.512, Xm+W+dw, 1, 0.23, 0, 0.25, 0);  // PLOT=1  UCC
   DoLine();
   DoText("0-0.2%");
   //DoLatex(0.28, 0.61, "#scale[1.1]{HYDJET++}");//position, text
   //DoLatex(0.28, 0.50, "PbPb  #sqrt{s_{NN}} = 2.76 TeV");//position, text
   DoLatex(0.225, 0.81, "#scale[1.1]{HYDJET++}");//position, text
   DoLegend();

   PlotData( pt0, INPUT["flowjets_mode1_UCC"+ext1], INPUT["flowjets_mode1_UCC_error"+ext1], kBlue, 21, 1.1, "p" );
   PlotData( pt0, INPUT["flowjets_mode2_UCC"+ext1], INPUT["flowjets_mode2_UCC_error"+ext1], kRed, 21, 1.1, "p" );
   PlotData( pt0, INPUT["flowjets_fit_UCC"+ext1], INPUT["flowjets_fit_UCC_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( pt0, INPUT["flow_mode1_UCC"+ext1], INPUT["flow_mode1_UCC_error"+ext1], kBlue, 25, 1.1, "p" );
   PlotData( pt0, INPUT["flow_mode2_UCC"+ext1], INPUT["flow_mode2_UCC_error"+ext1], kRed, 25, 1.1, "p" );
   PlotData( pt0, INPUT["flow_fit_UCC"+ext1], INPUT["flow_fit_UCC_error"+ext1], kCyan, 34, 1.1, "p" );

   //PlotData( pt0, INPUT["flowjets_mode1_UCC"+ext2], INPUT["flowjets_mode1_UCC_error"+ext2], kRed, 25, 1.1, "p" );
   //PlotData( pt0, INPUT["flowjets_mode2_UCC"+ext2], INPUT["flowjets_mode2_UCC_error"+ext2], kBlack, 25, 1.1, "p" );

   PlotData( x20_arr, y20_arr, y20_err, kOrange, 24, 1.1, "p" );

   cc1->cd();
   ////////////////////////////////////////////////////

   MakeHisto("P2", Xm+W+dw, 0.512, Xm+2*W+dw, 1, 0, 0, 0.25, 0, 1);  //  PLOT=2  0-5
   DoLine();
   DoText("0-5%");

   PlotData( pt1, INPUT["flowjets_mode1_00_05"+ext1], INPUT["flowjets_mode1_00_05_error"+ext1], kBlue, 21, 1.1, "p" );
   PlotData( pt1, INPUT["flowjets_mode2_00_05"+ext1], INPUT["flowjets_mode2_00_05_error"+ext1], kRed, 21, 1.1, "p" );
   PlotData( pt1, INPUT["flowjets_fit_00_05"+ext1], INPUT["flowjets_fit_00_05_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( pt1, INPUT["flow_mode1_00_05"+ext1], INPUT["flow_mode1_00_05_error"+ext1], kBlue, 25, 1.1, "p" );
   PlotData( pt1, INPUT["flow_mode2_00_05"+ext1], INPUT["flow_mode2_00_05_error"+ext1], kRed, 25, 1.1, "p" );
   PlotData( pt1, INPUT["flow_fit_00_05"+ext1], INPUT["flow_fit_00_05_error"+ext1], kCyan, 34, 1.1, "p" );

   //PlotData( pt1, INPUT["flowjets_mode1_00_05"+ext2], INPUT["flowjets_mode1_00_05_error"+ext2], kRed, 25, 1.1, "p" );
   //PlotData( pt1, INPUT["flowjets_mode2_00_05"+ext2], INPUT["flowjets_mode2_00_05_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   MakeHisto("P3", Xm+2*W+dw, 0.512, Xm+3*W+dw, 1, 0, 0, 0.25, 0, 1);  //  PLOT=3   0-10
   DoLine();
   DoText("0-10%");

   PlotData( pt2, INPUT["flowjets_mode1_00_10"+ext1], INPUT["flowjets_mode1_00_10_error"+ext1], kBlue, 21, 1.1, "p" );
   PlotData( pt2, INPUT["flowjets_mode2_00_10"+ext1], INPUT["flowjets_mode2_00_10_error"+ext1], kRed, 21, 1.1, "p" );
   PlotData( pt2, INPUT["flowjets_fit_00_10"+ext1], INPUT["flowjets_fit_00_10_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( pt2, INPUT["flow_mode1_00_10"+ext1], INPUT["flow_mode1_00_10_error"+ext1], kBlue, 25, 1.1, "p" );
   PlotData( pt2, INPUT["flow_mode2_00_10"+ext1], INPUT["flow_mode2_00_10_error"+ext1], kRed, 25, 1.1, "p" );
   PlotData( pt2, INPUT["flow_fit_00_10"+ext1], INPUT["flow_fit_00_10_error"+ext1], kCyan, 34, 1.1, "p" );

   //PlotData( pt2, INPUT["flowjets_mode1_00_10"+ext2], INPUT["flowjets_mode1_00_10_error"+ext2], kRed, 25, 1.1, "p" );
   //PlotData( pt2, INPUT["flowjets_mode2_00_10"+ext2], INPUT["flowjets_mode2_00_10_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   MakeHisto("P4", Xm+3*W+dw, 0.512, Xm+4*W-dw, 1, 0, 0.01, 0.25, 0, 1);  //  PLOT=4  10-20
   DoLine();
   DoText("10-20%");

   PlotData( pt3, INPUT["flowjets_mode1_10_20"+ext1], INPUT["flowjets_mode1_10_20_error"+ext1], kBlue, 21, 1.1, "p" );
   PlotData( pt3, INPUT["flowjets_mode2_10_20"+ext1], INPUT["flowjets_mode2_10_20_error"+ext1], kRed, 21, 1.1, "p" );
   PlotData( pt3, INPUT["flowjets_fit_10_20"+ext1], INPUT["flowjets_fit_10_20_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( pt3, INPUT["flow_mode1_10_20"+ext1], INPUT["flow_mode1_10_20_error"+ext1], kBlue, 25, 1.1, "p" );
   PlotData( pt3, INPUT["flow_mode2_10_20"+ext1], INPUT["flow_mode2_10_20_error"+ext1], kRed, 25, 1.1, "p" );
   PlotData( pt3, INPUT["flow_fit_10_20"+ext1], INPUT["flow_fit_10_20_error"+ext1], kCyan, 34, 1.1, "p" );
   DoLatex(0.34, 0.81, "#scale[1.3]{PbPb  #sqrt{s_{NN}} = 2.76 TeV}");//position, text

   //PlotData( pt3, INPUT["flowjets_mode1_10_20"+ext2], INPUT["flowjets_mode1_10_20_error"+ext2], kRed, 25, 1.1, "p" );
   //PlotData( pt3, INPUT["flowjets_mode2_10_20"+ext2], INPUT["flowjets_mode2_10_20_error"+ext2], kBlack, 25, 1.1, "p" );
   
   PlotData( x21_arr, y21_arr, y21_err, kBlack, 24, 1.1, "p" );

   cc1->cd();

   MakeHisto("P5", 0, 0.02, Xm+W+dw, 0.512, 0.23, 0, 0, 0.25);  //  PLOT=5
   DoLine();
   DoText("20-30%");

   PlotData( pt4, INPUT["flowjets_mode1_20_30"+ext1], INPUT["flowjets_mode1_20_30_error"+ext1], kBlue, 21, 1.1, "p" );
   PlotData( pt4, INPUT["flowjets_mode2_20_30"+ext1], INPUT["flowjets_mode2_20_30_error"+ext1], kRed, 21, 1.1, "p" );
   PlotData( pt4, INPUT["flowjets_fit_20_30"+ext1], INPUT["flowjets_fit_20_30_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( pt4, INPUT["flow_mode1_20_30"+ext1], INPUT["flow_mode1_20_30_error"+ext1], kBlue, 25, 1.1, "p" );
   PlotData( pt4, INPUT["flow_mode2_20_30"+ext1], INPUT["flow_mode2_20_30_error"+ext1], kRed, 25, 1.1, "p" );
   PlotData( pt4, INPUT["flow_fit_20_30"+ext1], INPUT["flow_fit_20_30_error"+ext1], kCyan, 34, 1.1, "p" );

   //PlotData( pt4, INPUT["flowjets_mode1_20_30"+ext2], INPUT["flowjets_mode1_20_30_error"+ext2], kRed, 25, 1.1, "p" );
   //PlotData( pt4, INPUT["flowjets_mode2_20_30"+ext2], INPUT["flowjets_mode2_20_30_error"+ext2], kBlack, 25, 1.1, "p" );
   
   PlotData( x22_arr, y22_arr, y22_err, kBlack, 24, 1.1, "p" );

   cc1->cd();

   MakeHisto("P6", Xm+W+dw, 0.02, Xm+2*W+dw, 0.512, 0, 0, 0, 0.25, 1);  //  PLOT=6
   DoLine();
   DoText("30-40%");

   PlotData( pt5, INPUT["flowjets_mode1_30_40"+ext1], INPUT["flowjets_mode1_30_40_error"+ext1], kBlue, 21, 1.1, "p" );
   PlotData( pt5, INPUT["flowjets_mode2_30_40"+ext1], INPUT["flowjets_mode2_30_40_error"+ext1], kRed, 21, 1.1, "p" );
   PlotData( pt5, INPUT["flowjets_fit_30_40"+ext1], INPUT["flowjets_fit_30_40_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( pt5, INPUT["flow_mode1_30_40"+ext1], INPUT["flow_mode1_30_40_error"+ext1], kBlue, 25, 1.1, "p" );
   PlotData( pt5, INPUT["flow_mode2_30_40"+ext1], INPUT["flow_mode2_30_40_error"+ext1], kRed, 25, 1.1, "p" );
   PlotData( pt5, INPUT["flow_fit_30_40"+ext1], INPUT["flow_fit_30_40_error"+ext1], kCyan, 34, 1.1, "p" );

   //PlotData( pt5, INPUT["flowjets_mode1_30_40"+ext2], INPUT["flowjets_mode1_30_40_error"+ext2], kRed, 25, 1.1, "p" );
   //PlotData( pt5, INPUT["flowjets_mode2_30_40"+ext2], INPUT["flowjets_mode2_30_40_error"+ext2], kBlack,  25, 1.1, "p" );

   PlotData( x23_arr, y23_arr, y23_err, kBlack, 24, 1.1, "p" );

   cc1->cd();

   MakeHisto("P7", Xm+2*W+dw, 0.02, Xm+3*W+dw, 0.512, 0, 0, 0, 0.25, 1);  //  PLOT=7
   DoLine();
   DoText("40-50%");

   PlotData( pt6, INPUT["flowjets_mode1_40_50"+ext1], INPUT["flowjets_mode1_40_50_error"+ext1], kBlue, 21, 1.1, "p" );
   PlotData( pt6, INPUT["flowjets_mode2_40_50"+ext1], INPUT["flowjets_mode2_40_50_error"+ext1], kRed, 21, 1.1, "p" );
   PlotData( pt6, INPUT["flowjets_fit_40_50"+ext1], INPUT["flowjets_fit_40_50_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( pt6, INPUT["flow_mode1_40_50"+ext1], INPUT["flow_mode1_40_50_error"+ext1], kBlue, 25, 1.1, "p" );
   PlotData( pt6, INPUT["flow_mode2_40_50"+ext1], INPUT["flow_mode2_40_50_error"+ext1], kRed, 25, 1.1, "p" );
   PlotData( pt6, INPUT["flow_fit_40_50"+ext1], INPUT["flow_fit_40_50_error"+ext1], kCyan, 34, 1.1, "p" );

   //PlotData( pt6, INPUT["flowjets_mode1_40_50"+ext2], INPUT["flowjets_mode1_40_50_error"+ext2], kRed, 25, 1.1, "p" );
   //PlotData( pt6, INPUT["flowjets_mode2_40_50"+ext2], INPUT["flowjets_mode2_40_50_error"+ext2], kBlack, 25, 1.1, "p" );

   PlotData( x24_arr, y24_arr, y24_err, kBlack, 24, 1.1, "p" );

   cc1->cd();

   MakeHisto("P8", Xm+3*W+dw, 0.02, Xm+4*W-dw, 0.512, 0, 0.01, 0, 0.25, 1);  //  PLOT=8
   DoLine();
   DoText("50-60%");

   PlotData( pt7, INPUT["flowjets_mode1_50_60"+ext1], INPUT["flowjets_mode1_50_60_error"+ext1], kBlue, 21, 1.1, "p" );
   PlotData( pt7, INPUT["flowjets_mode2_50_60"+ext1], INPUT["flowjets_mode2_50_60_error"+ext1], kRed, 21, 1.1, "p" );
   PlotData( pt7, INPUT["flowjets_fit_50_60"+ext1], INPUT["flowjets_fit_50_60_error"+ext1], kGreen, 34, 1.1, "p" );
   PlotData( pt7, INPUT["flow_mode1_50_60"+ext1], INPUT["flow_mode1_50_60_error"+ext1], kBlue, 25, 1.1, "p" );
   PlotData( pt7, INPUT["flow_mode2_50_60"+ext1], INPUT["flow_mode2_50_60_error"+ext1], kRed, 25, 1.1, "p" );
   PlotData( pt7, INPUT["flow_fit_50_60"+ext1], INPUT["flow_fit_50_60_error"+ext1], kCyan, 34, 1.1, "p" );

   //PlotData( pt7, INPUT["flowjets_mode1_50_60"+ext2], INPUT["flowjets_mode1_50_60_error"+ext2], kRed, 25, 1.1, "p" );
   //PlotData( pt7, INPUT["flowjets_mode2_50_60"+ext2], INPUT["flowjets_mode2_50_60_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   ////////////////////////////////////////////////
   //
   //cc1->Print("~/www/09-05-2016/hydjet/4/2/cc1_1.png");
   //cc1->Print("~/www/10-05-2016/hydjet/4/2/cc1_1.png");
   //cc1->Print((string("~/www/14-05-2016/hydjet/4/")+string(s1)+string("/")+string(deta1)+string("/cc1_1.png")).c_str());
   //std::ifstream t1("INPUT.txt");
   //std::string str1((std::istreambuf_iterator<char>(t1)),
   //                 std::istreambuf_iterator<char>());
   //std::ifstream t(str1.substr(0, str1.size()-1)+string("OPATH.txt").c_str());
   std::ifstream t(string("OPATH.txt").c_str());
   std::string str((std::istreambuf_iterator<char>(t)),
                    std::istreambuf_iterator<char>());
   cc1->Print((str.substr(0, str.size()-1)+string("6/")+string(s1)+string("/")+string(deta1)+string("/cc1_2.png")).c_str());
   cc1->Print((str.substr(0, str.size()-1)+string("6/")+string(s1)+string("/")+string(deta1)+string("/cc1_2.pdf")).c_str());
}
