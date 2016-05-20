#include "TROOT.h"
#include "TFile.h"
#include "TH1F.h"
#include<iostream>

using namespace std;
 
int main(int argc, char **argv) {
    TFile *f = TFile::Open(argv[1]);
    TH1F *h = (TH1F*)f->Get("hevt");
    cout << (int)h->Integral() << endl;
    return 0;
}
