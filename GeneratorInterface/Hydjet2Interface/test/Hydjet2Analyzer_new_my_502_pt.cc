// -*- C++ -*-
//
// Package: Hydjet2Analyzer_new_my_502_pt
// Class: Hydjet2Analyzer_new_my_502_pt
//
/**\class HydjetAnalyzer HydjetAnalyzer.cc yetkin/HydjetAnalyzer/src/HydjetAnalyzer.cc
   Description: <one line class summary>
   Implementation:
   <Notes on implementation>
*/
//
// Original Author: Yetkin Yilmaz
// Created: Tue Dec 18 09:44:41 EST 2007
//
//
// system include files
#include <memory>
#include <iostream>
#include <string>
#include <fstream>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
//#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/CrossingFrame/interface/MixCollection.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"
#include "SimDataFormats/HiGenData/interface/GenHIEvent.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "HepMC/GenEvent.h"
#include "HepMC/HeavyIon.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
// root include file
#include "TFile.h"
#include "TNtuple.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TMath.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
using namespace reco;
using namespace std;
using namespace edm;
static const int MAXPARTICLES = 5000000;
static const int ETABINS = 3; // Fix also in branch string
static const int MY_CODE = 3;

int NITERS = 0, WR_COUNT_DONE = 1; //15;
//
// class decleration
//
struct Hydjet2Event{
  int event;
  float b;
  float npart;
  float ncoll;
  float nhard;
  float phi0;
  float scale;
  int n[ETABINS];
  float ptav[ETABINS];
  int mult;
  float px[MAXPARTICLES];
  float py[MAXPARTICLES];
  float pz[MAXPARTICLES];
  float e[MAXPARTICLES];
  float pseudoRapidity[MAXPARTICLES];
  float pt[MAXPARTICLES];
  float eta[MAXPARTICLES];
  float phi[MAXPARTICLES];
  int pdg[MAXPARTICLES];
  int chg[MAXPARTICLES];
  float vx;
  float vy;
  float vz;
  float vr;
};

struct TRIPLET {

   double pt;
   double phi;
   double eta;
   int track_label;

};

struct EVENT {

   map< string, vector<TRIPLET> >PT;
   int event_label;
   //double z_vertex;
   //int centrality;

   string table;

};

struct COMB{   // to write comb.

   int label1;
   int label2;
};

class Hydjet2Analyzer_new_my_502_pt : public edm::EDAnalyzer {
public:
  explicit Hydjet2Analyzer_new_my_502_pt(const edm::ParameterSet&);
  ~Hydjet2Analyzer_new_my_502_pt();
private:
  virtual void beginRun(const edm::Run&, const edm::EventSetup&) ;
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  // ----------member data ---------------------------
  std::ofstream out_b;
  std::string fBFileName;
  std::ofstream out_n;
  std::string fNFileName;
  std::ofstream out_m;
  std::string fMFileName;
  //TTree* hydjetTree_;
  Hydjet2Event hev_;
  TNtuple *nt;
  std::string output; // Output filename
  bool doAnalysis_;
  bool printLists_;
  bool doCF_;
  bool doVertex_;
  bool useHepMCProduct_;
  bool doHI_;
  bool doParticles_;
  double etaMax_;
  double deltaEtaCut_;
  double ptMin_;
  edm::InputTag src_;
  edm::InputTag genParticleSrc_;
  edm::InputTag genHIsrc_;
  edm::InputTag simVerticesTag_;
  edm::ESHandle < ParticleDataTable > pdt;
  //edm::Service<TFileService> f;
  //TH1F *hevt, *hmult1L, *hmult2L, *hpt1L, *hpt2L, *hsum_cosL, *hsum_cos_normL;
  TH1F *hevt, *hmult1L, *hpt1L, *hsum_cosL, *hsum_cos_normL;
  TH1F *hpt;
  TH2F *hdelta_eta_phi;
  TH2F *hfractionS, *hfractionB, *heventcountS, *heventcountB;
  //TH1F **Hmult1L, **Hmult2L, **Hpt1L, **Hpt2L, **Hsum_cosL, **Hsum_cos_normL;
  TH1F **Hmult1L, **Hpt1L, **Hsum_cosL, **Hsum_cos_normL;
  TH2F **Hdelta_eta_phiS, **Hdelta_eta_phiScut, **Hdelta_eta_phiB;
  std::string foutname;
  TFile *fout;
  int nHarr, nHarr1;
  int WR_COUNT;
  int EVT;

  //USER FUNCTIONS
  TString ToString(float);
  //void DO_BACKGROUND(vector<EVENT>, string);
  //void DO_BACKGROUND( EVENT*, string, int);
  void DO_BACKGROUND2( EVENT*, vector<pair<int, int>>, string Noff_name = string(""));
  void CORRELATION_OF_MIXED_EVENTS(map<string, vector<TRIPLET>>, map<string, vector<TRIPLET>>, string Noff_name = string(""));
  int check_combination(int, int);
  int myrandom (int ); 

  //
  //USER VARIABLES
  //Service<TFileService> fs;
  //ofstream FOUT;
  map<string, pair<double, double> >BIN;//BIN['Pi'].first=min
  map<string, pair<double, double> >Noff_ranges;//BIN['Pi'].second=max
  //map<string,vector<EVENT>> BACKGROUND_EVENTS;
  EVENT BACKGROUND_EVENTS[1000];
  
  vector< pair<string, string> >BIN_PAIRS;
  vector< pair<int, int> >BIN_PAIRS2;//for histogram filling

  //vector<string> which_Noff;//only to loop names
  vector<string> which_Bin;//only to loop names
  vector< pair<string, int> > which_n_type;//only to loop names

  //vector<COMB> WRITE_COMBS;

  int EVENT_LABEL;
  int hiBin, hiNtracks; //centrality rep, number of tracks
  ofstream myfile;
  bool DO_TRACK_CUT;
  bool DO_SIGNAL;
  bool DO_BACK;
  bool DO_DIAG;
  bool DO_NONDIAG;

  /* CIRKOVIC COMMENTS */
  //CentralityProvider * centProvider;
  /**/

  //CutParameters cutPara;

  //HISTOGRAMS
  //
  TH1F *trackhisto;
  TH1F *histo_vertex_z;
  TH1F *histo_vertex_x;
  TH1F *histo_vertex_y;

  TH1F *histo_mix;

  map<string, TH1F*>HISTOGRAMS_1D;//string="pi_classi"
  map<string, TH2F*>HISTOGRAMS_2D;//

  //map<string, TFile*>EFF_FILES;//string="pi_classi"
  //map<string, TH2F*> EFF_HISTOS;//

