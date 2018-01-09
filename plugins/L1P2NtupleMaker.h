#include <DataFormats/L1Trigger/interface/BXVector.h>


//---------- class declaration----------

class L1P2NtupleMaker : public edm::EDAnalyzer {
public:
  explicit L1P2NtupleMaker(const edm::ParameterSet&);
  ~L1P2NtupleMaker();

private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() override;

  const edm::InputTag L1standMuCandidates_;
  const edm::InputTag L1GmtCandidates_;
  const edm::InputTag L1BmtfCandidates_;

  edm::Service<TFileService> fs;

  // ----------member data ---------------------------

  //TTree and TTree variables
  TTree *mytree;

  float standMu_pT_tree;
  float standMu_eta_tree;
  float standMu_phi_tree;

  float gmtMu_pT_tree; 
  float gmtMu_eta_tree;
  float gmtMu_phi_tree;
  //int   gmtMu_Quality_tree;

  float bmtfMu_pT_tree; 
  float bmtfMu_eta_tree;
  float bmtfMu_phi_tree;
  int   bmtfMu_Quality_tree;


  //Tokens
  edm::EDGetTokenT<std::vector<L1KalmanMuTrack> > L1standMuCandidatesToken_;
  edm::EDGetTokenT<BXVector<l1t::Muon> > L1GmtCandidatesToken_; 
  edm::EDGetTokenT<BXVector<l1t::RegionalMuonCand> > L1BmtfCandidatesToken_; 

};
