
//ROOT includes
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
 
#include "L1P2NtupleMaker.h"
 
// constructors and destructor
L1P2NtupleMaker::L1P2NtupleMaker(const edm::ParameterSet& iConfig) :
  L1standMuCandidates_(iConfig.getParameter<edm::InputTag>("L1standMuCandidates"))
{
  L1StandMuCandidatesToken_ = consumes<std::vector<CONTAINERFIXME> >(L1standMuCandidates_); 

  mytree = fs->make<TTree>("mytree", "Tree containing L1 info");

  mytree->Branch("standMu_pT",&standMu_pT_tree);
  mytree->Branch("standMu_eta",&standMu_eta_tree);
  mytree->Branch("standMu_phi",&standMu_phi_tree);

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
  edm::Handle<std::vector<CONTAINERFIXME>  > L1standMuCandidates;
  iEvent.getByLabel(L1standMuCandidates_, L1standMuCandidates);

  standMu_pT_tree = -999.;
  standMu_eta_tree = -999.;
  standMu_phi_tree = -999.;

  //Loop over standalone muons
  pTmuMax = -999.;

  for(auto mu = slimmedMuons->begin(); mu != slimmedMuons->end(); ++mu){

    if (mu->pt() < pTmuMax) continue;
    pTmuMax = mu->pt();

    standMu_pT_tree = pTmuMax;
    standMu_eta_tree = mu->eta();
    standMu_phi_tree = mu->phi;

    //std::cout << "mu pT :" << mu->pt() << "Eta: " << mu->eta() << "phi:" << mu->phi() << std::endl;
  }

  mytree->Fill();
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1P2NtupleMaker);