  unsigned int Nbins;
};
//
// constants, enums and typedefs
//
//
// static data member definitions
//
//
// constructors and destructor
//
Hydjet2Analyzer_new_my_502_pt::Hydjet2Analyzer_new_my_502_pt(const edm::ParameterSet& iConfig)
{
  //now do what ever initialization is needed
  fBFileName = iConfig.getUntrackedParameter<std::string>("output_b", "b_values.txt");
  fNFileName = iConfig.getUntrackedParameter<std::string>("output_n", "n_values.txt");
  fMFileName = iConfig.getUntrackedParameter<std::string>("output_m", "m_values.txt");
  doAnalysis_ = iConfig.getUntrackedParameter<bool>("doAnalysis", true);
  useHepMCProduct_ = iConfig.getUntrackedParameter<bool>("useHepMCProduct", true);
  consumes<HepMCProduct>(iConfig.getParameter<edm::InputTag>("HepMCProductLabel"));
  printLists_ = iConfig.getUntrackedParameter<bool>("printLists", false);
  doCF_ = iConfig.getUntrackedParameter<bool>("doMixed", false);
  doVertex_ = iConfig.getUntrackedParameter<bool>("doVertex", false);
  if (doVertex_) {
    simVerticesTag_ = iConfig.getParameter<edm::InputTag>("simVerticesTag");
  }
  etaMax_ = iConfig.getUntrackedParameter<double>("etaMax", 2.);
  deltaEtaCut_ = iConfig.getUntrackedParameter<double>("deltaEtaCut", 2.0);
  cout << "Which deltaEtaCut=" << deltaEtaCut_ << endl;
  ptMin_ = iConfig.getUntrackedParameter<double>("ptMin", 0);
  src_ = iConfig.getUntrackedParameter<edm::InputTag>("src",edm::InputTag("generator"));
  genParticleSrc_ = iConfig.getUntrackedParameter<edm::InputTag>("src",edm::InputTag("hiGenParticles"));
  genHIsrc_ = iConfig.getUntrackedParameter<edm::InputTag>("src",edm::InputTag("heavyIon"));
  doParticles_ = iConfig.getUntrackedParameter<bool>("doParticles", true);
  foutname = iConfig.getUntrackedParameter<std::string>("foutName", "output.root");
  fout = 0;
  
   //ofstream FOUT;
   //FOUT.open("DATA.txt");
   //now do what ever initialization is needed
   
   Nbins=iConfig.getParameter<int>("Nbins");

   DO_TRACK_CUT=iConfig.getParameter<bool>("track_cut");
   DO_SIGNAL=iConfig.getParameter<bool>("DO_SIGNAL");
   DO_BACK=iConfig.getParameter<bool>("DO_BACKGROUND");
   DO_DIAG=iConfig.getParameter<bool>("DO_DIAG");
   DO_NONDIAG=iConfig.getParameter<bool>("DO_NONDIAG");

   //TString table_name=iConfig.getParameter<string>("table_name");

   //EFF_FILES["TABLE"]=new TFile(table_name);
   //EFF_HISTOS["TABLE"]=(TH2F*)EFF_FILES["TABLE"]->Get("rTotalEff3D");

   double min;
   double max;
   string pt_bin;
   pair<string, string> bin_ij;

   EVENT_LABEL=0;

   ///////////////////////////// PT_RANGES
   //
   for (unsigned int bin=1; bin<Nbins+1; bin++){
  
        pt_bin="P"+ToString(bin);
        which_Bin.push_back(pt_bin);

        ParameterSet PT=iConfig.getParameter<ParameterSet>(pt_bin);

        min=PT.getParameter<double>("min");
        max=PT.getParameter<double>("max");
      
        BIN[pt_bin].first=(min); 
        BIN[pt_bin].second=(max); 

   }
   /////////////////////////////////
   //
   //

  if (DO_NONDIAG==true){

        for (unsigned int i=1; i<Nbins+1; i++){   //MAKE NON_DIAG. PAIRS
                 for (unsigned int j=i+1; j<Nbins+1; j++){

                         bin_ij.first="P"+ToString(i);
                         bin_ij.second="P"+ToString(j);

                         BIN_PAIRS.push_back(bin_ij);
                         BIN_PAIRS2.push_back(make_pair(i,j));
                 }
        }
  }

  if (DO_DIAG==true){

      for (unsigned int i=1; i<Nbins+1; i++){    //DIAG. PAIRS

             bin_ij.first="P"+ToString(i);
             bin_ij.second="P"+ToString(i);

             BIN_PAIRS.push_back(bin_ij);
             BIN_PAIRS2.push_back(make_pair(i,i));

      }

  }


  /*
     cout << "CIRKOVIC: BIN PAIRS" << endl;
     for (unsigned int bin_pair=0; bin_pair<BIN_PAIRS.size(); bin_pair++){//BIN COMBINATIONS****************************
              cout << BIN_PAIRS[bin_pair].first << "\t" << BIN_PAIRS[bin_pair].second << endl;
     }

     exit(0);
  */

  ////////////////////////////////////
  // Centrality
  ///////////////////////////////////

  //vector<ParameterSet> MultiplicityParameter = iConfig.getParameter<vector<ParameterSet>>("CentralityClasses");
  //string Noff_class;

  /*
  for (unsigned int i=0; i<MultiplicityParameter.size(); i++){

         if (MultiplicityParameter[i].getParameter<bool>("switch")==true){

                 Noff_class=MultiplicityParameter[i].getParameter<string>("name");

                 Noff_ranges[Noff_class].first=(MultiplicityParameter[i].getParameter<int>("Bin_min"));
                 Noff_ranges[Noff_class].second=(MultiplicityParameter[i].getParameter<int>("Bin_max"));

                 cout<<"Which centrality classes="<<Noff_ranges[Noff_class].first<<" "<<Noff_ranges[Noff_class].second<<endl;
       
                 which_Noff.push_back(Noff_class);

         }
    }
  */

   // exit(0);

  ////////////////////////////////////
  //
  ////////////////////////////////////
  
  ///////////////////////////////////
  //Degree Type
  //////////////////////////////////

  vector<ParameterSet> DegreeTypeParameter = iConfig.getParameter<vector<ParameterSet>>("DegreeClass");
  string degree_type_name;
  int degree_type_value;
  pair<string, int> temp_pair;

  for (unsigned int i=0; i<DegreeTypeParameter.size(); i++){

         if (DegreeTypeParameter[i].getParameter<bool>("switch")==true){

                 degree_type_name = DegreeTypeParameter[i].getParameter<string>("name");
                 degree_type_value= DegreeTypeParameter[i].getParameter<int>("n_type");
              
                 temp_pair=make_pair(degree_type_name, degree_type_value);

                 which_n_type.push_back(temp_pair);

         }

  }

  nHarr = BIN_PAIRS.size();
  nHarr1 = BIN_PAIRS.size() * 2;
  WR_COUNT = 0;
  EVT = 0;

  //////////////////////////////////
  //
}
Hydjet2Analyzer_new_my_502_pt::~Hydjet2Analyzer_new_my_502_pt()
{
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}
//
// member functions
//

TString Hydjet2Analyzer_new_my_502_pt::ToString(float num){

        ostringstream start;
        start<<num;
        string start1=start.str();

        return start1;

}

int Hydjet2Analyzer_new_my_502_pt::myrandom (int i) { return std::rand()%i;}

