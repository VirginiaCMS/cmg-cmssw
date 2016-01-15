#!/usr/bin/env python

import ROOT

from CMGTools.XZZ2l2nu.plotting.TreePlotter import TreePlotter
from CMGTools.XZZ2l2nu.plotting.MergedPlotter import MergedPlotter
from CMGTools.XZZ2l2nu.plotting.StackPlotter import StackPlotter

ROOT.gROOT.ProcessLine('.x tdrstyle.C') 
tag='loosecut_'
cuts='(nllnunu)'
lumi=2.153
sepSig=True
LogY=True
TTbottom=True
if LogY: tag = tag+'log_'

vvPlotters=[]
vvSamples = ['WW','WZ','ZZ']

for sample in vvSamples:
    vvPlotters.append(TreePlotter(sample+'/vvTreeProducer/tree.root','tree'))
    vvPlotters[-1].setupFromFile(sample+'/skimAnalyzerCount/SkimReport.pck')
    vvPlotters[-1].addCorrectionFactor('xsec','tree')
    vvPlotters[-1].addCorrectionFactor('genWeight','tree')
    vvPlotters[-1].addCorrectionFactor('puWeight','tree')

VV = MergedPlotter(vvPlotters)
VV.setFillProperties(1001,ROOT.kMagenta)

zjetsPlotters=[]
#zjetsSamples = ['DYJetsToLL_M50_HT100to200','DYJetsToLL_M50_HT200to400','DYJetsToLL_M50_HT400to600','DYJetsToLL_M50_HT600toInf']
zjetsSamples = ['DYJetsToLL_M50']

for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(sample+'/vvTreeProducer/tree.root','tree'))
    zjetsPlotters[-1].setupFromFile(sample+'/skimAnalyzerCount/SkimReport.pck')
    zjetsPlotters[-1].addCorrectionFactor('xsec','tree')
    zjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
    zjetsPlotters[-1].addCorrectionFactor('puWeight','tree')

ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kGreen+2)

ttPlotters=[]
ttSamples = ['TTLep_pow']

for sample in ttSamples:
    ttPlotters.append(TreePlotter(sample+'/vvTreeProducer/tree.root','tree'))
    ttPlotters[-1].setupFromFile(sample+'/skimAnalyzerCount/SkimReport.pck')
    ttPlotters[-1].addCorrectionFactor('xsec','tree')
    ttPlotters[-1].addCorrectionFactor('genWeight','tree')
    ttPlotters[-1].addCorrectionFactor('puWeight','tree')

TT = MergedPlotter(ttPlotters)
TT.setFillProperties(1001,ROOT.kAzure-9)

sigPlotters=[]
sigSamples = [
'RSGravToZZToZZinv_narrow_M-800', 
'RSGravToZZToZZinv_narrow_M-1000', 
'RSGravToZZToZZinv_narrow_M-1200', 
#'RSGravToZZToZZinv_narrow_M-1400', 
#'RSGravToZZToZZinv_narrow_M-2000',
]
sigSampleNames = [
'RS800',
'RS1000',
'RS1200',
#'RS1400',
#'RS2000',
]

for sample in sigSamples:
    sigPlotters.append(TreePlotter(sample+'/vvTreeProducer/tree.root','tree'))
    sigPlotters[-1].setupFromFile(sample+'/skimAnalyzerCount/SkimReport.pck')
    sigPlotters[-1].addCorrectionFactor('xsec','tree')
    sigPlotters[-1].addCorrectionFactor('genWeight','tree')
    sigPlotters[-1].addCorrectionFactor('puWeight','tree')
    sigPlotters[-1].setFillProperties(0,ROOT.kWhite)


dataPlotters=[]
dataSamples = ['SingleElectron_Run2015D_05Oct','SingleElectron_Run2015D_v4','SingleMuon_Run2015D_05Oct','SingleMuon_Run2015D_v4']
for sample in dataSamples:
    dataPlotters.append(TreePlotter(sample+'/vvTreeProducer/tree.root','tree'))

Data = MergedPlotter(dataPlotters)




