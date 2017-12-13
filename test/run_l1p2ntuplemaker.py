
import FWCore.ParameterSet.Config as cms
process = cms.Process("USER")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.Services_cff') 
process.load("Configuration.Geometry.GeometryRecoDB_cff")

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

print "MC Sample will be taken as input"
inputFiles='root://cms-xrd-global.cern.ch//store/mc/PhaseIISpring17D/SingleNeutrino/GEN-SIM-DIGI-RAW/PU140_90X_upgrade2023_realistic_v9-v1/70003/FCEF8065-BC28-E711-A891-0242AC130002.root'

process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (inputFiles)
)

# Output file
process.TFileService = cms.Service("TFileService",
   fileName = cms.string("L1P2NtupleMaker_output.root")
)

process.load("L1TriggerDPG.L1PhaseIIStudies.L1P2NtupleMaker_cfi")

#Load the L1 kalman muon emulation
from L1TriggerDPG.L1PhaseIIStudies.KalmanMuonEmulation_cfi import *
KalmanMuEmulation(process)

process.seq = cms.Path(process.simTwinMuxDigis * process.simBmtfDigis * process.l1KalmanMuons * process.L1P2NtupleMaker)
process.schedule = cms.Schedule(process.seq)

#process.out = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string('singleNeutrino140.root')
#)
#process.seq = cms.Path(process.simTwinMuxDigis * process.simBmtfDigis * process.l1KalmanMuons)
#process.e = cms.EndPath(process.out)
#process.schedule = cms.Schedule(process.seq,process.e)