//
// ------------ method called to for each event ------------
void
Hydjet2Analyzer_new_my_502_pt::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  /*
  if (MY_CODE == 2) {
      using namespace edm;
      using namespace HepMC;
      unsigned int cmult = 0;
      const GenEvent* evt;
      Handle<HepMCProduct> mc;
      iEvent.getByLabel(src_,mc);
      evt = mc->GetEvent();

      for(HepMC::GenEvent::particle_const_iterator it = evt->particles_begin(); it != evt->particles_end(); ++it){
        if((*it)->status() == 1){
          int pdg_id = (*it)->pdg_id();
          float pt = (*it)->momentum().perp();
          float eta = (*it)->momentum().eta();
          float phi = (*it)->momentum().phi();
          //cout << pdg_id << endl;
          const ParticleData *part = 0;
          part = pdt->particle(pdg_id);
          if (part) {
              int charge = static_cast<int>(part->charge());
              //if (charge != 0) {
              //if (abs(pdg_id) == 211 && pt > 0.4 && eta < 2.4) {
              if (abs(pdg_id) == 211 && pt > 0.3 && eta < 2.4) {
                hpt->Fill(pt);
                heta->Fill(eta);
                hphi->Fill(phi);
                hcharge->Fill(charge);
                hpdg_id->Fill(pdg_id);
                ++(cmult);
              }
          }
        }
      }

      hmult->Fill(cmult);
  }
  else */
  if (MY_CODE == 3) {

   using namespace edm;
   using namespace HepMC;
   //unsigned int cmult = 0;
   const GenEvent* evt;
   Handle<HepMCProduct> mc;
   iEvent.getByLabel(src_,mc);
   evt = mc->GetEvent();


   //FOUT.open("DATA.txt");
   //input data
   //Handle<reco::TrackCollection> tracks;
   //Handle<reco::VertexCollection> vertexCollection;

   //iEvent.getByLabel("hiGeneralAndPixelTracks", tracks);
   //iEvent.getByLabel("hiSelectedVertex", vertexCollection);

   //iEvent.getByLabel("generalTracks", tracks);
   //iEvent.getByLabel("offlinePrimaryVertices", vertexCollection);


   //const VertexCollection * recoVertices = vertexCollection.product();

   //int primaryvtx = 0;
   int number_of_tracks=0;

   //math::XYZPoint v1( (*recoVertices)[primaryvtx].position().x(), (*recoVertices)[primaryvtx].position().y(), (*recoVertices)[primaryvtx].position().z() );
   //double vxError = (*recoVertices)[primaryvtx].xError();
   //double vyError = (*recoVertices)[primaryvtx].yError();
   //double vzError = (*recoVertices)[primaryvtx].zError();	

   //double d0;
   //double derror;
   //double dz;
   //double dzerror;

   /////////////////////////////////////
   //  centrality const.
   /////////////////////////////////////

   /*
   centProvider = 0;

   if (!centProvider) centProvider = new CentralityProvider(iSetup);

   centProvider->newEvent(iEvent,iSetup);
   const Centrality* centrality = centProvider->raw();
   hiBin = centProvider->getBin();
   hiNtracks = centrality->Ntracks();


   trackhisto->Fill(hiNtracks);

   delete centProvider;
   */
   /////////////////////////////////////

    /////////////////////////////////// 
    //  CHECK Noff class
    ///////////////////////////////////
 
    
    /*
    string Noff_name;
    string Noff_temp;
    bool found_Noff=false;

    for (unsigned int i=0; i < which_Noff.size(); i++) {

             Noff_temp= which_Noff[i];
             if ((Noff_ranges[Noff_temp].first<=hiBin) && (hiBin<=Noff_ranges[Noff_temp].second)){

                                 found_Noff=true;
                                 Noff_name=which_Noff[i];
             } 
    }
    */
    bool found_Noff=true;
    
    ///////////////////////////////////

    //histo_vertex_z->Fill((*recoVertices)[primaryvtx].position().z());
    //histo_vertex_x->Fill((*recoVertices)[primaryvtx].position().x());
    //histo_vertex_y->Fill((*recoVertices)[primaryvtx].position().y());


   ////////////////////////////////////////////////////////////
   // TO COLLECT phi, eta, pt
   ////////////////////////////////////////////////////////////

    map< string, vector<TRIPLET> >PT; //
    TRIPLET PtPhiEta;
    EVENT CURRENT_EVENT;//FOR BACKGROUND GROUPING
  
    string first_bin;
    string second_bin;
    string bin_label;
 
    double BIN_MIN;
    double BIN_MAX;
    int track_label=0;
    //double z_diff;
    //int MIX_LIMIT=300;
    //int MIX_LIMIT=200;
    int MIX_LIMIT=3;

    vector<pair<int, int>> ALL_PAIRS;
    vector<pair<int, int>> SELECTED_PAIRS;
    vector<int>SKIPING;
    vector<int>SKIPING2;
    double track_to_skip=0;

    ////////////////////////////////////////////////////////////


    if (found_Noff==true){//SELECT TRACKS ONLY IF Noff EXIST FOR GIVEN CLASSES
                          //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                          //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

          ////////////////////////////////////////////

          /*
          if (DO_TRACK_CUT==true){

          / *
          for(TrackCollection::const_iterator TRACK = tracks->begin(); TRACK != tracks->end(); TRACK++) {//SELECT N0ff

                if ( !TRACK->quality(reco::TrackBase::highPurity) ) continue;
                if ( fabs(TRACK->eta()) > 2.4 ) continue;
                //if (fabs((*recoVertices)[primaryvtx].position().z())>15)  continue;
                if ( TRACK->charge() == 0 ) continue;

                track_to_skip++;
                SKIPING.push_back(track_to_skip);
      
          }// TO SET TRACKS FOR SKIPING
          * /


          for(HepMC::GenEvent::particle_const_iterator it = evt->particles_begin(); it != evt->particles_end(); ++it){
            if((*it)->status() == 1){
              int pdg_id = (*it)->pdg_id();
              float pt = (*it)->momentum().perp();
              float eta = (*it)->momentum().eta();
              //float phi = (*it)->momentum().phi();
              const ParticleData *part = 0;
              part = pdt->particle(pdg_id);
              if (part) {
                  //int charge = static_cast<int>(part->charge());
                  //if (abs(pdg_id) == 211 && pt > 0.4 && eta < 2.4) {
                  if (abs(pdg_id) == 211 && pt > 0.3 && eta < 2.4) {
                    track_to_skip++;
                    SKIPING.push_back(track_to_skip);
                  }
              }
            }
          }


          track_to_skip=0.30*track_to_skip;
          track_to_skip=(int)track_to_skip;

          std::random_shuffle ( SKIPING.begin(), SKIPING.end());
 
          for (unsigned int i=0; i<track_to_skip; i++ ) {

                 SKIPING2.push_back(SKIPING[i]);
          }

          }
          */
 
          /////////////////////////////////////////////

          EVENT_LABEL+=1;
          CURRENT_EVENT.event_label=EVENT_LABEL;
          //CURRENT_EVENT.z_vertex= (*recoVertices)[primaryvtx].position().z();
          //CURRENT_EVENT.centrality=hiBin;
   
          /*
          for(TrackCollection::const_iterator TRACK = tracks->begin(); TRACK != tracks->end(); TRACK++) {//SELECT N0ff

                if ( !TRACK->quality(reco::TrackBase::highPurity) ) continue;
                if ( fabs(TRACK->eta()) > 2.4 ) continue;
                //if (fabs((*recoVertices)[primaryvtx].position().z())>15)  continue;
                if ( TRACK->charge() == 0 ) continue;

                track_to_skip++;

                if (SKIPING2.empty()==false) {

                   if(std::find(SKIPING2.begin(), SKIPING2.end(), track_to_skip) != SKIPING2.end()) continue;
                    
                }

                track_label++;
                number_of_tracks++;

                PtPhiEta.pt=TRACK->pt();
                PtPhiEta.phi=TRACK->phi();
                PtPhiEta.eta=TRACK->eta();
                PtPhiEta.track_label=track_label;

                for (unsigned int bin=0; bin<which_Bin.size(); bin++){
 
                      bin_label=which_Bin[bin];                       

                      BIN_MIN= BIN[bin_label].first;
                      BIN_MAX= BIN[bin_label].second;
               
                      if ( BIN_MIN < TRACK->pt() && TRACK->pt()<BIN_MAX ) {

                             PT[bin_label].push_back(PtPhiEta);
                             CURRENT_EVENT.PT[bin_label].push_back(PtPhiEta);//for background
                             HISTOGRAMS_1D["Pt_"+bin_label+"_"+Noff_name]->Fill(TRACK->pt());
                      }

                }

          }//tracks loop
          */

          unsigned int multiplicity = 0;

          for(HepMC::GenEvent::particle_const_iterator it = evt->particles_begin(); it != evt->particles_end(); ++it){
            if((*it)->status() == 1){
              int pdg_id = (*it)->pdg_id();
              float pt = (*it)->momentum().perp();
              float eta = (*it)->momentum().eta();
              float phi = (*it)->momentum().phi();
              const ParticleData *part = 0;
              part = pdt->particle(pdg_id);
              if (part) {
                  //int charge = static_cast<int>(part->charge());
                  //if (abs(pdg_id) == 211 && pt > 0.4 && eta < 2.4) {
                  //if (abs(pdg_id) == 211 && pt > 0.3 && abs(eta) < 2.4) {
                  if (abs(pdg_id) == 211 && pt > 0.25 && pt < 15.0 && abs(eta) < 2.4) {

                    track_to_skip++;

                    /*
                    if (SKIPING2.empty()==false) {

                       if(std::find(SKIPING2.begin(), SKIPING2.end(), track_to_skip) != SKIPING2.end()) continue;

                    }
                    */

                    track_label++;
                    number_of_tracks++;

                    PtPhiEta.pt=pt;
                    PtPhiEta.phi=phi;
                    PtPhiEta.eta=eta;
                    PtPhiEta.track_label=track_label;

                    multiplicity++;

                    for (unsigned int bin=0; bin<which_Bin.size(); bin++){

                          bin_label=which_Bin[bin];

                          BIN_MIN= BIN[bin_label].first;
                          BIN_MAX= BIN[bin_label].second;

                          if ( BIN_MIN < pt && pt<BIN_MAX ) {

                                 PT[bin_label].push_back(PtPhiEta);
                                 CURRENT_EVENT.PT[bin_label].push_back(PtPhiEta);//for background
                                 //HISTOGRAMS_1D["Pt_"+bin_label+"_"+Noff_name]->Fill(pt);
                          }

                    }              
                    hpt->Fill(pt);
                  
                  }
              }
            }
          }


     ///////////////////////////////////////////////////
    //  BACKGROUND SELECTION
   /////////////////////////////////////////////////////  

     BACKGROUND_EVENTS[EVENT_LABEL]=CURRENT_EVENT;// "0" element not filled

     //int MIX_COUNT;
     //int which_event;
     //unsigned int ALL_PAIRS_SIZE;

     if (EVENT_LABEL==MIX_LIMIT){   //************************
                             //************************

          for (int i=1; i<EVENT_LABEL; i++){

              for (int j=i+1; j<EVENT_LABEL+1; j++){

                     //z_diff=BACKGROUND_EVENTS[i].z_vertex - BACKGROUND_EVENTS[j].z_vertex;

                     /*if (fabs(z_diff)<2.0) {

                            ALL_PAIRS.push_back(make_pair(i, j));
                            
                     }*/
                     ALL_PAIRS.push_back(make_pair(i, j));
              }
  
         }

     //MIX_COUNT=0;
     //which_event=0;
 
     std::random_shuffle ( ALL_PAIRS.begin(), ALL_PAIRS.end()); 
     vector<pair<int, int> >::iterator it;

     cout<<"BEGIN........."<<endl;

    /*
     while(MIX_COUNT<MIX_LIMIT*10) {

     which_event++;

     ALL_PAIRS_SIZE=ALL_PAIRS.size();

     cout << "CIRKOVIC DONE1" << MIX_COUNT << endl;
     //exit(0);

     for (unsigned int i=0; i<ALL_PAIRS_SIZE; i++){

           if (ALL_PAIRS[i].first==which_event || ALL_PAIRS[i].second==which_event){

                  //FOUT<<"(i, j)="<<ALL_PAIRS[i].first<<", "<<ALL_PAIRS[i].second<<endl;

                  SELECTED_PAIRS.push_back(make_pair(ALL_PAIRS[i].first, ALL_PAIRS[i].second));
                  ALL_PAIRS.erase (ALL_PAIRS.begin()+i);
         
                  MIX_COUNT++;

                  //histo_mix->Fill(which_event);
                  break;
           }
   
     }
    
     cout << "CIRKOVIC DONE2" << endl;
     //exit(0);
    
     if (which_event==MIX_LIMIT) which_event=0;

     }
    */

     }     // ****************************
           // ****************************

     //HISTOGRAMS_1D["tracks_per_centrality_"+Noff_name]->Fill(number_of_tracks); 

     }//END-found_Noff
     //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
     //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

     //for (unsigned int i=0; i<which_Noff.size(); i++)  {


                if (EVENT_LABEL==MIX_LIMIT){

                      cout<<"DO BACKGROUND!"<<endl;
                      //DO_BACKGROUND(BACKGROUND_EVENTS, which_Noff[i], MIX_LIMIT);
                      //if (DO_BACK==true) DO_BACKGROUND2(BACKGROUND_EVENTS, which_Noff[i], SELECTED_PAIRS);
                      //if (DO_BACK==true) DO_BACKGROUND2(BACKGROUND_EVENTS, SELECTED_PAIRS);
                      if (DO_BACK==true) DO_BACKGROUND2(BACKGROUND_EVENTS, ALL_PAIRS);
                      EVENT_LABEL=0;

                      //WRITE_COMBS.clear();

                }

     //}
     

     //cout << "CIRKOVIC DONE 3" << endl;
     


     ////////////////////////////////////////////////////////////
     //CORRELATION
     ////////////////////////////////////////////////////////////
     //
     double delta_phi;
     double delta_eta;

     int B1;//bin in histogram
     int B2;

     vector<double>sum_cos(which_n_type.size());
     vector<double>sum_sin(which_n_type.size());

     //vector<double>sum_cos_eff(which_n_type.size());
     //vector<double>sum_sin_eff(which_n_type.size());

     double ENTRY;
     //double ENTRY_EFF;
     double TotalNumberOfPairs;
     //double TotalNumberOfPairs_EFF;
     double fraction;
     //double fraction_eff;
     int deg_value;
     string deg_string;

     //double corr1=0;
     //double corr2=0;
     //double corr=0;

    
     if (DO_SIGNAL==true){

     hevt->Fill(EVT);

     unsigned int doffs = BIN_PAIRS.size() - Nbins;

     for (unsigned int bin_pair=0; bin_pair<BIN_PAIRS.size(); bin_pair++){//BIN COMBINATIONS****************************

              //cout << "BIN COMBINATIONS: " << bin_pair << endl;

              //if (NITERS > 200) exit(0);
              //else NITERS ++;
              
              first_bin=BIN_PAIRS[bin_pair].first;
              second_bin=BIN_PAIRS[bin_pair].second;
        
              B1=BIN_PAIRS2[bin_pair].first;
              B2=BIN_PAIRS2[bin_pair].second;
              
              if (PT[first_bin].empty()==true) continue;
              if (PT[second_bin].empty()==true) continue;


              /////////////////////////////////////////////////////////
              // Q1
              ////////////////////////////////////////////////////////
              fill(sum_cos.begin(), sum_cos.end(), 0);
              fill(sum_sin.begin(), sum_sin.end(), 0);

              //fill(sum_cos_eff.begin(), sum_cos_eff.end(), 0);
              //fill(sum_sin_eff.begin(), sum_sin_eff.end(), 0);

              ENTRY=0;
              //ENTRY_EFF=0;
              TotalNumberOfPairs=0;
              //TotalNumberOfPairs_EFF=0;

              if (bin_pair >= doffs) {
                  Hmult1L[bin_pair - doffs]->Fill(PT[first_bin].size());
                  //Hmult2L[bin_pair - doffs]->Fill(PT[second_bin].size());
              }

              for (unsigned int i=0; i<PT[first_bin].size(); i++){

                    for (unsigned int j=0; j<PT[second_bin].size(); j++){

                                   if (bin_pair >= doffs) {
                                       if (j == 0) Hpt1L[bin_pair - doffs]->Fill(PT[first_bin][i].pt);
                                       //if (i == 0) Hpt2L[bin_pair - doffs]->Fill(PT[second_bin][j].pt);
                                   }

                                   delta_phi=PT[first_bin][i].phi - PT[second_bin][j].phi;
                                   delta_eta=PT[first_bin][i].eta - PT[second_bin][j].eta;

                                   if (fabs(delta_eta) == 0) continue;//this will exclude pure autocorrelations

                                   if (PT[first_bin][i].track_label!=PT[second_bin][j].track_label)  {

                                          TotalNumberOfPairs++;

                                          //corr1=1.0/(EFF_HISTOS["TABLE"]->GetBinContent(EFF_HISTOS["TABLE"]->FindBin(PT[first_bin][i].eta, PT[first_bin][i].pt)));
                                          //corr2=1.0/(EFF_HISTOS["TABLE"]->GetBinContent(EFF_HISTOS["TABLE"]->FindBin(PT[second_bin][j].eta, PT[second_bin][j].pt)));

                                          //corr=corr1*corr2;
                                          //TotalNumberOfPairs_EFF+=corr;
                                   }

                                   double delta_phi1 = delta_phi;
                                   if (delta_phi1<-0.5*TMath::Pi()) delta_phi1=delta_phi1+2*TMath::Pi();
                                   if (delta_phi1>1.5*TMath::Pi()) delta_phi1=delta_phi1-2*TMath::Pi();

                                   Hdelta_eta_phiS[bin_pair]->Fill(delta_eta, delta_phi1);

                                   //if (fabs(delta_eta)<2) continue;//this will exclude autocorr. by def.
                                   if (fabs(delta_eta)<deltaEtaCut_) continue;//this will exclude autocorr. by def.

                                   Hdelta_eta_phiScut[bin_pair]->Fill(delta_eta, delta_phi1);

                                   //////////////////////////// efficiency

                                   //corr1=1.0/(EFF_HISTOS["TABLE"]->GetBinContent(EFF_HISTOS["TABLE"]->FindBin(PT[first_bin][i].eta, PT[first_bin][i].pt)));
                                   //corr2=1.0/(EFF_HISTOS["TABLE"]->GetBinContent(EFF_HISTOS["TABLE"]->FindBin(PT[second_bin][j].eta, PT[second_bin][j].pt)));

                                   //corr=corr1*corr2;
                                   
                                   /////////////////////////////

                                   ENTRY+=1;
                                   //ENTRY_EFF+=corr;

 
                                   for (unsigned int deg_count=0; deg_count<which_n_type.size(); deg_count++){

                                      deg_value=which_n_type[deg_count].second;
                                      deg_string=which_n_type[deg_count].first;

                                      sum_cos[deg_count]+=cos(deg_value*(delta_phi));
                                      sum_sin[deg_count]+=sin(deg_value*(delta_phi));

                                      //sum_cos_eff[deg_count]+=corr*cos(deg_value*(delta_phi));
                                      //sum_sin_eff[deg_count]+=corr*sin(deg_value*(delta_phi));

                                   }
                    }//PTj

              }//PTi

              if (ENTRY!=0){     // there is an event with non-zero entry for comb. (pi, pj)
 
                    fraction=ENTRY/TotalNumberOfPairs;
                    //fraction_eff=ENTRY_EFF/TotalNumberOfPairs_EFF;
                    /*
                    HISTOGRAMS_1D["CORR_SIG"+ Noff_name + first_bin + second_bin]->Fill(ENTRY_EFF/ENTRY);
                   
                    HISTOGRAMS_2D["EVENT_COUNT_"+Noff_name]->Fill(B1, B2, 1);// EVENTS TAKEN INTO ACCOUNT
                    */
                    //HISTOGRAMS_2D["PAIR_FRACTION_"+Noff_name]->Fill(B1, B2, fraction);//
                    /*
                    HISTOGRAMS_2D["PAIR_FRACTION_EFF"+Noff_name]->Fill(B1, B2, fraction_eff);//
                    */
                    hfractionS->Fill(B1, B2, fraction);
                    heventcountS->Fill(B1, B2, 1);

                    for (unsigned int deg_count=0; deg_count<which_n_type.size(); deg_count++)  {

                          deg_string=which_n_type[deg_count].first;

                          //if (deg_string!="0"){
                              //HISTOGRAMS_1D["cos_not_normed"+Noff_name+"_n"+deg_string + first_bin + second_bin]->Fill(sum_cos[deg_count]/5);
                              //HISTOGRAMS_1D["cos_normed"+Noff_name+"_n"+deg_string + first_bin + second_bin]->Fill(sum_cos[deg_count]/ENTRY);

                              //HISTOGRAMS_1D["cos_not_normed_eff"+Noff_name+"_n"+deg_string + first_bin + second_bin]->Fill(sum_cos_eff[deg_count]/50);
                              //HISTOGRAMS_1D["cos_normed_eff"+Noff_name+"_n"+deg_string + first_bin + second_bin]->Fill(sum_cos_eff[deg_count]/ENTRY_EFF);

                              hsum_cosL->Fill(sum_cos[deg_count]/5);
                              hsum_cos_normL->Fill(sum_cos[deg_count]/ENTRY);
                              Hsum_cosL[bin_pair*which_n_type.size()+deg_count]->Fill(sum_cos[deg_count]/5);
                              Hsum_cos_normL[bin_pair*which_n_type.size()+deg_count]->Fill(sum_cos[deg_count]/ENTRY);

                          //}

                          //if (deg_string=="0"){
                             /*
                             HISTOGRAMS_1D["pairs_with_cut_"+Noff_name+"_n"+deg_string + first_bin + second_bin]->Fill(ENTRY/1000);
                             HISTOGRAMS_1D["pairs_with_cut_eff"+Noff_name+"_n"+deg_string + first_bin + second_bin]->Fill(ENTRY_EFF/2000);
                             HISTOGRAMS_1D["pairs_total_"+Noff_name+"_n"+deg_string + first_bin + second_bin]->Fill(TotalNumberOfPairs/1000);
                             HISTOGRAMS_1D["pairs_total_eff"+Noff_name+"_n"+deg_string + first_bin + second_bin]->Fill(TotalNumberOfPairs_EFF/5000);
                             */
                          //}

                          /*
                          hsum_cosL->Fill(sum_cos[deg_count]/5);
                          hsum_cos_normL->Fill(sum_cos[deg_count]/ENTRY);
                          Hsum_cosL[bin_pair*3+deg_count]->Fill(sum_cos[deg_count]/5);
                          Hsum_cos_normL[bin_pair*3+deg_count]->Fill(sum_cos[deg_count]/ENTRY);
                          */

                    }
                          
              }
              //////////////////////////////////////////////////////

              
              ///////////////////////////////////////////////////////
              // Q2
              //////////////////////////////////////////////////////

              //if (first_bin== second_bin) HISTOGRAMS_1D["multiplicity_"+Noff_name+first_bin]->Fill(PT[first_bin].size());


              /*if (first_bin== second_bin) {

                   double MUL=0;
                   double corr;

                   for (unsigned int i=0; i<PT[first_bin].size(); i++){

                          corr=1.0/(EFF_HISTOS["TABLE"]->GetBinContent(EFF_HISTOS["TABLE"]->FindBin(PT[first_bin][i].eta, PT[first_bin][i].pt)));

                          MUL+=corr;
                   }

              //HISTOGRAMS_1D["multiplicity_eff"+Noff_name+first_bin]->Fill(MUL/10);

              }*/

              /////////////////////////////////////////////////////

     }//LOOP BIN_PAIRS *************

   
     }

     ///////////////////////////////////////////////////


  }
  /*
  else {
      cout << "CIRKOVIC 0" << endl;
      using namespace edm;
      using namespace HepMC;
      hev_.event = iEvent.id().event();
      for(int ieta = 0; ieta < ETABINS; ++ieta){
        hev_.n[ieta] = 0;
        hev_.ptav[ieta] = 0;
      }
      hev_.mult = 0;
      unsigned int cmult = 0;
      double phi0 = 0;
      double b = -1;
      double scale = -1;
      int npart = -1;
      int ncoll = -1;
      int nhard = -1;
      double vx = -99;
      double vy = -99;
      double vz = -99;
      double vr = -99;
      const GenEvent* evt;
      int nmix = -1;
      int np = 0;
      int sig = -1;
      int src = -1;
      if(useHepMCProduct_){
        cout << "CIRKOVIC useHepMCProduct_" << endl;
        if(doCF_){
          cout << "CIRKOVIC doCF_" << endl;
          Handle<CrossingFrame<HepMCProduct> > cf;
          iEvent.getByLabel(InputTag("mix","source"),cf);
          MixCollection<HepMCProduct> mix(cf.product());
          nmix = mix.size();
          cout<<"Mix Collection Size: "<<mix<<endl;
          MixCollection<HepMCProduct>::iterator mbegin = mix.begin();
          MixCollection<HepMCProduct>::iterator mend = mix.end();
          for(MixCollection<HepMCProduct>::iterator mixit = mbegin; mixit != mend; ++mixit){
            const GenEvent* subevt = (*mixit).GetEvent();
            int all = subevt->particles_size();
            np += all;
            HepMC::GenEvent::particle_const_iterator begin = subevt->particles_begin();
            HepMC::GenEvent::particle_const_iterator end = subevt->particles_end();
            for(HepMC::GenEvent::particle_const_iterator it = begin; it != end; ++it){
              if((*it)->status() == 1){
                int pdg_id = (*it)->pdg_id();
                float eta = (*it)->momentum().eta();
                float phi = (*it)->momentum().phi();
                float pt = (*it)->momentum().perp();
                const ParticleData * part = pdt->particle(pdg_id );
                int charge = static_cast<int>(part->charge());
                hev_.pt[hev_.mult] = pt;
                hev_.eta[hev_.mult] = eta;
                hev_.phi[hev_.mult] = phi;
                hev_.pdg[hev_.mult] = pdg_id;
                hev_.chg[hev_.mult] = charge;
                eta = fabs(eta);
                int etabin = 0;
                if(eta > 0.5) etabin = 1;
                if(eta > 1.) etabin = 2;
                if(eta < 2.){
                  hev_.ptav[etabin] += pt;
                  ++(hev_.n[etabin]);
                }
                ++(hev_.mult);
              }
            }
          }
        }else{
          cout << "CIRKOVIC NOT doCF_" << endl;
          Handle<HepMCProduct> mc;
          iEvent.getByLabel(src_,mc);
          evt = mc->GetEvent();
          scale = evt->event_scale();
          const HeavyIon* hi = evt->heavy_ion();

          if(hi){

            b = hi->impact_parameter();
            npart = hi->Npart_proj()+hi->Npart_targ();
            ncoll = hi->Ncoll();
            nhard = hi->Ncoll_hard();
            phi0 = hi->event_plane_angle();
            if(printLists_){
              out_b<<b<<endl;
              out_n<<npart<<endl;
            }
          }
          src = evt->particles_size();
          HepMC::GenEvent::particle_const_iterator begin = evt->particles_begin();
          HepMC::GenEvent::particle_const_iterator end = evt->particles_end();
          for(HepMC::GenEvent::particle_const_iterator it = begin; it != end; ++it){
            if((*it)->status() == 1){

              const ParticleData* part;
              int pdg_id = (*it)->pdg_id();
              float eta = (*it)->momentum().eta();
              float phi = (*it)->momentum().phi();
              float pt = (*it)->momentum().perp();

              float px = (*it)->momentum().px();
              float py = (*it)->momentum().py();
              float pz = (*it)->momentum().pz();
              float e = (*it)->momentum().e();
              float pseudoRapidity = (*it)->momentum().pseudoRapidity();

              if(pdg_id==-130){ //there are not -130 in pdt
        part = pdt->particle(130);
              }else{
        part = pdt->particle(pdg_id);
              }
              int charge = static_cast<int>(part->charge());
              hev_.px[hev_.mult] = px;
              hev_.py[hev_.mult] = py;
              hev_.pz[hev_.mult] = pz;
              hev_.e[hev_.mult] = e;
              hev_.pseudoRapidity[hev_.mult] = pseudoRapidity;
              hev_.pt[hev_.mult] = pt;
              hev_.eta[hev_.mult] = eta;
              hev_.phi[hev_.mult] = phi;
              hev_.pdg[hev_.mult] = pdg_id;
              hev_.chg[hev_.mult] = charge;
              float pneta = eta;
              eta = fabs(eta);
              int etabin = 0;
              if(eta > 0.5) etabin = 1;
              if(eta > 1.) etabin = 2;
              if(eta < 2.){
                hev_.ptav[etabin] += pt;
                ++(hev_.n[etabin]);
              }
              ++(hev_.mult);
              if (charge != 0) {
                hpt->Fill(pt);
                heta->Fill(pneta);
                hphi->Fill(phi);
                hcharge->Fill(charge);
                ++(cmult);
              }
            }
          }
        }
      }else{
        cout << "CIRKOVIC NOT useHepMCProduct_" << endl;
        edm::Handle<reco::GenParticleCollection> parts;
        iEvent.getByLabel(genParticleSrc_,parts);
        for(unsigned int i = 0; i < parts->size(); ++i){
          const reco::GenParticle& p = (*parts)[i];
          hev_.pt[hev_.mult] = p.pt();
          hev_.eta[hev_.mult] = p.eta();
          hev_.phi[hev_.mult] = p.phi();
          hev_.pdg[hev_.mult] = p.pdgId();
          hev_.chg[hev_.mult] = p.charge();
          double eta = fabs(p.eta());
          int etabin = 0;
          if(eta > 0.5) etabin = 1;
          if(eta > 1.) etabin = 2;
          if(eta < 2.){
            hev_.ptav[etabin] += p.pt();
            ++(hev_.n[etabin]);
          }
          ++(hev_.mult);
        }
        if(doHI_){
          edm::Handle<GenHIEvent> higen;
          iEvent.getByLabel(genHIsrc_,higen);
        }
      }
      if(doVertex_){
        edm::Handle<edm::SimVertexContainer> simVertices;
        iEvent.getByLabel<edm::SimVertexContainer>(simVerticesTag_, simVertices);
        if (! simVertices.isValid() ) throw cms::Exception("FatalError") << "No vertices found\n";
        int inum = 0;
        edm::SimVertexContainer::const_iterator it=simVertices->begin();
        SimVertex vertex = (*it);
        cout<<" Vertex position "<< inum <<" " << vertex.position().rho()<<" "<<vertex.position().z()<<endl;
        vx = vertex.position().x();
        vy = vertex.position().y();
        vz = vertex.position().z();
        vr = vertex.position().rho();
      }
      for(int i = 0; i<3; ++i){
        hev_.ptav[i] = hev_.ptav[i]/hev_.n[i];
      }
      hev_.b = b;
      hev_.scale = scale;
      hev_.npart = npart;
      hev_.ncoll = ncoll;
      hev_.nhard = nhard;
      .heS[i]->Write();v_phi0 = phi0;
      hev_.vx = vx;
      hev_.vy = vy;
      hev_.vz = vz;
      hev_.vr = vr;
      nt->Fill(nmix,np,src,sig);
      hydjetTree_->Fill();
      hmult->Fill(cmult);
  }
  */

  if (WR_COUNT == WR_COUNT_DONE - 1) {
      fout = TFile::Open(foutname.c_str(), "RECREATE");
      hevt->Write();
      hpt->Write();
      hfractionS->Write();
      hfractionB->Write();
      heventcountS->Write();
      heventcountB->Write();
      hsum_cosL->Write();
      hsum_cos_normL->Write();
      for (unsigned int i = 0; i < Nbins; i++) {
        Hmult1L[i]->Write();
        //Hmult2L[i]->Write();
        Hpt1L[i]->Write();
        //Hpt2L[i]->Write();
      }
      for (int i = 0; i < nHarr; i++) {
        Hdelta_eta_phiS[i]->Write();
        Hdelta_eta_phiScut[i]->Write();
        Hdelta_eta_phiB[i]->Write();
      }
      for (int i = 0; i < nHarr1; i++) {
        //Hsum_cos[i]->Write();
        Hsum_cosL[i]->Write();
        //Hsum_cos_norm[i]->Write();
        Hsum_cos_normL[i]->Write();
      }
      fout->Close();
      fout = 0;
      WR_COUNT = 0;
  } else
      WR_COUNT++;
  EVT++;
}
// ------------ method called once each job just before starting event loop ------------
void
Hydjet2Analyzer_new_my_502_pt::beginRun(const edm::Run&, const edm::EventSetup& iSetup)
{
  iSetup.getData(pdt);
}
void
Hydjet2Analyzer_new_my_502_pt::beginJob()
{
  if(printLists_){
    out_b.open(fBFileName.c_str());
    if(out_b.good() == false)
      throw cms::Exception("BadFile") << "Can\'t open file " << fBFileName;
    out_n.open(fNFileName.c_str());
    if(out_n.good() == false)
      throw cms::Exception("BadFile") << "Can\'t open file " << fNFileName;
    out_m.open(fMFileName.c_str());
    if(out_m.good() == false)
      throw cms::Exception("BadFile") << "Can\'t open file " << fMFileName;
  }
  /*
  if(doAnalysis_){
    nt = f->make<TNtuple>("nt","Mixing Analysis","mix:np:src:sig");
    hydjetTree_ = f->make<TTree>("hi","Tree of Hydjet Events");
    hydjetTree_->Branch("event",&hev_.event,"event/I");
    hydjetTree_->Branch("b",&hev_.b,"b/F");
    hydjetTree_->Branch("npart",&hev_.npart,"npart/F");
    hydjetTree_->Branch("ncoll",&hev_.ncoll,"ncoll/F");
    hydjetTree_->Branch("nhard",&hev_.nhard,"nhard/F");
    hydjetTree_->Branch("phi0",&hev_.phi0,"phi0/F");
    hydjetTree_->Branch("scale",&hev_.scale,"scale/F");
    hydjetTree_->Branch("n",hev_.n,"n[3]/I");
    hydjetTree_->Branch("ptav",hev_.ptav,"ptav[3]/F");
    if(doParticles_){
      hydjetTree_->Branch("mult",&hev_.mult,"mult/I");
      hydjetTree_->Branch("px",hev_.px,"px[mult]/F");
      hydjetTree_->Branch("py",hev_.py,"py[mult]/F");
      hydjetTree_->Branch("pz",hev_.pz,"pz[mult]/F");
      hydjetTree_->Branch("e",hev_.e,"e[mult]/F");
      hydjetTree_->Branch("pseudoRapidity",hev_.pseudoRapidity,"pseudoRapidity[mult]/F");
      hydjetTree_->Branch("pt",hev_.pt,"pt[mult]/F");
      hydjetTree_->Branch("eta",hev_.eta,"eta[mult]/F");
      hydjetTree_->Branch("phi",hev_.phi,"phi[mult]/F");
      hydjetTree_->Branch("pdg",hev_.pdg,"pdg[mult]/I");
      hydjetTree_->Branch("chg",hev_.chg,"chg[mult]/I");
      hydjetTree_->Branch("vx",&hev_.vx,"vx/F");
      hydjetTree_->Branch("vy",&hev_.vy,"vy/F");
      hydjetTree_->Branch("vz",&hev_.vz,"vz/F");
      hydjetTree_->Branch("vr",&hev_.vr,"vr/F");
    }
  }
  */
  //hevt = new TH1F("hevt", "hevt", 100, -0.5, 99.5);
  hevt = new TH1F("hevt", "hevt", 1000, -0.5, 999.5);
  hpt = new TH1F("hpt", "hpt", 100, 0.0, 10.0);
  hmult1L = new TH1F("hmult1L", "hmult1L", 4000, 0.0, 4000);
  //hmult2L = new TH1F("hmult2L", "hmult2L", 4000, 0.0, 4000);
  hpt1L = new TH1F("hpt1L", "hpt1L", 4000, 0.0, 15.0);
  //hpt2L = new TH1F("hpt2L", "hpt2L", 4000, 0.0, 15.0);
  hsum_cosL = new TH1F("hsum_cosL", "hsum_cosL", 2000, -2000.0, 2000.0);
  hsum_cos_normL = new TH1F("hsum_cos_normL", "hsum_cos_normL", 2000, -1.0, 1.0);
  hdelta_eta_phi = new TH2F("hdelta_eta_phi", "hdelta_eta_phi", 100, -4.8, 4.8, 100, -TMath::Pi()/2, 3*TMath::Pi()/2);
  hfractionS = new TH2F("pair_fraction_S", "pair_fraction_S", 15, 0.5, 15.5, 15, 0.5, 15.5);
  hfractionB = new TH2F("pair_fraction_B", "pair_fraction_B", 15, 0.5, 15.5, 15, 0.5, 15.5);
  heventcountS = new TH2F("event_count_S", "event_count_S", 15, 0.5, 15.5, 15, 0.5, 15.5);
  heventcountB = new TH2F("event_count_B", "event_count_B", 15, 0.5, 15.5, 15, 0.5, 15.5);

  hevt->StatOverflows(true);
  hpt->StatOverflows(true);
  hmult1L->StatOverflows(true);
  //hmult2L->StatOverflows(true);
  hpt1L->StatOverflows(true);
  //hpt2L->StatOverflows(true);
  hsum_cosL->StatOverflows(true);
  hsum_cos_normL->StatOverflows(true);
  hdelta_eta_phi->StatOverflows(true);
  hfractionS->StatOverflows(true);
  hfractionB->StatOverflows(true);
  heventcountS->StatOverflows(true);
  heventcountB->StatOverflows(true);

  Hmult1L = new TH1F*[Nbins];
  //Hmult2L = new TH1F*[Nbins];
  Hpt1L = new TH1F*[Nbins];
  //Hpt2L = new TH1F*[Nbins];
  Hdelta_eta_phiS = new TH2F*[nHarr];
  Hdelta_eta_phiScut = new TH2F*[nHarr];
  Hdelta_eta_phiB = new TH2F*[nHarr];
  Hsum_cosL = new TH1F*[nHarr1];
  Hsum_cos_normL = new TH1F*[nHarr1];
  const char *newname;
  for (unsigned int i = 0; i < Nbins; i++) {
    Hmult1L[i] = new TH1F(*hmult1L);
    newname = (string(Hmult1L[i]->GetName())+to_string(i)).c_str();
    Hmult1L[i]->SetName(newname); Hmult1L[i]->SetTitle(newname);
    //Hmult2L[i] = new TH1F(*hmult2L);
    //newname = (string(Hmult2L[i]->GetName())+to_string(i)).c_str();
    //Hmult2L[i]->SetName(newname); Hmult2L[i]->SetTitle(newname);
    Hpt1L[i] = new TH1F(*hpt1L);
    newname = (string(Hpt1L[i]->GetName())+to_string(i)).c_str();
    Hpt1L[i]->SetName(newname); Hpt1L[i]->SetTitle(newname);
    //Hpt2L[i] = new TH1F(*hpt2L);
    //newname = (string(Hpt2L[i]->GetName())+to_string(i)).c_str();
    //Hpt2L[i]->SetName(newname); Hpt2L[i]->SetTitle(newname);
  }
  for (int i = 0; i < nHarr; i++) {
    Hdelta_eta_phiS[i] = new TH2F(*hdelta_eta_phi);
    newname = (string(Hdelta_eta_phiS[i]->GetName())+string("S")+to_string(i)).c_str();
    Hdelta_eta_phiS[i]->SetName(newname); Hdelta_eta_phiS[i]->SetTitle(newname);
    Hdelta_eta_phiScut[i] = new TH2F(*hdelta_eta_phi);
    newname = (string(Hdelta_eta_phiScut[i]->GetName())+string("Scut")+to_string(i)).c_str();
    Hdelta_eta_phiScut[i]->SetName(newname); Hdelta_eta_phiScut[i]->SetTitle(newname);
    Hdelta_eta_phiB[i] = new TH2F(*hdelta_eta_phi);
    newname = (string(Hdelta_eta_phiB[i]->GetName())+string("B")+to_string(i)).c_str();
    Hdelta_eta_phiB[i]->SetName(newname); Hdelta_eta_phiB[i]->SetTitle(newname);
  }
  for (int i = 0; i < nHarr1; i++) {
    Hsum_cosL[i] = new TH1F(*hsum_cosL);
    newname = (string(Hsum_cosL[i]->GetName())+to_string(i)).c_str();
    Hsum_cosL[i]->SetName(newname); Hsum_cosL[i]->SetTitle(newname);
    Hsum_cos_normL[i] = new TH1F(*hsum_cos_normL);
    newname = (string(Hsum_cos_normL[i]->GetName())+to_string(i)).c_str();
    Hsum_cos_normL[i]->SetName(newname); Hsum_cos_normL[i]->SetTitle(newname);
  }
}

