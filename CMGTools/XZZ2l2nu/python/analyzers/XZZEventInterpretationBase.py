import random
import math
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsutils.JetReCalibrator import JetReCalibrator
from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg
#from CMGTools.XZZ2l2nu.tools.PyJetToolbox import *
from copy import copy



class XZZEventInterpretationBase( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(XZZEventInterpretationBase,self).__init__(cfg_ana, cfg_comp, looperName)
        self.selectPairLLNuNu = self.cfg_ana.selectPairLLNuNu
            
            
    def declareHandles(self):
        super(XZZEventInterpretationBase, self).declareHandles()


    def beginLoop(self, setup):
        super(XZZEventInterpretationBase,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('pass events')


    def process(self, event):
        self.readCollections( event.input )

            

        


                
                
