##########################################################
##      configuration for XZZ2l2nu 
##########################################################

import CMGTools.XZZ2l2nu.fwlite.Config as cfg
from CMGTools.XZZ2l2nu.fwlite.Config import printComps
from CMGTools.XZZ2l2nu.RootTools import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption


#Load all common analyzers
from CMGTools.VVResonances.analyzers.core_cff import *

#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.XZZ2l2nu.samples.loadSamples import *
selectedComponents = mcSamples+dataSamples

#-------- Analyzer
from CMGTools.XZZ2l2nu.analyzers.tree_cff import *

#-------- SEQUENCE
sequence = cfg.Sequence(coreSequence+[vvSkimmer,vvTreeProducer])


from CMGTools.XZZ2l2nu.samples.triggers_13TeV_Spring15 import *



################ old below

import PhysicsTools.HeppyCore.framework.config as cfg
#Load all analyzers
from CMGTools.XZZ2l2nu.analyzers.xzz2l2nuCore_modules_cff import * 


#-------- SAMPLES AND TRIGGERS -----------

#-------- SEQUENCE
from CMGTools.XZZ2l2nu.samples.samples_13TeV_Spring15 import *

selectedComponents = mcSamples + dataSamples
sequence = cfg.Sequence(hzz4lCoreSequence)

for comp in mcSamples:
    comp.triggers = []
    comp.vetoTriggers = []

from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
test = getHeppyOption('test')
if test == "1":
    comp = QQHZZ4L
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1 if getHeppyOption('single') else 5
    selectedComponents = [ comp ]
    if getHeppyOption('events'):
        eventSelector.toSelect = [ eval("("+x.replace(":",",")+")") for x in getHeppyOption('events').split(",") ]
        sequence = cfg.Sequence([eventSelector] + hzz4lCoreSequence)
        print "Will select events ",eventSelector.toSelect
elif test == '2':
    for comp in selectedComponents:
        comp.files = comp.files[:1]
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
elif test=="sync":
    comp = GGHZZ4L
    comp.name = 'HZZ4L'
    comp.files = [ 'root://eoscms.cern.ch//eos/cms'+X for X in (
         #'/store/mc/RunIISpring15DR74/GluGluHToZZTo4L_M125_13TeV_powheg_JHUgen_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/10000/00E6807C-9C16-E511-A165-0025905938A4.root',
         #'/store/cmst3/group/hzz/GluGluHToZZTo4L_M125_13TeV_powheg_JHUgen_pythia8_RunIISpring15DR74_Asympt25ns_MCRUN2_74_V9-v1_MINIAODSIM_00E6807C-9C16-E511-A165-0025905938A4.root',
         '/store/mc/RunIISpring15DR74/VBF_HToZZTo4L_M125_13TeV_powheg_JHUgen_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/68791C0A-3013-E511-88FD-D4AE5269F5FF.root', 
         '/store/mc/RunIISpring15DR74/WplusH_HToZZTo4L_M125_13TeV_powheg-minlo-HWJ_JHUgen_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/04BD6860-9F08-E511-8A80-842B2B1858FB.root',
         '/store/mc/RunIISpring15DR74/WminusH_HToZZTo4L_M125_13TeV_powheg-minlo-HWJ_JHUgen_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/70000/4A9FED55-DF0C-E511-A4B2-3417EBE6471D.root',
         '/store/mc/RunIISpring15DR74/ZH_HToZZ_4LFilter_M125_13TeV_powheg-minlo-HZJ_JHUgen_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/104B7067-0C02-E511-8FFB-0030487D07BA.root',
     # Sync on 7_4_X, miniAODv2 samples, with new FSR strategy 
        #'/store/mc/RunIISpring15MiniAODv2/VBF_HToZZTo4L_M125_13TeV_powheg_JHUgen_pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/3E964C5D-1D6E-E511-8B9A-0050560207C5.root',
        #'/store/mc/RunIISpring15MiniAODv2/WminusH_HToZZTo4L_M125_13TeV_powheg-minlo-HWJ_JHUgen_pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/D8CA6B54-056F-E511-BB1A-02163E014CE3.root',
        #'/store/mc/RunIISpring15MiniAODv2/WplusH_HToZZTo4L_M125_13TeV_powheg-minlo-HWJ_JHUgen_pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/D22BEE88-C26D-E511-B330-002590A81EF0.root',
        #'/store/mc/RunIISpring15MiniAODv2/ttH_HToZZ_4LFilter_M125_13TeV_powheg_JHUgen_pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/80000/84F62DD7-1475-E511-9F59-009C02AB98A6.root'
    )]
    #comp.splitFactor = 9
    #comp.fineSplitFactor = 1 if getHeppyOption('single') else 5
    comp.splitFactor = 1 if getHeppyOption('single') else 5
    selectedComponents = [ comp ]
    if getHeppyOption('events'):
        eventSelector.toSelect = [ eval("("+x.replace(":",",")+")") for x in getHeppyOption('events').split(",") ]
        sequence = cfg.Sequence([eventSelector] + hzz4lCoreSequence)
        print "Will select events ",eventSelector.toSelect

# the following is declared in case this cfg is used in input to the heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],  
                     events_class = Events)


