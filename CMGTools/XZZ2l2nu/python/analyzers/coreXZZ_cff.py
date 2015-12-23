import os
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.all import *
from PhysicsTools.Heppy.analyzers.objects.all import *
from PhysicsTools.Heppy.analyzers.gen.all import *
from PhysicsTools.HeppyCore.utils.deltar import *
from CMGTools.XZZ2l2nu.analyzers.Skimmer import *
from CMGTools.XZZ2l2nu.analyzers.XZZLeptonicVMaker import *
from CMGTools.XZZ2l2nu.analyzers.PackedCandidateLoader import *
from CMGTools.XZZ2l2nu.analyzers.XZZMultiFinalState  import *
from CMGTools.XZZ2l2nu.tools.leptonID  import *
from CMGTools.XZZ2l2nu.analyzers.XZZGenAnalyzer import *
from CMGTools.XZZ2l2nu.analyzers.XZZLeptonAnalyzer import *
from CMGTools.XZZ2l2nu.analyzers.XZZTriggerBitFilter import *
from CMGTools.XZZ2l2nu.analyzers.XZZVertexAnalyzer import *
from CMGTools.XZZ2l2nu.analyzers.XZZMETAnalyzer import *

###########################
# define analyzers
###########################

skimAnalyzer = cfg.Analyzer(
    SkimAnalyzerCount, name='skimAnalyzerCount',
    useLumiBlocks = False,
    )

# Apply json file (if the dataset has one)
jsonAna = cfg.Analyzer(
    JSONAnalyzer, name="JSONAnalyzer",
    )

# Filter using the 'triggers' and 'vetoTriggers' specified in the dataset
triggerAna = cfg.Analyzer(
    XZZTriggerBitFilter, name="TriggerBitFilter",
    )

# This analyzer actually does the pile-up reweighting (generic)
pileUpAna = cfg.Analyzer(
    PileUpAnalyzer, name="PileUpAnalyzer",
    true = True,  # use number of true interactions for reweighting
    makeHists=False
    )


## Gen Info Analyzer 
genAna = cfg.Analyzer(
    XZZGenAnalyzer, name="XZZGenAnalyzer",
    # Print out debug information
    verbose = False,
    )

# Select a list of good primary vertices (generic)
vertexAna = cfg.Analyzer(
    XZZVertexAnalyzer, name="VertexAnalyzer",
    vertexWeight = None,
    fixedWeight = 1,
    verbose = False
    )

lepAna = cfg.Analyzer(
    XZZLeptonAnalyzer, name="leptonAnalyzer",
    muons='slimmedMuons',
    electrons='slimmedElectrons',
    packedCandidates = 'packedPFCandidates',
    rhoMuon= 'fixedGridRhoFastjetCentralNeutral',
    rhoElectron = 'fixedGridRhoFastjetCentralNeutral',
    applyMiniIso = True,
    mu_isoCorr = "rhoArea" ,
    ele_isoCorr = "rhoArea" ,
    mu_effectiveAreas = "Spring15_25ns_v1",
    ele_effectiveAreas = "Spring15_25ns_v1",
    miniIsolationPUCorr = None, # Allowed options: 'rhoArea' (EAs for 03 cone scaled by R^2), 'deltaBeta', 
                                     # 'raw' (uncorrected), 'weights' (delta beta weights; not validated)
                                     # Choose None to just use the individual object's PU correction
)

metAna = cfg.Analyzer(
    XZZMETAnalyzer, name="metAnalyzer",
    metCollection     = "slimmedMETs",
    noPUMetCollection = "slimmedMETs",
    copyMETsByValue = False,
    doTkMet = False,
    doMetNoPU = True,
    doMetNoMu = False,
    doMetNoEle = False,
    doMetNoPhoton = False,
    recalibrate = False, # or "type1", or True
    applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer
    old74XMiniAODs = False, # set to True to get the correct Raw MET when running on old 74X MiniAODs
    jetAnalyzerPostFix = "",
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "",
    )


leptonicVAna = cfg.Analyzer(
    XZZLeptonicVMaker,
    name='leptonicVMaker',
    selectMuMuPair = (lambda x: x.leg1.pt()>50.0 and abs(x.leg1.eta())<2.1 
                      and x.leg2.pt()>20.0 and abs(x.leg2.eta())<2.4 
                      and x.mass()>60.0 and x.mass()<120.0 and x.pt()>200.0 ),
    selectElElPair = (lambda x: x.leg1.pt()>115.0 and abs(x.leg1.eta())<2.5 
                      and x.leg2.pt()>35.0 and abs(x.leg2.eta())<2.5 
                      and x.mass()>60.0 and x.mass()<120.0 and x.pt()>200.0 ),
    )

