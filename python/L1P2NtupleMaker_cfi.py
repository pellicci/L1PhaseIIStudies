import FWCore.ParameterSet.Config as cms

L1P2NtupleMaker = cms.EDAnalyzer('L1P2NtupleMaker',
                                  L1standMuCandidates    = cms.InputTag("l1KalmanMuonTracks:Cleaned"),
                                  L1standMuAllCandidates = cms.InputTag("l1KalmanMuonTracks:All"),
                                  L1GmtCandidates        = cms.InputTag("simGmtStage2Digis"),
                                  L1BmtfStdCandidates    = cms.InputTag("simBmtfDigis:BMTF:HLT"),
                                  L1BmtfCandidates       = cms.InputTag("simBmtfDigis:BMTF:USER"),
                                 )

