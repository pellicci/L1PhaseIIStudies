#! /usr/bin/env python

# *******************
# usage: ./kalmanComparison.py -f results/input_file.root
# *******************


import sys
import os
import argparse
import ROOT
from ROOT import gSystem, TFile, gPad, TCanvas, TLegend, kWhite, kBlack, kGreen


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

kalman_list        = []
kalmanAll_list     = []
kalmanAllName_list = []   # cross check list
gmt_list           = []
bmtfStd_list       = []
bmtfStdName_list   = []   # cross check list
bmtf_list          = []
plotName_list      = []   # needed also for naming final plots


for hname in names_list : 

    if "Chi2" in hname : continue    # will not store Chi2 plot since by now it is only in kalman lists

    if "_ER" in hname :
        if "_gmt" in hname :
            gmt_list.append(histos_dict[hname])
        elif "_bmtf" in hname :
            if "_Std" in hname : 
                bmtfStd_list.append(histos_dict[hname])
                bmtfStdName_list.append(hname) 
            else :
                bmtf_list.append(histos_dict[hname])
        elif "_All" in hname :
            kalmanAll_list.append(histos_dict[hname])
            kalmanAllName_list.append(hname) 
        else :
            kalman_list.append(histos_dict[hname])
            plotName_list.append(hname) 
        

print plotName_list
print bmtfStdName_list
print kalmanAllName_list


# draw plots
for i in range(len(plotName_list)) :            # will not plot plots which are only in the bmtfStd list


    canvas = TCanvas()
    canvas.cd()

    # gmt_list[i].SetMarkerStyle(20)
    # gmt_list[i].SetMarkerColor(1)
    # gmt_list[i].SetLineColor(1)

    kalman_list[i].SetMarkerStyle(20)
    kalman_list[i].SetMarkerColor(2)
    kalman_list[i].SetLineColor(2)

    kalmanAll_list[i].SetMarkerStyle(20)
    kalmanAll_list[i].SetMarkerColor(kGreen+2)
    kalmanAll_list[i].SetLineColor(kGreen+3)

    bmtfStd_list[i].SetMarkerStyle(20)
    bmtfStd_list[i].SetMarkerColor(4)
    bmtfStd_list[i].SetLineColor(1)
    
    bmtf_list[i].SetMarkerStyle(20)
    bmtf_list[i].SetMarkerColor(1)
    bmtf_list[i].SetLineColor(1)


    kalman_list[i].SetMaximum(   1.5 * max(kalman_list[i].GetMaximum(),kalmanAll_list[i].GetMaximum(),bmtfStd_list[i].GetMaximum(),bmtf_list[i].GetMaximum()))
    kalmanAll_list[i].SetMaximum(1.5 * max(kalman_list[i].GetMaximum(),kalmanAll_list[i].GetMaximum(),bmtfStd_list[i].GetMaximum(),bmtf_list[i].GetMaximum()))
    bmtfStd_list[i].SetMaximum(  1.5 * max(kalman_list[i].GetMaximum(),kalmanAll_list[i].GetMaximum(),bmtfStd_list[i].GetMaximum(),bmtf_list[i].GetMaximum()))
    bmtf_list[i].SetMaximum(     1.5 * max(kalman_list[i].GetMaximum(),kalmanAll_list[i].GetMaximum(),bmtfStd_list[i].GetMaximum(),bmtf_list[i].GetMaximum()))

    #kalman_list[i].SetMinimum(min(kalman_list[i].GetMinimum(),bmtf_list[i].GetMinimum()))
    #bmtf_list[i].SetMinimum(min(kalman_list[i].GetMinimum(),bmtf_list[i].GetMinimum()))

    
    if "Pt" in plotName_list[i] : 
        canvas.SetLogy()

    # if "Chi2" in plotName_list[i] : 
    #     canvas.SetLogx()
        

    # gmt_list[i].Draw('EP')
    kalman_list[i].Draw('EP')
    kalmanAll_list[i].Draw('sameEP')
    bmtfStd_list[i].Draw('sameEP')
    bmtf_list[i].Draw('sameEP')
    
    
    
    # legend
    legend = TLegend(0.80,0.74,0.99,0.91)
    legend.AddEntry(kalman_list[i],"Kalman Cleaned", "pl")
    legend.AddEntry(kalmanAll_list[i],"Kalman All", "pl")
    # legend.AddEntry(gmt_list[i],"Gmt","pl")
    legend.AddEntry(bmtfStd_list[i],"BmtfStd","pl")
    legend.AddEntry(bmtf_list[i],"Bmtf","pl")
    legend.SetFillColor(kWhite)
    legend.SetLineColor(kBlack)
    legend.SetTextFont(43)
    legend.SetTextSize(14)#20
    legend.Draw()
    
    canvas.Update()
    
    canvas.SaveAs(OutputPath + "/" + plotName_list[i] + ".pdf")
    canvas.SaveAs(OutputPath + "/" + plotName_list[i] + ".png")
    
    
    
    
    
    