packedAna = cfg.Analyzer(
    PackedCandidateLoader,
    name = 'PackedCandidateLoader',
    select=lambda x: x.pt()<13000.0
    )

multiStateAna = cfg.Analyzer(
    XZZMultiFinalState,
    name='MultiFinalStateMaker',
    ktPowerFat = -1.0,
    rFat = 0.8,
    massdrop=True,
    subjets=2,
    doCHS = True,
    prunning=True,
    softdrop = True,
    softdrop_beta=0.0,
    softdrop_zeta=0.1,
    selectFat = (lambda x: x.pt()>200.0 and abs(x.eta())<2.4 and x.prunedJet.mass()>0.0 and len(x.subjets)>1 and x.looseID),
    ktPower=-1.0,
    r = 0.4,
    selectPairLL = (lambda x:  x.mass()>0 and x.deltaPhi()>1.5 and x.leg1.pt()>200  and ((abs(x.leg1.leg1.pdgId())==11 and max(x.leg1.leg1.pt(),x.leg1.leg2.pt())>80) or (abs(x.leg1.leg1.pdgId())==13 and max(x.leg1.leg1.pt(),x.leg1.leg2.pt())>50))),
    selectPairLNu = (lambda x: x.deltaPhi()>1.5 and x.leg1.pt()>200 and ((abs(x.leg1.leg1.pdgId())==11 and x.leg1.leg2.pt()>80) or (abs(x.leg1.leg1.pdgId())==13 and x.leg1.leg2.pt()>40))),
    selectPairJJ = (lambda x:  x.mass()>1000 and x.leg1.tightID and x.leg2.tightID),
    selectPairJJNuNu = (lambda x: x.leg1.pt()>200 and x.deltaPhi()>1.5 ),
    selectPairLLNuNu = (lambda x: x.leg1.pt()>200 ),
    suffix = '',
    recalibrateJets = True, # True, False, 'MC', 'Data'
    recalibrationType = "AK4PFchs",
    recalibrationTypeFAT = "AK8PFchs",
    jecPath = "%s/src/CMGTools/RootTools/data/jec/" % os.environ['CMSSW_BASE'],
    shiftJEC = 0, # set to +1 or -1 to get +/-1 sigma shifts
    rho = ('fixedGridRhoFastjetAll','',''),
    attachBTag = True,
    btagDiscriminator = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
    standardJets = 'slimmedJets',
    fatJets = 'slimmedJetsAK8',
    subJets = 'slimmedJetsAK8PFCHSSoftDropPacked',
    doSkim = True
    )

# Create flags for MET filter bits

eventFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="EventFlags",
    processName = 'PAT',
    fallbackProcessName = 'RECO',
    outprefix   = 'Flag',
    triggerBits = {
        "HBHENoiseFilter" : [ "Flag_HBHENoiseFilter" ],
        "HBHENoiseIsoFilter" : [ "Flag_HBHENoiseIsoFilter" ],
        "CSCTightHaloFilter" : [ "Flag_CSCTightHaloFilter" ],
        "hcalLaserEventFilter" : [ "Flag_hcalLaserEventFilter" ],
        "EcalDeadCellTriggerPrimitiveFilter" : [ "Flag_EcalDeadCellTriggerPrimitiveFilter" ],
        "goodVertices" : [ "Flag_goodVertices" ],
        "trackingFailureFilter" : [ "Flag_trackingFailureFilter" ],
        "eeBadScFilter" : [ "Flag_eeBadScFilter" ],
        "ecalLaserCorrFilter" : [ "Flag_ecalLaserCorrFilter" ],
        "trkPOGFilters" : [ "Flag_trkPOGFilters" ],
        "trkPOG_manystripclus53X" : [ "Flag_trkPOG_manystripclus53X" ],
        "trkPOG_toomanystripclus53X" : [ "Flag_trkPOG_toomanystripclus53X" ],
        "trkPOG_logErrorTooManyClusters" : [ "Flag_trkPOG_logErrorTooManyClusters" ],
        "METFilters" : [ "Flag_METFilters" ],
    }
    )

# Create flags for trigger bits
triggerFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="TriggerFlags",
    processName = 'HLT',
    triggerBits = {
    }
    )



################
coreSequence = [
    skimAnalyzer,
    jsonAna,
    triggerAna,
    pileUpAna,
    genAna,
    vertexAna,
    lepAna,
    metAna,
    leptonicVAna,
#    packedAna,
    multiStateAna,
    eventFlagsAna,
    triggerFlagsAna
]

###################




