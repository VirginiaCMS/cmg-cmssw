from CMGTools.XZZ2l2nu.analyzers.XZZEventInterpretationBase import *
from CMGTools.XZZ2l2nu.tools.Pair import Pair
import itertools

class XZZMultiFinalState( XZZEventInterpretationBase ):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(XZZMultiFinalState,self).__init__(cfg_ana, cfg_comp, looperName)

    def process(self, event):
        super(XZZMultiFinalState,self).process(event)
        self.counters.counter('events').inc('all events')

        LLNuNu=[]

        # do LL+MET combination
        if len(event.LL)>0:
            #take the Z->ll  nearest to the Z mass and the highest pt jets
            bestZ = min(event.LL,key = lambda x: abs(x.M()-91.118))
            VV=Pair(bestZ,event.met)
            if self.selectPairLLNuNu(VV):
                selected = {'pair':VV}
                LLNuNu.append(selected)

        if len(LLNuNu)>0: 
             self.counters.counter('events').inc('pass events')

        setattr(event,'LLNuNu'+self.cfg_ana.suffix,LLNuNu)

