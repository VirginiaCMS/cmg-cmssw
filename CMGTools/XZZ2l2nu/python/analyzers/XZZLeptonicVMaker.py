import ROOT
import random
import math
from  itertools import combinations
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg
from CMGTools.XZZ2l2nu.tools.Pair import *


class XZZLeptonicVMaker( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(XZZLeptonicVMaker,self).__init__(cfg_ana, cfg_comp, looperName)
        self.selectMuMuPair = cfg_ana.selectMuMuPair
        self.selectElElPair = cfg_ana.selectElElPair
        self.selectVBoson = cfg_ana.selectVBoson

    def declareHandles(self):
        super(XZZLeptonicVMaker, self).declareHandles()


    def beginLoop(self, setup):
        super(XZZLeptonicVMaker,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('pass events')
        count.register('pass el events')
        count.register('pass mu events')

        
    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        self.n_pass_el = 0
        self.n_pass_mu = 0

        LL = []

        # electron pair
        for l1,l2 in combinations(event.selectedElectrons,2):
            if  (l1.pdgId() == -l2.pdgId() or l1.charge() == -l2.charge()):
                pair = Pair(l1,l2,23)
                if self.selectElElPair(pair):
                    LL.append(pair)
                    self.n_pass_el += 1
        # muon pair
        for l1,l2 in combinations(event.selectedMuons,2):
            #if  (l1.pdgId() == -l2.pdgId() and l1.charge() == -l2.charge()):
            #if  (l1.charge() == -l2.charge()):
            if  (l1.pdgId() == -l2.pdgId() or l1.charge() == -l2.charge()):
                pair = Pair(l1,l2,23)
                if self.selectMuMuPair(pair):
                    LL.append(pair)
                    self.n_pass_mu += 1

        # select V boson
        event.LL = [pair for pair in LL if self.selectVBoson(pair) ]

        if self.n_pass_el>0.1: 
            self.counters.counter('events').inc('pass el events')       
        if self.n_pass_mu>0.1: 
            self.counters.counter('events').inc('pass mu events')       
 
        if len(event.LL)<=0:
            return False

        self.counters.counter('events').inc('pass events') 
        return True



        
            

        


                
                
