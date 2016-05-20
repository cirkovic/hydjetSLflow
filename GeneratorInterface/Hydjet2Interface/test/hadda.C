//macro to add histogram files
//NOTE: This macro is kept for back compatibility only.
//Use instead the executable $ROOTSYS/bin/hadd
//
//This macro will add histograms from a list of root files and write them
//to a target root file. The target file is newly created and must not be
//identical to one of the source files.
//
//Author: Sven A. Schmidt, sven.schmidt@cern.ch
//Date:   13.2.2001

//This code is based on the hadd.C example by Rene Brun and Dirk Geppert,
//which had a problem with directories more than one level deep.
//(see macro hadd_old.C for this previous implementation).
//
//The macro from Sven has been enhanced by
//   Anne-Sylvie Nicollerat <Anne-Sylvie.Nicollerat@cern.ch>
// to automatically add Trees (via a chain of trees).
//
//To use this macro, modify the file names in function hadd.
//
//NB: This macro is provided as a tutorial.
//    Use $ROOTSYS/bin/hadd to merge many histogram files



#include <string.h>
#include "TChain.h"
#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "TKey.h"
#include "Riostream.h"

TList *FileList;
TFile *Target;

void MergeRootfile( TDirectory *target, TList *sourcelist );


void hadd() {
   // Prepare the files to me merged
   /*
   if(gSystem->AccessPathName("hsimple1.root")) {
     gSystem->CopyFile("hsimple.root", "hsimple1.root");
     gSystem->CopyFile("hsimple.root", "hsimple2.root");
   }
   */

   // in an interactive ROOT session, edit the file names
   // Target and FileList, then
   // root > .L hadd.C
   // root > hadd()

   Target = TFile::Open( "result.root", "RECREATE" );

   FileList = new TList();
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3179.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3174.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3173.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3088.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3082.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3095.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3090.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3073.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3038.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3042.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3011.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3021.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3019.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0003/output_4000_2_40-50_2.0_3004.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2976.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2972.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2969.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2968.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2961.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2966.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2958.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2965.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2957.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2954.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2950.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2962.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2936.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2929.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2914.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2912.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2859.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2871.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2883.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2876.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2872.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2863.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2852.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2843.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2842.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2760.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2762.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2750.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2741.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2756.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2706.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2712.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2694.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2692.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2695.root") );
   FileList->Add( TFile::Open("root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/crab_20160724_144137/160724_124144/0002/output_4000_2_40-50_2.0_2686.root") );

   MergeRootfile( Target, FileList );

}

void MergeRootfile( TDirectory *target, TList *sourcelist ) {

   //  cout << "Target path: " << target->GetPath() << endl;
   TString path( (char*)strstr( target->GetPath(), ":" ) );
   path.Remove( 0, 2 );

   TFile *first_source = (TFile*)sourcelist->First();
   first_source->cd( path );
   TDirectory *current_sourcedir = gDirectory;
   //gain time, do not add the objects in the list in memory
   Bool_t status = TH1::AddDirectoryStatus();
   TH1::AddDirectory(kFALSE);

   // loop over all keys in this directory
   TChain *globChain = 0;
   TIter nextkey( current_sourcedir->GetListOfKeys() );
   TKey *key, *oldkey=0;
   while ( (key = (TKey*)nextkey())) {

      //keep only the highest cycle number for each key
      if (oldkey && !strcmp(oldkey->GetName(),key->GetName())) continue;

      // read object from first source file
      first_source->cd( path );
      TObject *obj = key->ReadObj();

      if ( obj->IsA()->InheritsFrom( TH1::Class() ) ) {
         // descendant of TH1 -> merge it

         //      cout << "Merging histogram " << obj->GetName() << endl;
         TH1 *h1 = (TH1*)obj;

         // loop over all source files and add the content of the
         // correspondant histogram to the one pointed to by "h1"
         TFile *nextsource = (TFile*)sourcelist->After( first_source );
         while ( nextsource ) {

            // make sure we are at the correct directory level by cd'ing to path
            nextsource->cd( path );
            TKey *key2 = (TKey*)gDirectory->GetListOfKeys()->FindObject(h1->GetName());
            if (key2) {
               TH1 *h2 = (TH1*)key2->ReadObj();
               h1->Add( h2 );
               delete h2;
            }

            nextsource = (TFile*)sourcelist->After( nextsource );
         }
      }
      else if ( obj->IsA()->InheritsFrom( TTree::Class() ) ) {

         // loop over all source files create a chain of Trees "globChain"
         const char* obj_name= obj->GetName();

         globChain = new TChain(obj_name);
         globChain->Add(first_source->GetName());
         TFile *nextsource = (TFile*)sourcelist->After( first_source );
         //      const char* file_name = nextsource->GetName();
         // cout << "file name  " << file_name << endl;
         while ( nextsource ) {

            globChain->Add(nextsource->GetName());
            nextsource = (TFile*)sourcelist->After( nextsource );
         }

      } else if ( obj->IsA()->InheritsFrom( TDirectory::Class() ) ) {
         // it's a subdirectory

         cout << "Found subdirectory " << obj->GetName() << endl;

         // create a new subdir of same name and title in the target file
         target->cd();
         TDirectory *newdir = target->mkdir( obj->GetName(), obj->GetTitle() );

         // newdir is now the starting point of another round of merging
         // newdir still knows its depth within the target file via
         // GetPath(), so we can still figure out where we are in the recursion
         MergeRootfile( newdir, sourcelist );

      } else {

         // object is of no type that we know or can handle
         cout << "Unknown object type, name: "
         << obj->GetName() << " title: " << obj->GetTitle() << endl;
      }

      // now write the merged histogram (which is "in" obj) to the target file
      // note that this will just store obj in the current directory level,
      // which is not persistent until the complete directory itself is stored
      // by "target->Write()" below
      if ( obj ) {
         target->cd();

         //!!if the object is a tree, it is stored in globChain...
         if(obj->IsA()->InheritsFrom( TTree::Class() ))
            globChain->Merge(target->GetFile(),0,"keep");
         else
            obj->Write( key->GetName() );
      }

   } // while ( ( TKey *key = (TKey*)nextkey() ) )

   // save modifications to target file
   target->SaveSelf(kTRUE);
   TH1::AddDirectory(status);
}
