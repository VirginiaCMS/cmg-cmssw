import os
import PhysicsTools.HeppyCore.framework.config as cfg
from CMGTools.VVres2l2v.utils.miniAodFiles import miniAodFiles

# input component 
# several input components can be declared,
# and added to the list of selected components

# add component creator to have the list of files
from CMGTools.VVres2l2v.samples.signal_13TeV_74X import *

# inputSample = cfg.Component(
#     'test_signal_component',
#     files = miniAodFiles(),
#     )
#inputSample.isMC = True
#inputSample.splitFactor = 2 

selectedComponents  = signalSamples #[inputSample]
for comp in signalSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 1
#    comp.puFileMC=dataDir+"/pileup_MC.root"
#    comp.puFileData=dataDir+"/pileup_DATA.root"
#    comp.efficiency = eff2012
#    comp.triggers=triggers_1mu_noniso+triggers_1mu_iso+triggers_1e+triggers_1e_noniso+triggers_HT800+triggers_HT900+triggers_dijet_fat+triggers_met90_mht90+triggers_metNoMu90_mhtNoMu90+triggers_metNoMu120_mhtNoMu120
    comp.globalTag = "Summer15_25nsV6_MC"

from PhysicsTools.Heppy.analyzers.examples.SimpleJetAnalyzer import SimpleJetAnalyzer
jets = cfg.Analyzer(
    SimpleJetAnalyzer,
    'jets',
    ptmin = 30. 
    )

from PhysicsTools.Heppy.analyzers.examples.SimpleTreeAnalyzer import SimpleTreeAnalyzer
tree = cfg.Analyzer(
    SimpleTreeAnalyzer
    )


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    jets,
    tree
    ] )

# finalization of the configuration object. 
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
                     sequence = sequence, 
                     services = [],
                     events_class = Events)

print config

