#####################
# load samples 
#####################

import PhysicsTools.HeppyCore.framework.config as cfg
import os

# Load backgrounds
from CMGTools.XZZ2l2nu.samples.samples_13TeV_RunIISpring15MiniAODv2 import *
# Load signals
from CMGTools.XZZ2l2nu.samples.samples_13TeV_signal import *
# Load Data 
from CMGTools.XZZ2l2nu.samples.samples_13TeV_DATA2015 import *
# Load triggers
from CMGTools.XZZ2l2nu.samples.triggers_13TeV_Spring15 import *


# backgrounds
backgroundSamples = [
DYJetsToLL_M50_HT100to200,
DYJetsToLL_M50_HT200to400,
DYJetsToLL_M50_HT400to600,
DYJetsToLL_M50_HT600toInf,
WW,
WZ,
ZZ
]


# signals
signalSamples = [
RSGravToZZToZZinv_narrow_M-600,
RSGravToZZToZZinv_narrow_M-800,
RSGravToZZToZZinv_narrow_M-1000,
RSGravToZZToZZinv_narrow_M-1200,
RSGravToZZToZZinv_narrow_M-1400,
RSGravToZZToZZinv_narrow_M-1600,
RSGravToZZToZZinv_narrow_M-2000,
RSGravToZZToZZinv_narrow_M-2500,
RSGravToZZToZZinv_narrow_M-3000,
RSGravToZZToZZinv_narrow_M-3500,
RSGravToZZToZZinv_narrow_M-4500,
BulkGravToZZ_narrow_M-600,
BulkGravToZZ_narrow_M-800,
BulkGravToZZ_narrow_M-1000,
BulkGravToZZ_narrow_M-1200,
BulkGravToZZ_narrow_M-1400,
BulkGravToZZ_narrow_M-1600,
BulkGravToZZ_narrow_M-1800,
BulkGravToZZ_narrow_M-2000,
BulkGravToZZ_narrow_M-2500,
BulkGravToZZ_narrow_M-3000,
BulkGravToZZ_narrow_M-3500,
BulkGravToZZ_narrow_M-4000,
BulkGravToZZ_narrow_M-4500,
]

# mc samples
mcSamples = signalSamples + backgroundSamples



# data
SingleMuon=[SingleMuon_Run2015D_Promptv4,SingleMuon_Run2015D_05Oct]
SingleElectron=[SingleElectron_Run2015D_Promptv4,SingleElectron_Run2015D_05Oct]

for s in SingleMuon:
    s.triggers = triggers_1mu_noniso
    s.vetoTriggers = []
for s in SingleElectron:
    s.triggers = triggers_1e_noniso+triggers_1e
    s.vetoTriggers = triggers_1mu_noniso

dataSamples=SingleMuon+SingleElectron

# JSON
silverJson = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver.txt'
goldenJson = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt'

jsonFile = goldenJson


from CMGTools.XZZ2l2nu.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/XZZ2l2nu/data"

for comp in mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250
    comp.puFileMC=dataDir+"/pileup_MC.root"
    comp.puFileData=dataDir+"/pileup_DATA.root"
    comp.efficiency = eff2012
    comp.triggers=triggers_1mu_noniso+triggers_1e
    comp.globalTag = "Summer15_25nsV6_MC"

for comp in dataSamples:
    comp.splitFactor = 250
    comp.isMC = False
    comp.isData = True
    comp.json = jsonFile
    comp.globalTag = "Summer15_25nsV6_DATA"