Stack = StackPlotter()
Stack.addPlotter(Data, "data_obs", "Data", "data")
if TTbottom: Stack.addPlotter(TT, "TT","TT", "background")
Stack.addPlotter(VV, "WWWZZZ","WW/WZ/ZZ", "background")
Stack.addPlotter(ZJets, "ZJets","Z+Jets", "background")
if not TTbottom: Stack.addPlotter(TT, "TT","TT", "background")


for i in range(len(sigSamples)):
  sigPlotters[i].setLineProperties(2,ROOT.kRed+i,2)
  Stack.addPlotter(sigPlotters[i],sigSampleNames[i],sigSampleNames[i],'signal')  

 
Stack.setLog(LogY)

Stack.drawStack('llnunu_mt', cuts, str(lumi*1000), 60, 0.0, 1200.0, titlex = "M_{T}", units = "GeV",output=tag+'out_mt_stack.eps',separateSignal=sepSig)
Stack.drawStack('met_pt', cuts, str(lumi*1000), 100, 0, 1000, titlex = "MET", units = "GeV",output=tag+'out_met_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_pt', cuts, str(lumi*1000), 75, 0.0, 1500.0, titlex = "P_{T}(Z)", units = "GeV",output=tag+'out_zpt_stack.eps',separateSignal=sepSig)
Stack.drawStack('met_pt', cuts, str(lumi*1000), 50, 0, 500, titlex = "MET", units = "GeV",output=tag+'out_met_low_stack.eps',separateSignal=sepSig)

Stack.drawStack('nVert', cuts, str(lumi*1000), 50, 0.0, 50.0, titlex = "N vertices", units = "",output=tag+'out_nVert_stack.eps',separateSignal=sepSig)

Stack.drawStack('llnunu_l1_eta', cuts, str(lumi*1000), 60, -3.0, 3.0, titlex = "#eta(Z) ", units = "",output=tag+'out_zeta_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_phi', cuts, str(lumi*1000), 64, -3.2, 3.2, titlex = "#phi(Z)", units = "",output=tag+'out_zphi_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_mass', cuts, str(lumi*1000), 50, 50, 150, titlex = "M(Z)", units = "GeV",output=tag+'out_zmass_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_mt', cuts, str(lumi*1000), 50, 0.0, 150.0, titlex = "M_{T}(Z)", units = "GeV",output=tag+'out_zmt_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_deltaPhi', cuts, str(lumi*1000), 50, 0.0, 5.0, titlex = "#Delta#phi", units = "",output=tag+'out_ZdeltaPhi_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_deltaR', cuts, str(lumi*1000), 50, 0.0, 5.0, titlex = "#Delta R", units = "",output=tag+'out_ZdeltaR_stack.eps',separateSignal=sepSig)

Stack.drawStack('llnunu_l2_phi', cuts, str(lumi*1000), 100, -3.2, 3.2, titlex = "#phi(MET)", units = "",output=tag+'out_metPhi_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l2_sumEt', cuts, str(lumi*1000), 80, 0.0, 2400.0, titlex = "sumE_{T}", units = "GeV",output=tag+'out_metSumEt_stack.eps',separateSignal=sepSig)

Stack.drawStack('llnunu_l1_l1_pt', cuts, str(lumi*1000), 100, 0.0, 1000.0, titlex = "P_{T}(l_{1})", units = "GeV",output=tag+'out_pTlep1_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_eta', cuts, str(lumi*1000), 60, -3.0, 3.0, titlex = "#eta(l_{1})", units = "",output=tag+'out_etalep1_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_phi', cuts, str(lumi*1000), 64, -3.2, 3.2, titlex = "#phi(l_{1})", units = "",output=tag+'out_philep1_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_miniRelIso', cuts, str(lumi*1000), 100, 0.0, 0.2, titlex = "miniISO_{rel}(l_{1})", units = "",output=tag+'out_miniISOlep1_stack.eps',separateSignal=sepSig)

