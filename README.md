# L1PhaseIIStudies

This package provides utilities for Phase-2 studies for L1 objects.

How to install:

- Instructions to create a release:
  https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TPhase2Instructions#CMSSW_9_2_0_and_l1t_phase2_v1_14

```
  cmsrel CMSSW_9_2_0
  cd CMSSW_9_2_0/src/
  cmsenv
  git cms-init
  git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
  git fetch cms-l1t-offline
  git cms-merge-topic -u cms-l1t-offline:l1t-phase2-v1.14.1
```

- If you want the L1 muon kalman filter, do this

```
  git remote add bachtis git@github.com:bachtis/cmssw.git
  git fetch bachtis
  git checkout bachtis/KMTF_PhaseII
  git cms-merge-topic -u cms-l1t-offline:l1t-phase2-v1.14.1
```

- Then get our package

```
  git clone https://github.com/pellicci/L1PhaseIIStudies.git L1TriggerDPG/L1PhaseIIStudies
  scram b
```

- Then go in test, where you'll find run_l1p2ntuplemaker.py, which is the main python config for the ntuple maker
