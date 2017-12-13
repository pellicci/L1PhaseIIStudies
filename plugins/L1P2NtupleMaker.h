
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

  edm::Service<TFileService> fs;

  // ----------member data ---------------------------

  //TTree and TTree variables
  TTree *mytree;

  float standMu_pT_tree;
  float standMu_eta_tree;
  float standMu_phi_tree;

  //Tokens
  edm::EDGetTokenT<std::vector<L1KalmanMuTrack> > L1standMuCandidatesToken_; 

};
