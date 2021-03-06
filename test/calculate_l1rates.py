#! /usr/bin/env python

"""
Usage:
./calculate_l1rates.py destination_file.root origin_directory_of_root_files
"""

import ROOT
import sys
import os
import math

nBunches = 2508.
nPU_min = 100.
nPU_max = 200.
nEventsMax = -1 #500000

isMC = True
print "Am I running on MC? -> ", isMC

out_dir = 'results/'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
out_root = sys.argv[1]
print "The output file name will be ", out_dir + out_root

ROOT.gStyle.SetOptStat(0)

dir_path = sys.argv[2]
print "I will look for the trees in ", dir_path

print "Merging the trees"
ls_command = "ls " + dir_path + "/ | grep root "
file_list = os.popen(ls_command).read()
mytree = ROOT.TChain("L1P2NtupleMaker/mytree")
for filename in file_list.split():
    mytree.Add(dir_path + "/" + filename)

def get_scale_factor(_nZeroBias, _nBunches):

    if _nZeroBias != 0:
        scal = 11246.      #ZeroBias per bunch in kHz
        scal /= _nZeroBias
        scal *= _nBunches
        return scal

    return 0.

print "Preparing plotting stuff"
nbins_mupt  = 131
nbins_muPhi = 16

h_l1rate = dict()
# kalman Cleaned
h_l1rate["MuPt_ER"]       = ROOT.TH1F("MuPt_ER",       "L1_SingleMu p_{T} distribution in |#eta|<=0.8",      nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsPt_ER"]    = ROOT.TH1F("nMuVsPt_ER",    "L1_SingleMu rate vs p_{T} threshold in |#eta|<=0.8", nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsEta_ER"]   = ROOT.TH1F("nMuVsEta_ER",   "L1_SingleMu16 rate vs #eta in |#eta|<=0.8",          30,          -3.,   3.   )
h_l1rate["nMuVsPhi_ER"]   = ROOT.TH1F("nMuVsPhi_ER",   "L1_SingleMu16 rate vs #phi in |#eta|<=0.8",          nbins_muPhi, -3.14, 3.14 )
h_l1rate["quality_ER"]    = ROOT.TH1F("quality_ER",    "L1_SingleMu quality information",                    17,          -0.5,  16.5 )
h_l1rate["charge_ER"]     = ROOT.TH1F("charge_ER",     "L1_SingleMu charge information",                     150,         -1.5,  1.5  )
h_l1rate["approxChi2_ER"] = ROOT.TH1F("approxChi2_ER", "L1_SingleMu Chi2 information",                       100,          0,    1000 )

# kalman All
h_l1rate["MuPt_All_ER"]       = ROOT.TH1F("MuPt_All_ER",       "L1_SingleMu_All p_{T} distribution in |#eta|<=0.8",      nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsPt_All_ER"]    = ROOT.TH1F("nMuVsPt_All_ER",    "L1_SingleMu_All rate vs p_{T} threshold in |#eta|<=0.8", nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsEta_All_ER"]   = ROOT.TH1F("nMuVsEta_All_ER",   "L1_SingleMu16_All rate vs #eta in |#eta|<=0.8",          30,          -3.,   3.   )
h_l1rate["nMuVsPhi_All_ER"]   = ROOT.TH1F("nMuVsPhi_All_ER",   "L1_SingleMu16_All rate vs #phi in |#eta|<=0.8",          nbins_muPhi, -3.14, 3.14 )
h_l1rate["quality_All_ER"]    = ROOT.TH1F("quality_All_ER",    "L1_SingleMu_All quality information",                    17,          -0.5,  16.5 )
h_l1rate["charge_All_ER"]     = ROOT.TH1F("charge_All_ER",     "L1_SingleMu_All charge information",                     150,         -1.5,  1.5  )
h_l1rate["approxChi2_All_ER"] = ROOT.TH1F("approxChi2_All_ER", "L1_SingleMu_All Chi2 information",                       100,          0,    1000 )
 
# gmt
h_l1rate["MuPt_gmt_ER"]     = ROOT.TH1F("MuPt_gmt_ER",    "L1_SingleMu_gmt p_{T} distribution in |#eta|<=0.8",      nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsPt_gmt_ER"]  = ROOT.TH1F("nMuVsPt_gmt_ER", "L1_SingleMu_gmt rate vs p_{T} threshold in |#eta|<=0.8", nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsEta_gmt_ER"] = ROOT.TH1F("nMuVsEta_gmt_ER","L1_SingleMu16_gmt rate vs #eta in |#eta|<=0.8",          30,          -3.,   3.   )
h_l1rate["nMuVsPhi_gmt_ER"] = ROOT.TH1F("nMuVsPhi_gmt_ER","L1_SingleMu16_gmt rate vs #phi in |#eta|<=0.8",          nbins_muPhi, -3.14, 3.14 )

h_l1rate["MuPt_gmt"]     = ROOT.TH1F("MuPt_gmt",    "L1_SingleMu_gmt p_{T} distribution in full #eta range",      nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsPt_gmt"]  = ROOT.TH1F("nMuVsPt_gmt", "L1_SingleMu_gmt rate vs p_{T} threshold in full #eta range", nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsEta_gmt"] = ROOT.TH1F("nMuVsEta_gmt","L1_SingleMu16_gmt rate vs #eta in full #eta range",          30,          -3.,   3.   )
h_l1rate["nMuVsPhi_gmt"] = ROOT.TH1F("nMuVsPhi_gmt","L1_SingleMu16_gmt rate vs #phi in full #eta range",          nbins_muPhi, -3.14, 3.14 )

# bmtf Standard
h_l1rate["MuPt_bmtf_Std_ER"]     = ROOT.TH1F("MuPt_bmtf_Std_ER",    "L1_SingleMu_bmtf_Std p_{T} distribution in |#eta|<=0.8",      nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsPt_bmtf_Std_ER"]  = ROOT.TH1F("nMuVsPt_bmtf_Std_ER", "L1_SingleMu_bmtf_Std rate vs p_{T} threshold in |#eta|<=0.8", nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsEta_bmtf_Std_ER"] = ROOT.TH1F("nMuVsEta_bmtf_Std_ER","L1_SingleMu16_bmtf_Std rate vs #eta in |#eta|<=0.8",          30,          -3.,   3.   )
h_l1rate["nMuVsPhi_bmtf_Std_ER"] = ROOT.TH1F("nMuVsPhi_bmtf_Std_ER","L1_SingleMu16_bmtf_Std rate vs #phi in |#eta|<=0.8",          nbins_muPhi, -3.14, 3.14 )
h_l1rate["quality_bmtf_Std_ER"]  = ROOT.TH1F("quality_bmtf_Std_ER", "L1_SingleMu_bmtf_Std quality information",                    17,          -0.5,  16.5 )
h_l1rate["charge_bmtf_Std_ER"]   = ROOT.TH1F("charge_bmtf_Std_ER",  "L1_SingleMu_bmtf_Std charge information",                     150,         -1.5,  1.5  )

# bmtf
h_l1rate["MuPt_bmtf_ER"]     = ROOT.TH1F("MuPt_bmtf_ER",    "L1_SingleMu_bmtf p_{T} distribution in |#eta|<=0.8",      nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsPt_bmtf_ER"]  = ROOT.TH1F("nMuVsPt_bmtf_ER", "L1_SingleMu_bmtf rate vs p_{T} threshold in |#eta|<=0.8", nbins_mupt,  -0.5,  130.5)
h_l1rate["nMuVsEta_bmtf_ER"] = ROOT.TH1F("nMuVsEta_bmtf_ER","L1_SingleMu16_bmtf rate vs #eta in |#eta|<=0.8",          30,          -3.,   3.   )
h_l1rate["nMuVsPhi_bmtf_ER"] = ROOT.TH1F("nMuVsPhi_bmtf_ER","L1_SingleMu16_bmtf rate vs #phi in |#eta|<=0.8",          nbins_muPhi, -3.14, 3.14 )
h_l1rate["quality_bmtf_ER"]  = ROOT.TH1F("quality_bmtf_ER", "L1_SingleMu_bmtf quality information",                    17,          -0.5,  16.5 )
h_l1rate["charge_bmtf_ER"]   = ROOT.TH1F("charge_bmtf_ER",  "L1_SingleMu_bmtf charge information",                     150,         -1.5,  1.5  )


# assign axis title
h_l1rate["MuPt_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsPt_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsEta_ER"].GetXaxis().SetTitle("#eta")
h_l1rate["nMuVsPhi_ER"].GetXaxis().SetTitle("#phi")
h_l1rate["quality_ER"].GetXaxis().SetTitle("#mu quality")    
h_l1rate["charge_ER"].GetXaxis().SetTitle("#mu charge")     
h_l1rate["approxChi2_ER"].GetXaxis().SetTitle("#chi^{2}") 


h_l1rate["MuPt_All_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsPt_All_ER"].GetXaxis().SetTitle("p_{T} [GeV]")   
h_l1rate["nMuVsEta_All_ER"].GetXaxis().SetTitle("#eta")  
h_l1rate["nMuVsPhi_All_ER"].GetXaxis().SetTitle("#phi")  
h_l1rate["quality_All_ER"].GetXaxis().SetTitle("#mu quality")    
h_l1rate["charge_All_ER"].GetXaxis().SetTitle("#mu charge")    
h_l1rate["approxChi2_All_ER"].GetXaxis().SetTitle("#chi^{2}")


h_l1rate["MuPt_gmt_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsPt_gmt_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsEta_gmt_ER"].GetXaxis().SetTitle("#eta")
h_l1rate["nMuVsPhi_gmt_ER"].GetXaxis().SetTitle("#phi")

h_l1rate["MuPt_gmt"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsPt_gmt"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsEta_gmt"].GetXaxis().SetTitle("#eta")
h_l1rate["nMuVsPhi_gmt"].GetXaxis().SetTitle("#phi")


h_l1rate["MuPt_bmtf_Std_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsPt_bmtf_Std_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsEta_bmtf_Std_ER"].GetXaxis().SetTitle("#eta")
h_l1rate["nMuVsPhi_bmtf_Std_ER"].GetXaxis().SetTitle("#phi")
h_l1rate["quality_bmtf_Std_ER"].GetXaxis().SetTitle("#mu quality")
h_l1rate["charge_bmtf_Std_ER"].GetXaxis().SetTitle("#mu charge") 


h_l1rate["MuPt_bmtf_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsPt_bmtf_ER"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsEta_bmtf_ER"].GetXaxis().SetTitle("#eta")
h_l1rate["nMuVsPhi_bmtf_ER"].GetXaxis().SetTitle("#phi")
h_l1rate["quality_bmtf_ER"].GetXaxis().SetTitle("#mu quality")
h_l1rate["charge_bmtf_ER"].GetXaxis().SetTitle("#mu charge") 



for hname in h_l1rate:
    if isMC:
        h_l1rate[hname].SetLineColor(ROOT.kRed)
        h_l1rate[hname].SetMarkerColor(ROOT.kRed)
    else:
        h_l1rate[hname].SetLineColor(ROOT.kBlue)
        h_l1rate[hname].SetMarkerColor(ROOT.kBlue)
    h_l1rate[hname].SetMarkerStyle(21)
    
nZeroBias = 0.

print "Starting the loop over the events"
for jentry in xrange(mytree.GetEntriesFast()):
    ientry = mytree.LoadTree(jentry)
    if ientry < 0:
        break
    nb = mytree.GetEntry(jentry)
    if nb <=0:
        continue

    nZeroBias += 1.

    if nZeroBias % 50000 == 0 :
        print "Processing event number = ", nZeroBias

    if nZeroBias > nEventsMax and nEventsMax != -1:
        break

    #Get the leading objects of the event
    maxmu_pt         = mytree.standMu_pT
    maxmu_eta        = mytree.standMu_eta
    maxmu_phi        = mytree.standMu_phi
    maxmu_quality    = mytree.standMu_Quality
    maxmu_charge     = mytree.standMu_charge
    maxmu_approxChi2 = mytree.standMu_approxChi2

    maxmuAll_pt         = mytree.standMuAll_pT
    maxmuAll_eta        = mytree.standMuAll_eta
    maxmuAll_phi        = mytree.standMuAll_phi
    maxmuAll_quality    = mytree.standMuAll_Quality
    maxmuAll_charge     = mytree.standMuAll_charge
    maxmuAll_approxChi2 = mytree.standMuAll_approxChi2
    
    gmtmu_pt  = mytree.gmtMu_pT
    gmtmu_eta = mytree.gmtMu_eta
    gmtmu_phi = mytree.gmtMu_phi

    bmtfStdmu_pt      = mytree.bmtfStdMu_pT
    bmtfStdmu_eta     = mytree.bmtfStdMu_eta
    bmtfStdmu_phi     = mytree.bmtfStdMu_phi
    bmtfStdmu_quality = mytree.bmtfStdMu_Quality
    bmtfStdmu_charge  = mytree.bmtfStdMu_charge

    bmtfmu_pt      = mytree.bmtfMu_pT
    bmtfmu_eta     = mytree.bmtfMu_eta
    bmtfmu_phi     = mytree.bmtfMu_phi
    bmtfmu_quality = mytree.bmtfMu_Quality
    bmtfmu_charge  = mytree.bmtfMu_charge


    ##Fill the histos for the pT distribution
    h_l1rate["MuPt_ER"].Fill(maxmu_pt)
    h_l1rate["MuPt_All_ER"].Fill(maxmuAll_pt)
    h_l1rate["MuPt_gmt"].Fill(gmtmu_pt)
    if math.fabs(gmtmu_eta) <= 0.8 :        
        h_l1rate["MuPt_gmt_ER"].Fill(gmtmu_pt)

    h_l1rate["MuPt_bmtf_Std_ER"].Fill(bmtfStdmu_pt)
    h_l1rate["MuPt_bmtf_ER"].Fill(bmtfmu_pt)


    ##Fill the histos for rate vs threshold
    for ptcut in xrange(nbins_mupt):
        if  maxmu_pt>= ptcut :
            h_l1rate["nMuVsPt_ER"].Fill(ptcut)

    for ptcut in xrange(nbins_mupt):
        if  maxmuAll_pt>= ptcut :
            h_l1rate["nMuVsPt_All_ER"].Fill(ptcut)
            
    for ptcut in xrange(nbins_mupt):
        if  gmtmu_pt>= ptcut :
            h_l1rate["nMuVsPt_gmt"].Fill(ptcut)
            if  math.fabs(gmtmu_eta) <= 0.8 :   
                h_l1rate["nMuVsPt_gmt_ER"].Fill(ptcut)

    for ptcut in xrange(nbins_mupt):
        if  bmtfStdmu_pt>= ptcut :
            h_l1rate["nMuVsPt_bmtf_Std_ER"].Fill(ptcut)

    for ptcut in xrange(nbins_mupt):
        if  bmtfmu_pt>= ptcut :
            h_l1rate["nMuVsPt_bmtf_ER"].Fill(ptcut)


    ##Fill the histos for rate vs eta and phi
    if maxmu_pt >= 16. :
        if maxmu_eta >= -3. :
            h_l1rate["nMuVsEta_ER"].Fill(maxmu_eta)
        if maxmu_phi >= -3.14 :
            h_l1rate["nMuVsPhi_ER"].Fill(maxmu_phi)

    if maxmuAll_pt >= 16. :
        if maxmuAll_eta >= -3. :
            h_l1rate["nMuVsEta_All_ER"].Fill(maxmuAll_eta)
        if maxmuAll_phi >= -3.14 :
            h_l1rate["nMuVsPhi_All_ER"].Fill(maxmuAll_phi)

    if gmtmu_pt >= 16. :
        if gmtmu_eta >= -3. :
            h_l1rate["nMuVsEta_gmt"].Fill(gmtmu_eta)
            if  math.fabs(gmtmu_eta) <= 0.8 :  
                h_l1rate["nMuVsEta_gmt_ER"].Fill(gmtmu_eta)            

        if gmtmu_phi >= -3.14 :
            h_l1rate["nMuVsPhi_gmt"].Fill(gmtmu_phi)
            if  math.fabs(gmtmu_eta) <= 0.8 : 
                h_l1rate["nMuVsPhi_gmt_ER"].Fill(gmtmu_phi)

    if bmtfStdmu_pt >= 16. :
        if bmtfStdmu_eta >= -3. :
            h_l1rate["nMuVsEta_bmtf_Std_ER"].Fill(bmtfStdmu_eta)
        if bmtfStdmu_phi >= -3.14 :
            h_l1rate["nMuVsPhi_bmtf_Std_ER"].Fill(bmtfStdmu_phi)

    if bmtfmu_pt >= 16. :
        if bmtfmu_eta >= -3. :
            h_l1rate["nMuVsEta_bmtf_ER"].Fill(bmtfmu_eta)
        if bmtfmu_phi >= -3.14 :
            h_l1rate["nMuVsPhi_bmtf_ER"].Fill(bmtfmu_phi)


    ##Fill the histos for the trigger quality 
    if maxmu_pt >= 16. :
        h_l1rate["quality_ER"].Fill(maxmu_quality)

    if maxmuAll_pt >= 16. :
        h_l1rate["quality_All_ER"].Fill(maxmuAll_quality)

    if bmtfStdmu_pt >= 16. :  
        h_l1rate["quality_bmtf_Std_ER"].Fill(bmtfStdmu_quality)

    if bmtfmu_pt >= 16. :  
        h_l1rate["quality_bmtf_ER"].Fill(bmtfmu_quality)


    ##Fill histos for muon charge 
    if maxmu_pt >= 16. :
        h_l1rate["charge_ER"].Fill(maxmu_charge)

    if maxmuAll_pt >= 16. :
        h_l1rate["charge_All_ER"].Fill(maxmuAll_charge)

    if bmtfStdmu_pt >= 16. :
        h_l1rate["charge_bmtf_Std_ER"].Fill(bmtfStdmu_charge)

    if bmtfmu_pt >= 16. :
        h_l1rate["charge_bmtf_ER"].Fill(bmtfmu_charge)


    ##FIll histos for Chi2
    if maxmu_pt >= 16. :
        h_l1rate["approxChi2_ER"].Fill(maxmu_approxChi2)

    if maxmuAll_pt >= 16. :
        h_l1rate["approxChi2_All_ER"].Fill(maxmuAll_approxChi2)



print "End of event loop"


fOut_histos = ROOT.TFile(out_dir + out_root,"RECREATE")
scale_factor_std = get_scale_factor(nZeroBias,nBunches)


for hname in h_l1rate:
    h_l1rate[hname].Scale(scale_factor_std)
    h_l1rate[hname].GetYaxis().SetTitle("Rate [Hz]")
    h_l1rate[hname].Write()

    c1 = ROOT.TCanvas()
    c1.cd()
    if "Pt" in hname:
        c1.SetLogy()
    if "Chi2" in hname : 
        c1.SetLogx()
    h_l1rate[hname].Draw("PE")
    c1.SaveAs(out_dir + hname + ".png")
    c1.SaveAs(out_dir + hname + ".pdf")

fOut_histos.Close()

print "Number of events analyzed = ", nZeroBias
