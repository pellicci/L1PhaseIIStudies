
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
  L1BmtfStdCandidates_(iConfig.getParameter<edm::InputTag>("L1BmtfStdCandidates")),
  L1BmtfCandidates_(iConfig.getParameter<edm::InputTag>("L1BmtfCandidates"))
{
  L1standMuCandidatesToken_ = consumes<vector<L1KalmanMuTrack> >(L1standMuCandidates_); 
  L1GmtCandidatesToken_     = consumes<BXVector<l1t::Muon> >(L1GmtCandidates_);
  L1BmtfStdCandidatesToken_ = consumes<BXVector<l1t::RegionalMuonCand> >(L1BmtfStdCandidates_);
  L1BmtfCandidatesToken_    = consumes<BXVector<l1t::RegionalMuonCand> >(L1BmtfCandidates_);

  mytree = fs->make<TTree>("mytree", "Tree containing L1 info");

  mytree->Branch("standMu_pT", &standMu_pT_tree);
  mytree->Branch("standMu_eta",&standMu_eta_tree);
  mytree->Branch("standMu_phi",&standMu_phi_tree);
  mytree->Branch("standMu_Quality", &standMu_Quality_tree);
  mytree->Branch("standMu_charge", &standMu_charge_tree);
  mytree->Branch("standMu_approxChi2", &standMu_approxChi2_tree);

  mytree->Branch("gmtMu_pT", &gmtMu_pT_tree); 
  mytree->Branch("gmtMu_eta",&gmtMu_eta_tree);
  mytree->Branch("gmtMu_phi",&gmtMu_phi_tree);
  //mytree->Branch("gmtMu_Quality",&gmtMu_Quality_tree);

  mytree->Branch("bmtfStdMu_pT", &bmtfStdMu_pT_tree); 
  mytree->Branch("bmtfStdMu_eta",&bmtfStdMu_eta_tree);
  mytree->Branch("bmtfStdMu_phi",&bmtfStdMu_phi_tree);
  mytree->Branch("bmtfStdMu_Quality",&bmtfStdMu_Quality_tree);
  mytree->Branch("bmtfStdMu_charge", &bmtfStdMu_charge_tree);

  mytree->Branch("bmtfMu_pT", &bmtfMu_pT_tree); 
  mytree->Branch("bmtfMu_eta",&bmtfMu_eta_tree);
  mytree->Branch("bmtfMu_phi",&bmtfMu_phi_tree);
  mytree->Branch("bmtfMu_Quality",&bmtfMu_Quality_tree);
  mytree->Branch("bmtfMu_charge", &bmtfMu_charge_tree); 

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


// take the local phi from hw and return the global phi for bmtf 
float L1P2NtupleMaker::calcGlobalPhi(int localhwPhi, int proc)
{
  int   globhwPhi   = 0;
  float globPhysPhi = 0.;

  // --- first convert hw local phi to hw global phi   
  globhwPhi = (proc) * 48 + localhwPhi; // each BMTF processor corresponds to a 30 degree wedge = 48 in int-scale
    
  globhwPhi += 576-24;                  // first processor starts at CMS phi = -15 degrees...
  
  globhwPhi = globhwPhi%576;            // handle wrap-around (since we add the 576-24, the value will never be negative!)


  //std::cout<< "processor: "<<proc<<" local phi: "<<localhwPhi<<" global hw phi: "<<globhwPhi<<endl;


  // --- then convert hw global phi to physical global phi (in rad)
  globPhysPhi = globhwPhi * 2 * TMath::Pi() /576.; // phi in 0 - 2Pi

  // --- phi in -Pi - Pi 
  if(globPhysPhi >= 0 && globPhysPhi <= TMath::Pi() ) {globPhysPhi = globPhysPhi;}
  else if (globPhysPhi > TMath::Pi() && globPhysPhi <= 2 * TMath::Pi()) {globPhysPhi = globPhysPhi - 2*TMath::Pi();}
  else std::cout<<" wrong value of phi!";
  
  
  //std::cout<< "global physical phi "<< globPhysPhi <<endl;


  return globPhysPhi;
}


// ------------ method called for each event  ------------
void L1P2NtupleMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<vector<L1KalmanMuTrack>  > L1standMuCandidates;
  iEvent.getByLabel(L1standMuCandidates_, L1standMuCandidates);

  edm::Handle<BXVector<l1t::Muon> > L1GmtCandidates;
  iEvent.getByLabel(L1GmtCandidates_, L1GmtCandidates);

  edm::Handle<BXVector<l1t::RegionalMuonCand> > L1BmtfStdCandidates;
  iEvent.getByLabel(L1BmtfStdCandidates_, L1BmtfStdCandidates);

  edm::Handle<BXVector<l1t::RegionalMuonCand> > L1BmtfCandidates;
  iEvent.getByLabel(L1BmtfCandidates_, L1BmtfCandidates);

  standMu_pT_tree         = -999.;
  standMu_eta_tree        = -999.;
  standMu_phi_tree        = -999.;
  standMu_Quality_tree    = 0;
  standMu_charge_tree     = -999;
  standMu_approxChi2_tree = -999;

  gmtMu_pT_tree      = -999.;     
  gmtMu_eta_tree     = -999.;
  gmtMu_phi_tree     = -999.;
  //gmtMu_Quality_tree = 0;

  bmtfStdMu_pT_tree      = -999.;     
  bmtfStdMu_eta_tree     = -999.;
  bmtfStdMu_phi_tree     = -999.;
  bmtfStdMu_Quality_tree = 0;
  bmtfStdMu_charge_tree  = -999;

  bmtfMu_pT_tree      = -999.;     
  bmtfMu_eta_tree     = -999.;
  bmtfMu_phi_tree     = -999.;
  bmtfMu_Quality_tree = 0;
  bmtfMu_charge_tree  = -999;
  

  //Loop over Kalman Filter standalone muons 
  float pTmuMax   = -999.;
  float pTmu_temp = -999.;
  
  for(auto mu = L1standMuCandidates->begin(); mu != L1standMuCandidates->end(); ++mu){

    pTmu_temp = mu->pt();

    if (pTmu_temp < pTmuMax) continue;
    pTmuMax = pTmu_temp;

    standMu_pT_tree         = pTmuMax;
    standMu_eta_tree        = mu->eta();
    standMu_phi_tree        = mu->phi();
    standMu_Quality_tree    = mu->quality();
    standMu_charge_tree     = mu->charge();  
    standMu_approxChi2_tree = mu->approxChi2();

    //std::cout << "mu pT :" << mu->pt() << " Eta: " << mu->eta() << " phi:" << mu->phi() << std::endl;
    //std::cout<<"charge kalman mu: "<< standMu_charge_tree<< endl;
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

    //std::cout << "mu pT :" << mu->pt() << " Eta: " << mu->eta() << " phi:" << mu->phi() << std::endl;
  }


  //Loop over Standard BMTF standalone muons 
  float pTmuBmtfStdMax   = -999.;
  float pTmuBmtfStd_temp = -999.;
  
  for(auto mu = L1BmtfStdCandidates->begin(); mu != L1BmtfStdCandidates->end(); ++mu){

    pTmuBmtfStd_temp = 0.5 * mu->hwPt(); // 0.5* compressed pT as transmitted by hardware = pT (GeV)

    if (pTmuBmtfStd_temp < pTmuBmtfStdMax) continue;
    pTmuBmtfStdMax = pTmuBmtfStd_temp;

    bmtfStdMu_pT_tree      = pTmuBmtfStdMax;
    bmtfStdMu_eta_tree     = mu->hwEta() * 0.010875; // compressed eta from hardware * 0.010875 = eta
    bmtfStdMu_phi_tree     = L1P2NtupleMaker::calcGlobalPhi(mu->hwPhi(), mu->processor());
    bmtfStdMu_Quality_tree = mu->hwQual(); // hardware quality code
    bmtfStdMu_charge_tree  = TMath::Power(-1, mu->hwSign()); // charge

    //std::cout << " mu pT :" << bmtfStdMu_pT_tree  << " Eta: " << bmtfStdMu_eta_tree << " Global phi Rad: " << bmtfStdMu_phi_tree << " quality: "<< bmtfStdMu_Quality_tree << std::endl;
    //std::cout<<"charge Stdbmtf mu: "<< bmtfStdMu_charge_tree<<endl;
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
    bmtfMu_phi_tree     = L1P2NtupleMaker::calcGlobalPhi(mu->hwPhi(), mu->processor());
    bmtfMu_Quality_tree = mu->hwQual(); // hardware quality code
    bmtfMu_charge_tree  = TMath::Power(-1, mu->hwSign()); // charge

    //std::cout << " mu pT :" << bmtfMu_pT_tree  << " Eta: " << bmtfMu_eta_tree << " Global phi Rad: " << bmtfMu_phi_tree << " quality: "<< bmtfMu_Quality_tree << std::endl;
    //std::cout<<"charge bmtf mu: "<< bmtfStdMu_charge_tree<<endl;
  }


  mytree->Fill();
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1P2NtupleMaker);
