#! /usr/bin/env python

"""
Usage:
./calculate_l1rates.py destination_file.root origin_directory_of_root_files
"""

import ROOT
import sys
import os

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
nbins_mupt = 131

h_l1rate = dict()
h_l1rate["MuPt"]     = ROOT.TH1F("MuPt",    "L1_SingleMu p_{T} distribution",      nbins_mupt, -0.5,  130.5)
h_l1rate["nMuVsPt"]  = ROOT.TH1F("nMuVsPt", "L1_SingleMu rate vs p_{T} threshold", nbins_mupt, -0.5,  130.5)
h_l1rate["nMuVsEta"] = ROOT.TH1F("nMuVsEta","L1_SingleMu16 rate vs #eta",          30,         -3.,   3.   )
h_l1rate["nMuVsPhi"] = ROOT.TH1F("nMuVsPhi","L1_SingleMu16 rate vs #phi",          16,         -3.14, 3.14 )
h_l1rate["MuPt_gmt"]     = ROOT.TH1F("MuPt_gmt",    "L1_SingleMu_gmt p_{T} distribution",      nbins_mupt, -0.5,  130.5)
h_l1rate["nMuVsPt_gmt"]  = ROOT.TH1F("nMuVsPt_gmt", "L1_SingleMu_gmt rate vs p_{T} threshold", nbins_mupt, -0.5,  130.5)
h_l1rate["nMuVsEta_gmt"] = ROOT.TH1F("nMuVsEta_gmt","L1_SingleMu16_gmt rate vs #eta",          30,         -3.,   3.   )
h_l1rate["nMuVsPhi_gmt"] = ROOT.TH1F("nMuVsPhi_gmt","L1_SingleMu16_gmt rate vs #phi",          16,         -3.14, 3.14 )


h_l1rate["MuPt"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsPt"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsEta"].GetXaxis().SetTitle("#eta")
h_l1rate["nMuVsPhi"].GetXaxis().SetTitle("#phi")
h_l1rate["MuPt_gmt"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsPt_gmt"].GetXaxis().SetTitle("p_{T} [GeV]")
h_l1rate["nMuVsEta_gmt"].GetXaxis().SetTitle("#eta")
h_l1rate["nMuVsPhi_gmt"].GetXaxis().SetTitle("#phi")


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
    maxmu_pt  = mytree.standMu_pT
    maxmu_eta = mytree.standMu_eta
    maxmu_phi = mytree.standMu_phi
    
    gmtmu_pt  = mytree.gmtMu_pT
    gmtmu_eta = mytree.gmtMu_eta
    gmtmu_phi = mytree.gmtMu_phi


    ##Fill the histos
    h_l1rate["MuPt"].Fill(maxmu_pt)
    h_l1rate["MuPt_gmt"].Fill(gmtmu_pt)

    ##Fill the histos for rate vs threshold
    for ptcut in xrange(nbins_mupt):
        if  maxmu_pt>= ptcut :
            h_l1rate["nMuVsPt"].Fill(ptcut)
            
    for ptcut in xrange(nbins_mupt):
        if  gmtmu_pt>= ptcut :
            h_l1rate["nMuVsPt_gmt"].Fill(ptcut)

    # Fill the histos for rate vs eta and phi
    if maxmu_pt >= 16. :
        if maxmu_eta >= -3. :
            h_l1rate["nMuVsEta"].Fill(maxmu_eta)
        if maxmu_phi >= -3.14 :
            h_l1rate["nMuVsPhi"].Fill(maxmu_phi)

    if gmtmu_pt >= 16. :
        if gmtmu_eta >= -3. :
            h_l1rate["nMuVsEta_gmt"].Fill(gmtmu_eta)
        if gmtmu_phi >= -3.14 :
            h_l1rate["nMuVsPhi_gmt"].Fill(gmtmu_phi)


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
    h_l1rate[hname].Draw("PE")
    c1.SaveAs(out_dir + hname + ".png")
    c1.SaveAs(out_dir + hname + ".pdf")

fOut_histos.Close()

print "Number of events analyzed = ", nZeroBias
