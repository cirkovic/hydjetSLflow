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


#include "rapidjson/document.h"     // rapidjson's DOM-style API
#include "rapidjson/prettywriter.h" // for stringify JSON
#include "rapidjson/filereadstream.h"
#include <cstdio>


using namespace rapidjson;
using namespace std;

double maximum = 0.29;
double lvpos = 0.13/0.29*maximum;

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
   hist->GetXaxis()->SetLabelOffset(0.006);
   hist->GetXaxis()->SetLabelSize(16);
   hist->GetXaxis()->SetTitleSize(20);
   hist->GetXaxis()->SetTitleFont(43);
   
   if (check=="P5"|| check=="P6" || check=="P7" || check=="P8") {

       hist->GetXaxis()->SetTitle("p_{T} (GeV/c)");
       hist->GetXaxis()->CenterTitle(true);
       hist->GetXaxis()->SetTitleOffset(2.47);

   }

   if (check=="P1"|| check=="P5" ) {
      hist->GetYaxis()->SetTitle("v^{(#alpha)}_{2/3}");
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

   TLegend *leg = new TLegend(0.1,0.4,0.48,0.6, NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextSize(0.075);
   leg->SetLineColor(1);
   leg->SetLineStyle(2);
   leg->SetLineWidth(1);
 
   TLegendEntry *entry=leg->AddEntry("", "#alpha=1 n=2","p");
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


   entry=leg->AddEntry("", "#alpha=1 n=3","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kMagenta);
   entry->SetMarkerStyle(25);
   entry->SetMarkerSize(1.2);

   entry=leg->AddEntry("", "#alpha=2 n=3","p");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(4);
   entry->SetMarkerColor(kBlack);
   entry->SetMarkerStyle(25);
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

   TText *t = new TText(2.45,lvpos, text);
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
               double BottomMargin
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


void EFF_VS_NO_EFF_1(const char *s, const char *deta){


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

   /////////////////////////////
   ///////////////////////////////////////////////////
  
   MakeHisto("P1", 0, 0.512, Xm+W+dw, 1, 0.23, 0, 0.25, 0);  // PLOT=1  UCC
   DoLine();
   DoText("0-0.2%");
   DoLatex(0.28, 0.61, "PbPb  #sqrt{s_{NN}} = 2.76 TeV");//position, text
   DoLatex(0.28, 0.50, "#scale[1.1]{Hydjet}");//position, text

   PlotData( pt, INPUT["mode1_UCC"+ext1], INPUT["mode1_UCC_error"+ext1], kBlue, 21, 1.1, "pl" );
   //PlotData( pt, INPUT["mode2_UCC"+ext1], INPUT["mode2_UCC_error"+ext1], kRed, 21, 1.1, "pl" );

   PlotData( pt, INPUT["mode1_UCC"+ext2], INPUT["mode1_UCC_error"+ext2], kMagenta, 25, 1.1, "p" );
   //PlotData( pt, INPUT["mode2_UCC"+ext2], INPUT["mode2_UCC_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();
   ////////////////////////////////////////////////////

   MakeHisto("P2", Xm+W+dw, 0.512, Xm+2*W+dw, 1, 0, 0, 0.25, 0);  //  PLOT=2  0-5
   DoLine();
   DoText("0-5%");

   PlotData( pt, INPUT["mode1_00_05"+ext1], INPUT["mode1_00_05_error"+ext1], kBlue, 21, 1.1, "pl" );
   //PlotData( pt, INPUT["mode2_00_05"+ext1], INPUT["mode2_00_05_error"+ext1], kRed, 21, 1.1, "pl" );

   PlotData( pt, INPUT["mode1_00_05"+ext2], INPUT["mode1_00_05_error"+ext2], kMagenta, 25, 1.1, "p" );
   //PlotData( pt, INPUT["mode2_00_05"+ext2], INPUT["mode2_00_05_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   MakeHisto("P3", Xm+2*W+dw, 0.512, Xm+3*W+dw, 1, 0, 0, 0.25, 0);  //  PLOT=3   0-10
   DoLine();
   DoText("0-10%");
   DoLegend();

   PlotData( pt, INPUT["mode1_00_10"+ext1], INPUT["mode1_00_10_error"+ext1], kBlue, 21, 1.1, "pl" );
   //PlotData( pt, INPUT["mode2_00_10"+ext1], INPUT["mode2_00_10_error"+ext1], kRed, 21, 1.1, "pl" );

   PlotData( pt, INPUT["mode1_00_10"+ext2], INPUT["mode1_00_10_error"+ext2], kMagenta, 25, 1.1, "p" );
   //PlotData( pt, INPUT["mode2_00_10"+ext2], INPUT["mode2_00_10_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   MakeHisto("P4", Xm+3*W+dw, 0.512, Xm+4*W-dw, 1, 0, 0.01, 0.25, 0);  //  PLOT=4  10-20
   DoLine();
   DoText("10-20%");

   PlotData( pt, INPUT["mode1_10_20"+ext1], INPUT["mode1_10_20_error"+ext1], kBlue, 21, 1.1, "pl" );
   //PlotData( pt, INPUT["mode2_10_20"+ext1], INPUT["mode2_10_20_error"+ext1], kRed, 21, 1.1, "pl" );

   PlotData( pt, INPUT["mode1_10_20"+ext2], INPUT["mode1_10_20_error"+ext2], kMagenta, 25, 1.1, "p" );
   //PlotData( pt, INPUT["mode2_10_20"+ext2], INPUT["mode2_10_20_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   MakeHisto("P5", 0, 0.02, Xm+W+dw, 0.512, 0.23, 0, 0, 0.25);  //  PLOT=5
   DoLine();
   DoText("20-30%");

   PlotData( pt, INPUT["mode1_20_30"+ext1], INPUT["mode1_20_30_error"+ext1], kBlue, 21, 1.1, "pl" );
   //PlotData( pt, INPUT["mode2_20_30"+ext1], INPUT["mode2_20_30_error"+ext1], kRed, 21, 1.1, "pl" );

   PlotData( pt, INPUT["mode1_20_30"+ext2], INPUT["mode1_20_30_error"+ext2], kMagenta, 25, 1.1, "p" );
   //PlotData( pt, INPUT["mode2_20_30"+ext2], INPUT["mode2_20_30_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   MakeHisto("P6", Xm+W+dw, 0.02, Xm+2*W+dw, 0.512, 0, 0, 0, 0.25);  //  PLOT=6
   DoLine();
   DoText("30-40%");

   PlotData( pt, INPUT["mode1_30_40"+ext1], INPUT["mode1_30_40_error"+ext1], kBlue, 21, 1.1, "pl" );
   //PlotData( pt, INPUT["mode2_30_40"+ext1], INPUT["mode2_30_40_error"+ext1], kRed, 21, 1.1, "pl" );

   PlotData( pt, INPUT["mode1_30_40"+ext2], INPUT["mode1_30_40_error"+ext2], kMagenta, 25, 1.1, "p" );
   //PlotData( pt, INPUT["mode2_30_40"+ext2], INPUT["mode2_30_40_error"+ext2], kBlack,  25, 1.1, "p" );

   cc1->cd();

   MakeHisto("P7", Xm+2*W+dw, 0.02, Xm+3*W+dw, 0.512, 0, 0, 0, 0.25);  //  PLOT=7
   DoLine();
   DoText("40-50%");

   PlotData( pt, INPUT["mode1_40_50"+ext1], INPUT["mode1_40_50_error"+ext1], kBlue, 21, 1.1, "pl" );
   //PlotData( pt, INPUT["mode2_40_50"+ext1], INPUT["mode2_40_50_error"+ext1], kRed, 21, 1.1, "pl" );

   PlotData( pt, INPUT["mode1_40_50"+ext2], INPUT["mode1_40_50_error"+ext2], kMagenta, 25, 1.1, "p" );
   //PlotData( pt, INPUT["mode2_40_50"+ext2], INPUT["mode2_40_50_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   MakeHisto("P8", Xm+3*W+dw, 0.02, Xm+4*W-dw, 0.512, 0, 0.01, 0, 0.25);  //  PLOT=8
   DoLine();
   DoText("50-60%");

   PlotData( pt, INPUT["mode1_50_60"+ext1], INPUT["mode1_50_60_error"+ext1], kBlue, 21, 1.1, "pl" );
   //PlotData( pt, INPUT["mode2_50_60"+ext1], INPUT["mode2_50_60_error"+ext1], kRed, 21, 1.1, "pl" );

   PlotData( pt, INPUT["mode1_50_60"+ext2], INPUT["mode1_50_60_error"+ext2], kMagenta, 25, 1.1, "p" );
   //PlotData( pt, INPUT["mode2_50_60"+ext2], INPUT["mode2_50_60_error"+ext2], kBlack, 25, 1.1, "p" );

   cc1->cd();

   ////////////////////////////////////////////////
   //
   //cc1->Print("~/www/09-05-2016/hydjet/4/2/cc1_1.png");
   //cc1->Print("~/www/10-05-2016/hydjet/4/2/cc1_1.png");
   //cc1->Print((string("~/www/14-05-2016/hydjet/4/")+string(s)+string("/")+string(deta)+string("/cc1_1.png")).c_str());
   cc1->Print((string("~/www/27-05-2016/hydjet/4/")+string(s)+string("/")+string(deta)+string("/cc1_1.png")).c_str());
}
