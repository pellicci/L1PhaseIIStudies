import FWCore.ParameterSet.Config as cms

L1P2NtupleMaker = cms.EDAnalyzer('L1P2NtupleMaker',
                                  L1standMuCandidates = cms.InputTag("l1KalmanMuonTracks:Cleaned"),
                                 )