Stack.drawStack('llnunu_l1_l2_pt', cuts, str(lumi*1000), 100, 0.0, 1000.0, titlex = "P_{T}(l_{2})", units = "GeV",output=tag+'out_pTlep2_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_eta', cuts, str(lumi*1000), 60, -3.0, 3.0, titlex = "#eta(l_{2})", units = "",output=tag+'out_etalep2_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_phi', cuts, str(lumi*1000), 64, -3.2, 3.2, titlex = "#phi(l_{2})", units = "",output=tag+'out_philep2_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_miniRelIso', cuts, str(lumi*1000), 100, 0.0, 0.2, titlex = "miniISO_{rel}(l_{2})", units = "",output=tag+'out_miniISOlep2_stack.eps',separateSignal=sepSig)


Stack.drawStack('llnunu_l1_l1_pt', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 100, 0.0, 1000.0, titlex = "P_{T}(#mu_{1})", units = "GeV",output=tag+'out_pTlep1_mu_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_eta', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 60, -3.0, 3.0, titlex = "#eta(#mu_{1})", units = "",output=tag+'out_etalep1_mu_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_phi', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 64, -3.2, 3.2, titlex = "#phi(#mu_{1})", units = "",output=tag+'out_philep1_mu_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_miniRelIso', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 100, 0.0, 0.2, titlex = "miniISO_{rel}(#mu_{1})", units = "",output=tag+'out_miniISOlep1_mu_stack.eps',separateSignal=sepSig)


Stack.drawStack('llnunu_l1_l2_pt', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 100, 0.0, 1000.0, titlex = "P_{T}(#mu_{2})", units = "GeV",output=tag+'out_pTlep2_mu_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_eta', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 60, -3.0, 3.0, titlex = "#eta(#mu_{2})", units = "",output=tag+'out_etalep2_mu_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_phi', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 64, -3.2, 3.2, titlex = "#phi(#mu_{2})", units = "",output=tag+'out_philep2_mu_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_miniRelIso', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 100, 0.0, 0.2, titlex = "miniISO_{rel}(#mu_{2})", units = "",output=tag+'out_miniISOlep2_mu_stack.eps',separateSignal=sepSig)

Stack.drawStack('llnunu_l1_l1_pt', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 100, 0.0, 1000.0, titlex = "P_{T}(e_{1})", units = "GeV",output=tag+'out_pTlep1_el_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_eta', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 60, -3.0, 3.0, titlex = "#eta(e_{1})", units = "",output=tag+'out_etalep1_el_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_phi', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 64, -3.2, 3.2, titlex = "#phi(e_{1})", units = "",output=tag+'out_philep1_el_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_miniRelIso', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 100, 0.0, 0.2, titlex = "miniISO_{rel}(e_{1})", units = "",output=tag+'out_miniISOlep1_el_stack.eps',separateSignal=sepSig)

Stack.drawStack('llnunu_l1_l2_pt', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 100, 0.0, 1000.0, titlex = "P_{T}(e_{2})", units = "GeV",output=tag+'out_pTlep2_el_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_eta', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 60, -3.0, 3.0, titlex = "#eta(e_{2})", units = "",output=tag+'out_etalep2_el_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_phi', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 64, -3.2, 3.2, titlex = "#phi(e_{2})", units = "",output=tag+'out_philep2_el_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l2_miniRelIso', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 100, 0.0, 0.2, titlex = "miniISO_{rel}(e_{2})", units = "",output=tag+'out_miniISOlep2_el_stack.eps',separateSignal=sepSig)


Stack.drawStack('llnunu_l1_l1_pt', cuts+"&&(abs(llnunu_l1_l1_pdgId)==13)", str(lumi*1000), 100, 45.0, 1000.0, titlex = "P_{T}(#mu_{1})", units = "GeV",output=tag+'out_pTlep1_mu_pthlt_stack.eps',separateSignal=sepSig)
Stack.drawStack('llnunu_l1_l1_pt', cuts+"&&(abs(llnunu_l1_l1_pdgId)==11)", str(lumi*1000), 100, 105.0, 1000.0, titlex = "P_{T}(e_{1})", units = "GeV",output=tag+'out_pTlep1_el_pthlt_stack.eps',separateSignal=sepSig)


