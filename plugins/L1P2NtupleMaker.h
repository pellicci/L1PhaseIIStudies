#include <DataFormats/L1Trigger/interface/BXVector.h>


//---------- class declaration----------

class L1P2NtupleMaker : public edm::EDAnalyzer {
public:
  explicit L1P2NtupleMaker(const edm::ParameterSet&);
  ~L1P2NtupleMaker();

  float calcGlobalPhi(int localhwPhi, int proc);

private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() override;

  const edm::InputTag L1standMuCandidates_;
  const edm::InputTag L1standMuAllCandidates_;
  const edm::InputTag L1GmtCandidates_;
  const edm::InputTag L1BmtfStdCandidates_;
  const edm::InputTag L1BmtfCandidates_;

  edm::Service<TFileService> fs;

  // ----------member data ---------------------------

  //TTree and TTree variables
  TTree *mytree;

  float standMu_pT_tree;
  float standMu_eta_tree;
  float standMu_phi_tree;
  int   standMu_Quality_tree;
  int   standMu_charge_tree;
  int   standMu_approxChi2_tree;

  float standMuAll_pT_tree;
  float standMuAll_eta_tree;
  float standMuAll_phi_tree;
  int   standMuAll_Quality_tree;
  int   standMuAll_charge_tree;
  int   standMuAll_approxChi2_tree;

  float gmtMu_pT_tree; 
  float gmtMu_eta_tree;
  float gmtMu_phi_tree;
  //int   gmtMu_Quality_tree;

  float bmtfStdMu_pT_tree; 
  float bmtfStdMu_eta_tree;
  float bmtfStdMu_phi_tree;
  int   bmtfStdMu_Quality_tree;
  int   bmtfStdMu_charge_tree;

  float bmtfMu_pT_tree; 
  float bmtfMu_eta_tree;
  float bmtfMu_phi_tree;
  int   bmtfMu_Quality_tree;
  int   bmtfMu_charge_tree;


  //Tokens
  edm::EDGetTokenT<std::vector<L1KalmanMuTrack> > L1standMuCandidatesToken_;
  edm::EDGetTokenT<std::vector<L1KalmanMuTrack> > L1standMuAllCandidatesToken_;
  edm::EDGetTokenT<BXVector<l1t::Muon> > L1GmtCandidatesToken_; 
  edm::EDGetTokenT<BXVector<l1t::RegionalMuonCand> > L1BmtfStdCandidatesToken_; 
  edm::EDGetTokenT<BXVector<l1t::RegionalMuonCand> > L1BmtfCandidatesToken_; 

};
