#! /usr/bin/env python

# *******************
# usage: ./kalmanGmtComparison.py -f results/input_file.root
# *******************


import sys
import os
import argparse
import ROOT
from ROOT import gSystem, TFile, gPad, TCanvas, TLegend, kWhite, kBlack


# create output directory
OutputPath = "plots_kalmanGmtComparison"
gSystem.Exec("mkdir -p " + OutputPath)
print "Output directory created!"


# input file
parser = argparse.ArgumentParser()
parser.add_argument("--file","-f",type=str,required=True)
args = parser.parse_args()
in_file = TFile.Open(args.file)
print "Reading file", args.file


# get histos from input file 
histos_dict = {}
names_list  = in_file.GetListOfKeys()
names_iter  = names_list.MakeIterator()


while(names_iter.Next()) :

    histoname = names_iter.GetName()

    histos_dict[histoname] = in_file.Get(histoname)


names_list = histos_dict.keys()
names_list.sort()

kalman_list    = []
gmt_list       = []
plotName_list  = []


for hname in names_list : 

    if "_ER" in hname :
        if "_gmt" in hname :
            gmt_list.append(histos_dict[hname])
        else :
            kalman_list.append(histos_dict[hname])
            plotName_list.append(hname)
        

# draw plots
for i in range(len(plotName_list)) :

    canvas = TCanvas()
    canvas.cd()

    kalman_list[i].SetMarkerStyle(20)
    kalman_list[i].SetMarkerColor(2)
    kalman_list[i].SetLineColor(2)

    gmt_list[i].SetMarkerStyle(20)
    gmt_list[i].SetMarkerColor(1)
    gmt_list[i].SetLineColor(1)

    gmt_list[i].Draw('EP')
    kalman_list[i].Draw('sameEP')

    gPad.SetLogy()
    
    # legend
    legend = TLegend(0.74,0.68,0.94,0.87)
    legend.AddEntry(kalman_list[i],"Kalman", "pl")
    legend.AddEntry(gmt_list[i],"Gmt","pl")
    legend.SetFillColor(kWhite)
    legend.SetLineColor(kBlack)
    legend.SetTextFont(43)
    legend.SetTextSize(20)
    legend.Draw()
    
    canvas.Update()
    
    canvas.SaveAs(OutputPath + "/" + plotName_list[i] + ".pdf")
    canvas.SaveAs(OutputPath + "/" + plotName_list[i] + ".png")
    
    
    
    
    
    
