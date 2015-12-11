##########################################################
##       GENERIC SUSY TREE PRODUCTION CONFIG.           ##
## no skim is applied in this configuration, as it is   ##
## meant only to check that all common modules run ok   ##
##########################################################


import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.RootTools.RootTools import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#Load all common analyzers
from CMGTools.VVres2l2v.analyzers.core_cff import * 

#-------- SAMPLES AND TRIGGERS -----------
#from CMGTools.VVres2l2v.samples.loadSamples import *
from CMGTools.VVres2l2v.samples.signal_13TeV_74X import *
from CMGTools.TTHAnalysis.setup.Efficiencies import *
#load triggers
from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
dataDir = "$CMSSW_BASE/src/CMGTools/VVres2l2v/data"
selectedComponents = signalSamples
for comp in signalSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 20
    comp.puFileMC=dataDir+"/pileup_MC.root"
    comp.puFileData=dataDir+"/pileup_DATA.root"
    comp.efficiency = eff2012
    comp.triggers=triggers_1mu_noniso+triggers_1mu_iso+triggers_1e+triggers_1e_noniso+triggers_HT800+triggers_HT900+triggers_dijet_fat+triggers_met90_mht90+triggers_metNoMu90_mhtNoMu90+triggers_metNoMu120_mhtNoMu120
    comp.globalTag = "Summer15_25nsV6_MC"

#selectedComponents = mcSamples+dataSamples
#selectedComponents = dataSamples

#-------- Analyzer
from CMGTools.VVres2l2v.analyzers.tree_cff import * 

#-------- SEQUENCE

coreSequence = [
   #eventSelector,
#    jsonAna,
#    triggerAna,
    pileUpAna,
#    genAna,
#    pdfwAna,
    vertexAna,
    lepAna
]


sequence = cfg.Sequence(coreSequence+[vvSkimmer,vvTreeProducer])
print sequence

#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *


# triggerFlagsAna.triggerBits ={
#     "ISOMU":triggers_1mu_iso,
#     "MU":triggers_1mu_noniso,
#     "ISOELE":triggers_1e,
#     "ELE":triggers_1e_noniso,
#     "HT800":triggers_HT800,
#     "HT900":triggers_HT900,
#     "JJ":triggers_dijet_fat,  
#     "MET90":triggers_met90_mht90+triggers_metNoMu90_mhtNoMu90,
#     "MET120":triggers_metNoMu120_mhtNoMu120
# }


#-------- HOW TO RUN
test = 0
if test==1:
    # test a single component, using a single thread.
    selectedComponents = [VBF_RadionToZZ_narrow_4500]
    for c in selectedComponents:
        c.files = c.files[:1]
        c.splitFactor = 1
elif test==2:    
    # test all components (1 thread per component).
    selectedComponents = [BulkGravToWW_narrow_2500]
    for comp in selectedComponents:
        comp.splitFactor = 1
#        comp.files = comp.files[:1]
elif test==3:    
    # test all components (1 thread per component).
    selectedComponents = [DYJetsToLL_M50_HT600toInf]
    for comp in selectedComponents:
        comp.splitFactor = 1

elif test==4:    
    # test all components (1 thread per component).
    selectedComponents = [RSGravToWWToLNQQ_kMpl01_4500]
    for comp in selectedComponents:
        comp.splitFactor = 20

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='vvTreeProducer/tree.root',
    option='recreate'
    )    
outputService.append(output_service)



from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload
event_class = Events
if getHeppyOption("nofetch"):
    event_class = Events 
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],  
                     events_class = event_class)

print config
