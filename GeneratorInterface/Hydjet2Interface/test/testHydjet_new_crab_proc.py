import FWCore.ParameterSet.Config as cms

import sys
#print sys.argv

from GeneratorInterface.Hydjet2Interface.offset_proc import *

import random
from datetime import datetime
random.seed(datetime.now())

process = cms.Process("ANA")

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("Configuration.StandardSequences.Services_cff")
process.load("GeneratorInterface.Hydjet2Interface.hydjet2Default_cfi_n_crab")

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
	generator = cms.PSet(
		initialSeed = cms.untracked.uint32(random.randint(0,123456789)),
		engineName = cms.untracked.string('HepJamesRandom')
	)
)

Nevt = int(sys.argv[offset+INEVT])

process.maxEvents = cms.untracked.PSet(
    #input = cms.untracked.int32(-1)
    #input = cms.untracked.int32(2)
    #input = cms.untracked.int32(100)
    #input = cms.untracked.int32(1000)
    input = cms.untracked.int32(Nevt)
)

#process.ana = cms.EDAnalyzer('Hydjet2Analyzer',
process.ana = cms.EDAnalyzer('Hydjet2Analyzer_new',
    foutName = cms.untracked.string('output_'+'_'.join(argv)+'.root'),
    HepMCProductLabel = cms.string('Hydjet2Analyzer_new'),

       deltaEtaCut=cms.untracked.double(sys.argv[offset+IDETC]),

       Nbins=cms.int32(7),
       #Nbins=cms.int32(3),
       track_cut=cms.bool(False),  #no track suppresion

       DO_SIGNAL=cms.bool(True),  #no signal calculation
       DO_BACKGROUND=cms.bool(True),  #no signal calculation

       DO_DIAG=cms.bool(True),  #no signal calculation
       DO_NONDIAG=cms.bool(True),  #no signal calculation

       #table_name=cms.string("./TrackCorrections_HYDJET_5320_hiGenPixelTrk_cent1030.root"),

       P1=cms.PSet( min=cms.double(0.3), max=cms.double(0.5)),
       P2=cms.PSet( min=cms.double(0.5), max=cms.double(0.75)),
       P3=cms.PSet( min=cms.double(0.75), max=cms.double(1.0)),
       P4=cms.PSet( min=cms.double(1.0), max=cms.double(1.5)),
       P5=cms.PSet( min=cms.double(1.5), max=cms.double(2.0)),
       P6=cms.PSet( min=cms.double(2.0), max=cms.double(2.5)),
       P7=cms.PSet( min=cms.double(2.5), max=cms.double(3.0)),
       #P8=cms.PSet( min=cms.double(3.0), max=cms.double(4.0)),
       #P9=cms.PSet( min=cms.double(4.0), max=cms.double(5.0)),
       #P10=cms.PSet( min=cms.double(5.0), max=cms.double(6.0)),


       #CentralityClasses = cms.VPSet(
       #
       # cms.PSet( Bin_min=cms.int32(0), Bin_max=cms.int32(0), switch=cms.bool(sys.argv[offset+3] == "0-02"), name=cms.string("0_02")),
       # cms.PSet( Bin_min=cms.int32(0), Bin_max=cms.int32(1), switch=cms.bool(sys.argv[offset+3] == "0-05"), name=cms.string("0_05")),
       # cms.PSet( Bin_min=cms.int32(0), Bin_max=cms.int32(9), switch=cms.bool(sys.argv[offset+3] == "0-5"), name=cms.string("0_5")),
       # cms.PSet( Bin_min=cms.int32(10), Bin_max=cms.int32(19), switch=cms.bool(sys.argv[offset+3] == "5-10"), name=cms.string("5_10")),
       # cms.PSet( Bin_min=cms.int32(0), Bin_max=cms.int32(19), switch=cms.bool(sys.argv[offset+3] == "0-10"), name=cms.string("0_10")),
       # cms.PSet( Bin_min=cms.int32(20), Bin_max=cms.int32(39), switch=cms.bool(sys.argv[offset+3] == "10-20"), name=cms.string("10_20")),
       # cms.PSet( Bin_min=cms.int32(40), Bin_max=cms.int32(59), switch=cms.bool(sys.argv[offset+3] == "20-30"), name=cms.string("20_30")),
       # cms.PSet( Bin_min=cms.int32(60), Bin_max=cms.int32(79), switch=cms.bool(sys.argv[offset+3] == "30-40"), name=cms.string("30_40")),
       # cms.PSet( Bin_min=cms.int32(80), Bin_max=cms.int32(99), switch=cms.bool(sys.argv[offset+3] == "40-50"), name=cms.string("40_50")),
       # cms.PSet( Bin_min=cms.int32(100), Bin_max=cms.int32(119), switch=cms.bool(sys.argv[offset+3] == "50-60"), name=cms.string("50_60")),
       #
       #                             ),

        DegreeClass= cms.VPSet(

       # cms.PSet( n_type= cms.int32(0), switch=cms.bool(True), name=cms.string("0")),
        cms.PSet( n_type= cms.int32(2), switch=cms.bool(True),  name=cms.string("2")),
        cms.PSet( n_type= cms.int32(3), switch=cms.bool(True), name=cms.string("3")),

                              )


)

process.p = cms.Path(process.generator*process.ana)

#process.output = cms.OutputModule("PoolOutputModule",
    #outputCommands = cms.untracked.vstring("drop *", "keep recoTracks_*_*_*"),
    #fileName = cms.untracked.string('output.root'),
#    fileName = cms.untracked.string('output_'+'_'.join(argv)+'.root'),
#)

import multiprocessing

nproc = multiprocessing.cpu_count()

process.options = cms.untracked.PSet(
    multiProcesses = cms.untracked.PSet(
        maxChildProcesses                       = cms.untracked.int32( nproc ),
        maxSequentialEventsPerChild             = cms.untracked.uint32( 2 ),
        #setCpuAffinity                          = cms.untracked.bool( False ),
        continueAfterChildFailure               = cms.untracked.bool( True ),
        #eventSetupDataToExcludeFromPrefetching  = cms.untracked.PSet( )
    )
)

