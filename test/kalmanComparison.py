#! /usr/bin/env python

# *******************
# usage: ./kalmanComparison.py -f results/input_file.root
# *******************


import sys
import os
import argparse
import ROOT
from ROOT import gSystem, TFile, gPad, TCanvas, TLegend, kWhite, kBlack


# create output directory
OutputPath = "plots_kalmanComparison"
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

kalman_list      = []
gmt_list         = []
bmtfStd_list     = []
bmtfStdName_list = []
bmtf_list        = []
plotName_list    = []   # needed also for naming final plots


for hname in names_list : 

    if "_ER" in hname :
        if "_gmt" in hname :
            gmt_list.append(histos_dict[hname])
        elif "_bmtf" in hname :
            if "_Std" in hname : 
                bmtfStd_list.append(histos_dict[hname])
                bmtfStdName_list.append(hname) 
            else :
                bmtf_list.append(histos_dict[hname])
        else :
            kalman_list.append(histos_dict[hname])
            plotName_list.append(hname) 
        

# draw plots
for i in range(len(plotName_list)) :            # will not plot plots which are only in the bmtfStd list

    if i > len(bmtfStdName_list) : continue     # will not plot plots which are only in the kmtf list

    canvas = TCanvas()
    canvas.cd()

    # gmt_list[i].SetMarkerStyle(20)
    # gmt_list[i].SetMarkerColor(1)
    # gmt_list[i].SetLineColor(1)

    kalman_list[i].SetMarkerStyle(20)
    kalman_list[i].SetMarkerColor(2)
    kalman_list[i].SetLineColor(2)

    bmtfStd_list[i].SetMarkerStyle(20)
    bmtfStd_list[i].SetMarkerColor(4)
    bmtfStd_list[i].SetLineColor(1)
    
    bmtf_list[i].SetMarkerStyle(20)
    bmtf_list[i].SetMarkerColor(1)
    bmtf_list[i].SetLineColor(1)


    kalman_list[i].SetMaximum( 1.3 * max(kalman_list[i].GetMaximum(),bmtf_list[i].GetMaximum()))
    bmtfStd_list[i].SetMaximum(1.3 * max(kalman_list[i].GetMaximum(),bmtf_list[i].GetMaximum()))
    bmtf_list[i].SetMaximum(   1.3 * max(kalman_list[i].GetMaximum(),bmtf_list[i].GetMaximum()))

    #kalman_list[i].SetMinimum(min(kalman_list[i].GetMinimum(),bmtf_list[i].GetMinimum()))
    #bmtf_list[i].SetMinimum(min(kalman_list[i].GetMinimum(),bmtf_list[i].GetMinimum()))

    
    if "Pt" in plotName_list[i] : 
        canvas.SetLogy()
        

    # gmt_list[i].Draw('EP')
    kalman_list[i].Draw('EP')
    bmtfStd_list[i].Draw('sameEP')
    bmtf_list[i].Draw('sameEP')
    
    
    
    # legend
    legend = TLegend(0.74,0.68,0.94,0.87)
    legend.AddEntry(kalman_list[i],"Kalman", "pl")
    # legend.AddEntry(gmt_list[i],"Gmt","pl")
    legend.AddEntry(bmtfStd_list[i],"BmtfStd","pl")
    legend.AddEntry(bmtf_list[i],"Bmtf","pl")
    legend.SetFillColor(kWhite)
    legend.SetLineColor(kBlack)
    legend.SetTextFont(43)
    legend.SetTextSize(20)
    legend.Draw()
    
    canvas.Update()
    
    canvas.SaveAs(OutputPath + "/" + plotName_list[i] + ".pdf")
    canvas.SaveAs(OutputPath + "/" + plotName_list[i] + ".png")
    
    
    
    
    
    