void Hydjet2Analyzer_new_my_502_pt:: DO_BACKGROUND2(EVENT* EVENTS, vector<pair<int, int>> PAIRS, string Noff){

     int t1;
     int t2;

     for (unsigned int pair=0; pair<PAIRS.size(); pair++){

            t1=PAIRS[pair].first;
            t2=PAIRS[pair].second;

            //cout << "CIRKOVIC: " << t1 << " " << t2 << endl;


            if (t1!=t2) CORRELATION_OF_MIXED_EVENTS(EVENTS[t1].PT, EVENTS[t2].PT, Noff);

      }//FOR LOOP

}

void Hydjet2Analyzer_new_my_502_pt:: CORRELATION_OF_MIXED_EVENTS(map<string, vector<TRIPLET>> PT_FIXED, map<string, vector<TRIPLET>> PT_CURRENT, string Noff_name){

      double ENTRY;
      //double ENTRY_EFF;
      double TotalPairs;
      //double TotalPairs_EFF;
      double fraction;
      //double fraction_eff;

      //double sum_cos_n2;
      //double sum_cos_n3;

      //double sum_cos_n2_eff;
      //double sum_cos_n3_eff;

      double delta_phi;
      double delta_eta;

      string first_bin;
      string second_bin;

      //double corr1=0;
      //double corr2=0;
      //double corr=0;

      for (unsigned int bin_pair=0; bin_pair<BIN_PAIRS.size(); bin_pair++){//BIN COMBINATIONS

                       first_bin=BIN_PAIRS[bin_pair].first;
                       second_bin=BIN_PAIRS[bin_pair].second;
     
                       if (PT_FIXED[first_bin].empty()==true) continue;
                       if (PT_CURRENT[second_bin].empty()==true) continue;

                       ENTRY=0;
                       //ENTRY_EFF=0;
                       TotalPairs=0;
                       //TotalPairs_EFF=0;

                       //sum_cos_n2=0;
                       //sum_cos_n3=0;

                       //sum_cos_n2_eff=0;
                       //sum_cos_n3_eff=0;

                       for (unsigned int i=0; i<PT_FIXED[first_bin].size(); i++){

                           for (unsigned int j=0; j<PT_CURRENT[second_bin].size(); j++){
                                   
                                   delta_phi=PT_FIXED[first_bin][i].phi - PT_CURRENT[second_bin][j].phi;
                                   delta_eta=PT_FIXED[first_bin][i].eta - PT_CURRENT[second_bin][j].eta;

                                   if (fabs(delta_eta) == 0) continue;//this will exclude pure autocorrelations

                                   double delta_phi1 = delta_phi;
                                   if (delta_phi1<-0.5*TMath::Pi()) delta_phi1=delta_phi1+2*TMath::Pi();
                                   if (delta_phi1>1.5*TMath::Pi()) delta_phi1=delta_phi1-2*TMath::Pi();

                                   Hdelta_eta_phiB[bin_pair]->Fill(delta_eta, delta_phi1);

                                   TotalPairs++;

                                   /*

                                   corr1=1.0/(EFF_HISTOS["TABLE"]->GetBinContent(EFF_HISTOS["TABLE"]->FindBin(PT_FIXED[first_bin][i].eta, PT_FIXED[first_bin][i].pt)));
                                   corr2=1.0/(EFF_HISTOS["TABLE"]->GetBinContent(EFF_HISTOS["TABLE"]->FindBin(PT_CURRENT[second_bin][j].eta, PT_CURRENT[second_bin][j].pt)));

                                   corr=corr1*corr2;

                                   TotalPairs_EFF+=corr;
                                   */
 
                                   if (fabs(delta_eta)<2) continue;//this will exclude autocorr. by def.

                                   /////////////////////////////////////// efficiency
                                   
                                   ENTRY+=1;
                                   /*
                                   ENTRY_EFF+=corr;

                                   sum_cos_n2+=cos(2*(delta_phi));
                                   sum_cos_n3+=cos(3*(delta_phi));

                                   sum_cos_n2_eff+=corr*cos(2*(delta_phi));
                                   sum_cos_n3_eff+=corr*cos(3*(delta_phi));
                                   */
                           }//PTi

                       }//PTj
       
                        if (ENTRY!=0){     // there is an event with non-zero entry for comb. (pi, pj)

                              fraction=ENTRY/TotalPairs;
                              /*
                              fraction_eff=ENTRY_EFF/TotalPairs_EFF;

                              HISTOGRAMS_1D["CORR_BACK"+ Noff_name + first_bin + second_bin]->Fill(ENTRY_EFF/ENTRY);

                              HISTOGRAMS_2D["EVENT_COUNT_BACK"+Noff_name]->Fill(BIN_PAIRS2[bin_pair].first, BIN_PAIRS2[bin_pair].second, 1);// EVENTS TAKEN INTO ACCOUNT
                              HISTOGRAMS_2D["PAIR_FRACTION_BACK"+Noff_name]->Fill(BIN_PAIRS2[bin_pair].first, BIN_PAIRS2[bin_pair].second, fraction);//
                              HISTOGRAMS_2D["PAIR_FRACTION_BACK_EFF"+Noff_name]->Fill(BIN_PAIRS2[bin_pair].first, BIN_PAIRS2[bin_pair].second, fraction_eff);//

                              HISTOGRAMS_1D["cos_normed_back" +Noff_name+"_n2" + first_bin + second_bin]->Fill(sum_cos_n2/ENTRY);
                              HISTOGRAMS_1D["cos_normed_back" +Noff_name+"_n3" + first_bin + second_bin]->Fill(sum_cos_n3/ENTRY);

                              HISTOGRAMS_1D["cos_normed_back_eff" +Noff_name+"_n2" + first_bin + second_bin]->Fill(sum_cos_n2_eff/ENTRY_EFF);
                              HISTOGRAMS_1D["cos_normed_back_eff" +Noff_name+"_n3" + first_bin + second_bin]->Fill(sum_cos_n3_eff/ENTRY_EFF);

                              HISTOGRAMS_1D["cos_not_normed_back" +Noff_name+"_n2" + first_bin + second_bin]->Fill(sum_cos_n2/50);
                              HISTOGRAMS_1D["cos_not_normed_back" +Noff_name+"_n3" + first_bin + second_bin]->Fill(sum_cos_n3/50);

                              HISTOGRAMS_1D["cos_not_normed_back_eff" +Noff_name+"_n2" + first_bin + second_bin]->Fill(sum_cos_n2_eff/50);
                              HISTOGRAMS_1D["cos_not_normed_back_eff" +Noff_name+"_n3" + first_bin + second_bin]->Fill(sum_cos_n3_eff/50);

                              HISTOGRAMS_1D["pairs_with_cut_back"+Noff_name+"_n0" + first_bin + second_bin]->Fill(ENTRY/1000);
                              HISTOGRAMS_1D["pairs_with_cut_eff_back"+Noff_name+"_n0" + first_bin + second_bin]->Fill(ENTRY_EFF/2000);
                              HISTOGRAMS_1D["pairs_total_back"+Noff_name+"_n0" + first_bin + second_bin]->Fill(TotalPairs/1000);
                              HISTOGRAMS_1D["pairs_total_eff_back"+Noff_name+"_n0" + first_bin + second_bin]->Fill(TotalPairs_EFF/5000);
                              */
                              hfractionB->Fill(BIN_PAIRS2[bin_pair].first, BIN_PAIRS2[bin_pair].second, fraction);
                              heventcountB->Fill(BIN_PAIRS2[bin_pair].first, BIN_PAIRS2[bin_pair].second, 1);
                        }

        }//LOOP BIN_PAIRS


}//END CORRELATION


// ------------ method called once each job just after ending the event loop ------------
void
Hydjet2Analyzer_new_my_502_pt::endJob() {
}
//define this as a plug-in
DEFINE_FWK_MODULE(Hydjet2Analyzer_new_my_502_pt);
