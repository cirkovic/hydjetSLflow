import FWCore.ParameterSet.Config as cms
process = cms.Process("TEST")
process.source = cms.Source("EmptySource")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.options.numberOfThreads = cms.untracked.uint32(8)
#process.maxEvents = cms.untracked.PSet(
#    input = cms.untracked.int32(1)
#)
