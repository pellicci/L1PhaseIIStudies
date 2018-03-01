from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.workArea = 'crab_projects/180221_kalmanPlusGmtPlusBmtf/'

config.section_('JobType')
config.JobType.psetName = 'run_l1p2ntuplemaker.py'
config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = ['L1P2NtupleMaker_output.root']

config.section_('Data')
config.Data.splitting = 'FileBased'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False

config.section_('Site')
config.Site.storageSite = 'T2_IT_Legnaro'

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    from multiprocessing import Process

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    config.General.requestName = 'P1P2NtupleMaker_SingleNu140'
    config.Data.unitsPerJob = 10
    config.Data.inputDataset = '/SingleNeutrino/PhaseIISpring17D-PU140_90X_upgrade2023_realistic_v9-v1/GEN-SIM-DIGI-RAW'
    p140 = Process(target=submit, args=(config,))
    p140.start()
    p140.join()

    config.Site.ignoreGlobalBlacklist = False

    config.General.requestName = 'P1P2NtupleMaker_SingleNu200'
    config.Data.unitsPerJob = 10
    config.Data.inputDataset = '/SingleNeutrino/PhaseIISpring17D-PU200_90X_upgrade2023_realistic_v9-v1/GEN-SIM-DIGI-RAW'
    p200 = Process(target=submit, args=(config,))
    p200.start()
    p200.join()

    config.Site.ignoreGlobalBlacklist = True

    config.General.requestName = 'P1P2NtupleMaker_DYJetsToLL140'
    config.Data.unitsPerJob = 10
    config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_ext1/PhaseIISpring17D-PU140_100M_90X_upgrade2023_realistic_v9-v1/GEN-SIM-DIGI-RAW'
    pDY140 = Process(target=submit, args=(config,))
    pDY140.start()
    pDY140.join()

    config.General.requestName = 'P1P2NtupleMaker_DYJetsToLL200'
    config.Data.unitsPerJob = 10
    config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_ext1/PhaseIISpring17D-PU200_100M_90X_upgrade2023_realistic_v9-v1/GEN-SIM-DIGI-RAW'
    pDY200 = Process(target=submit, args=(config,))
    pDY200.start()
    pDY200.join()
