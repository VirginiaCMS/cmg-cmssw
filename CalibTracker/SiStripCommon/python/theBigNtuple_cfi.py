import FWCore.ParameterSet.Config as cms

from CalibTracker.SiStripCommon.ShallowEventDataProducer_cfi import *
from CalibTracker.SiStripCommon.ShallowClustersProducer_cfi import *
from CalibTracker.SiStripCommon.ShallowTrackClustersProducer_cfi import *
from CalibTracker.SiStripCommon.ShallowRechitClustersProducer_cfi import *
from CalibTracker.SiStripCommon.ShallowTracksProducer_cfi import *

shallowTree = cms.EDAnalyzer("ShallowTree",
                             outputCommands = cms.untracked.vstring(
    'drop *',
    'keep *_shallowEventRun_*_*',
    'keep *_shallowClusters_*_*',
    'keep *_shallowRechitClusters_*_*',
    'keep *_shallowTracks_*_*',
    'keep *_shallowTrackClusters_*_*'
    ))

theBigNtuple = cms.Sequence( (shallowEventRun +
                              shallowClusters +
                              shallowRechitClusters +
                              shallowTracks +
                              shallowTrackClusters) *
                             shallowTree
                             )
