
//ROOT includes
#include "TTree.h"
#include "TMath.h"

//CMSSW includes
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
 
#include "DataFormats/L1KalmanMuonTrigger/interface/L1KalmanMuTrack.h"
#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/L1TMuon/interface/RegionalMuonCand.h"

#include "L1P2NtupleMaker.h"

using namespace::std;
 
// constructors and destructor
L1P2NtupleMaker::L1P2NtupleMaker(const edm::ParameterSet& iConfig) :
  L1standMuCandidates_(iConfig.getParameter<edm::InputTag>("L1standMuCandidates")),
  L1GmtCandidates_(iConfig.getParameter<edm::InputTag>("L1GmtCandidates")),
  L1BmtfCandidates_(iConfig.getParameter<edm::InputTag>("L1BmtfCandidates"))
{
  L1standMuCandidatesToken_ = consumes<vector<L1KalmanMuTrack> >(L1standMuCandidates_); 
  L1GmtCandidatesToken_     = consumes<BXVector<l1t::Muon> >(L1GmtCandidates_);
  L1BmtfCandidatesToken_    = consumes<BXVector<l1t::RegionalMuonCand> >(L1BmtfCandidates_);

  mytree = fs->make<TTree>("mytree", "Tree containing L1 info");

  mytree->Branch("standMu_pT", &standMu_pT_tree);
  mytree->Branch("standMu_eta",&standMu_eta_tree);
  mytree->Branch("standMu_phi",&standMu_phi_tree);

  mytree->Branch("gmtMu_pT", &gmtMu_pT_tree); 
  mytree->Branch("gmtMu_eta",&gmtMu_eta_tree);
  mytree->Branch("gmtMu_phi",&gmtMu_phi_tree);
  //mytree->Branch("gmtMu_Quality",&gmtMu_Quality_tree);

  mytree->Branch("bmtfMu_pT", &bmtfMu_pT_tree); 
  mytree->Branch("bmtfMu_eta",&bmtfMu_eta_tree);
  mytree->Branch("bmtfMu_phi",&bmtfMu_phi_tree);
  mytree->Branch("bmtfMu_Quality",&bmtfMu_Quality_tree);

}

L1P2NtupleMaker::~L1P2NtupleMaker()
{
}

void L1P2NtupleMaker::beginJob()
{
}


void L1P2NtupleMaker::endJob() 
{
}

// ------------ method called for each event  ------------
void L1P2NtupleMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<vector<L1KalmanMuTrack>  > L1standMuCandidates;
  iEvent.getByLabel(L1standMuCandidates_, L1standMuCandidates);

  edm::Handle<BXVector<l1t::Muon> > L1GmtCandidates;
  iEvent.getByLabel(L1GmtCandidates_, L1GmtCandidates);

  edm::Handle<BXVector<l1t::RegionalMuonCand> > L1BmtfCandidates;
  iEvent.getByLabel(L1BmtfCandidates_, L1BmtfCandidates);

  standMu_pT_tree  = -999.;
  standMu_eta_tree = -999.;
  standMu_phi_tree = -999.;

  gmtMu_pT_tree      = -999.;     
  gmtMu_eta_tree     = -999.;
  gmtMu_phi_tree     = -999.;
  //gmtMu_Quality_tree = 0;

  bmtfMu_pT_tree      = -999.;     
  bmtfMu_eta_tree     = -999.;
  bmtfMu_phi_tree     = -999.;
  bmtfMu_Quality_tree = 0;
  

  //Loop over Kalman Filter standalone muons 
  float pTmuMax   = -999.;
  float pTmu_temp = -999.;

  for(auto mu = L1standMuCandidates->begin(); mu != L1standMuCandidates->end(); ++mu){

    pTmu_temp = mu->pt();

    if (pTmu_temp < pTmuMax) continue;
    pTmuMax = pTmu_temp;

    standMu_pT_tree  = pTmuMax;
    standMu_eta_tree = mu->eta();
    standMu_phi_tree = mu->phi();

    //std::cout << "mu pT :" << mu->pt() << "Eta: " << mu->eta() << "phi:" << mu->phi() << std::endl;
  }


  //Loop over GMT standalone muons 
  float pTmuGmtMax   = -999.;
  float pTmuGmt_temp = -999.;

  for(auto mu = L1GmtCandidates->begin(); mu != L1GmtCandidates->end(); ++mu){

    pTmuGmt_temp = mu->pt();

    if (pTmuGmt_temp < pTmuGmtMax) continue;
    pTmuGmtMax = pTmuGmt_temp;

    gmtMu_pT_tree      = pTmuGmtMax;
    gmtMu_eta_tree     = mu->eta();
    gmtMu_phi_tree     = mu->phi();
    //gmtMu_Quality_tree = mu->hwQual(); // hardware quality code  

    //std::cout << "mu pT :" << mu->pt() << "Eta: " << mu->eta() << "phi:" << mu->phi() << std::endl;
  }


  //Loop over BMTF standalone muons 
  float pTmuBmtfMax   = -999.;
  float pTmuBmtf_temp = -999.;

  for(auto mu = L1BmtfCandidates->begin(); mu != L1BmtfCandidates->end(); ++mu){

    pTmuBmtf_temp = 0.5 * mu->hwPt(); // 0.5* compressed pT as transmitted by hardware = pT (GeV)

    if (pTmuBmtf_temp < pTmuBmtfMax) continue;
    pTmuBmtfMax = pTmuBmtf_temp;

    bmtfMu_pT_tree      = pTmuBmtfMax;
    bmtfMu_eta_tree     = mu->hwEta() * 0.010875; // compressed eta from hardware * 0.010875 = eta
    bmtfMu_phi_tree     = mu->hwPhi() * 2. * TMath::Pi() /576.; // compressed relative phi from hardware * 2*pi/576 = local phi in rad
    bmtfMu_Quality_tree = mu->hwQual(); // hardware quality code

  }


  mytree->Fill();
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1P2NtupleMaker);
