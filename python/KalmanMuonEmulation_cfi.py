import FWCore.ParameterSet.Config as cms

def KalmanMuEmulation(process):

    
    process.load('L1Trigger.L1KalmanMuonTrackFinder.l1KalmanMuons_cff')

    ##Stage 2 BMTF emulator####

    ##Emulator Parameter
    process.load('L1Trigger.L1TMuonBarrel.fakeBmtfParams_cff')
    process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
                                    toGet = cms.VPSet(
            cms.PSet(record = cms.string('L1TMuonBarrelParamsRcd'),
                     data = cms.vstring('L1TMuonBarrelParams'))
            ),
                                    verbose = cms.untracked.bool(True)
                                    )

    process.fakeBmtfParams.fwVersion = cms.uint32(2)
    ##process.fakeBmtfParams.EtaTrackFinder = cms.bool(False)
    process.fakeBmtfParams.BX_max = cms.int32(2)
    process.fakeBmtfParams.BX_min = cms.int32(-2)

    ##enable stations here-each digit corresponds to a sector
    maskenable      = '000000000000'
    maskdisable     = '111111111111'

    process.fakeBmtfParams.mask_phtf_st1        = cms.vstring(maskdisable, maskenable, maskenable, maskenable, maskenable, maskenable, maskdisable)
    process.fakeBmtfParams.mask_phtf_st2        = cms.vstring(maskenable,  maskenable, maskenable, maskenable, maskenable, maskenable, maskenable)
    process.fakeBmtfParams.mask_phtf_st3        = cms.vstring(maskenable,  maskenable, maskenable, maskenable, maskenable, maskenable, maskenable)
    process.fakeBmtfParams.mask_phtf_st4        = cms.vstring(maskenable,  maskenable, maskenable, maskenable, maskenable, maskenable, maskenable)

    process.fakeBmtfParams.mask_ettf_st1        = cms.vstring(maskdisable, maskenable, maskenable, maskenable, maskenable, maskenable, maskdisable)
    process.fakeBmtfParams.mask_ettf_st2        = cms.vstring(maskenable,  maskenable, maskenable, maskenable, maskenable, maskenable, maskenable)
    process.fakeBmtfParams.mask_ettf_st3        = cms.vstring(maskenable,  maskenable, maskenable, maskenable, maskenable, maskenable, maskenable)

    ####BMTF Emulator is loaded here
    process.load('L1Trigger.L1TMuonBarrel.simTwinMuxDigis_cfi')
    process.load('L1Trigger.L1TMuonBarrel.simBmtfDigis_cfi')
    process.simBmtfDigis.Debug = cms.untracked.int32(0)
    process.simBmtfDigis.DTDigi_Source = cms.InputTag("simDtTriggerPrimitiveDigis")
    process.simBmtfDigis.DTDigi_Theta_Source = cms.InputTag("simDtTriggerPrimitiveDigis")
