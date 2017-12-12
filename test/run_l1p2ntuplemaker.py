
import FWCore.ParameterSet.Config as cms
process = cms.Process("USER")

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.Services_cff') 
from Configuration.AlCa.GlobalTag import GlobalTag

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)


process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')
print "MC Sample will be taken as input for check up of the code working "
inputFiles='root://cms-xrd-global.cern.ch//store/user/pellicci/WPiGamma_GENSIM_80XV1/WPiGamma_MINIAODSIM_80XV1/161214_125251/0000/WPiGamma_pythia8_MINIAOD_1.root'

process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (inputFiles)
)

# Output file
process.TFileService = cms.Service("TFileService",
   fileName = cms.string("L1P2NtupleMaker_output.root")
)

process.load("L1TriggerDPG.L1PhaseIIStudies.L1P2NtupleMaker_cfi")

process.seq = cms.Path(process.L1P2NtupleMaker)

process.schedule = cms.Schedule(process.seq)
