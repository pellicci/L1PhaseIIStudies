
//ROOT includes
#include "TTree.h"

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

#include "L1P2NtupleMaker.h"

using namespace::std;
 
// constructors and destructor
L1P2NtupleMaker::L1P2NtupleMaker(const edm::ParameterSet& iConfig) :
  L1standMuCandidates_(iConfig.getParameter<edm::InputTag>("L1standMuCandidates")),
  L1GmtCandidates_(iConfig.getParameter<edm::InputTag>("L1GmtCandidates"))
{
  L1standMuCandidatesToken_ = consumes<vector<L1KalmanMuTrack> >(L1standMuCandidates_); 
  L1GmtCandidatesToken_     = consumes<BXVector<l1t::Muon> >(L1GmtCandidates_);

  mytree = fs->make<TTree>("mytree", "Tree containing L1 info");

  mytree->Branch("standMu_pT", &standMu_pT_tree);
  mytree->Branch("standMu_eta",&standMu_eta_tree);
  mytree->Branch("standMu_phi",&standMu_phi_tree);

  mytree->Branch("gmtMu_pT", &gmtMu_pT_tree); 
  mytree->Branch("gmtMu_eta",&gmtMu_eta_tree);
  mytree->Branch("gmtMu_phi",&gmtMu_phi_tree);

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

  standMu_pT_tree  = -999.;
  standMu_eta_tree = -999.;
  standMu_phi_tree = -999.;

  gmtMu_pT_tree  = -999.;     
  gmtMu_eta_tree = -999.;
  gmtMu_phi_tree = -999.;

  //Loop over Kalman Filter standalone muons 
  float pTmuMax = -999.;

  for(auto mu = L1standMuCandidates->begin(); mu != L1standMuCandidates->end(); ++mu){

    if (mu->pt() < pTmuMax) continue;
    pTmuMax = mu->pt();

    standMu_pT_tree  = pTmuMax;
    standMu_eta_tree = mu->eta();
    standMu_phi_tree = mu->phi();

    //std::cout << "mu pT :" << mu->pt() << "Eta: " << mu->eta() << "phi:" << mu->phi() << std::endl;
  }


  //Loop over GMT standalone muons 
  float pTmuGmtMax = -999.;

  for(auto mu = L1GmtCandidates->begin(); mu != L1GmtCandidates->end(); ++mu){

    if (mu->pt() < pTmuGmtMax) continue;
    pTmuGmtMax = mu->pt();

    gmtMu_pT_tree  = pTmuGmtMax;
    gmtMu_eta_tree = mu->eta();
    gmtMu_phi_tree = mu->phi();

    //std::cout << "mu pT :" << mu->pt() << "Eta: " << mu->eta() << "phi:" << mu->phi() << std::endl;
  }

  mytree->Fill();
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1P2NtupleMaker);
