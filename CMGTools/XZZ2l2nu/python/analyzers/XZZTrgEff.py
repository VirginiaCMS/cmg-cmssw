from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from ROOT import TFile,TH1F
class TrgEffHists(object):
    def __init__(self, filename):
        self.file=TFile(filename,'recreate')
        self.dRmunoHLT=TH1F('dRmunoHLT','deltaR with mu no HLT',6,0,1.2)
        self.dRelnoHLT=TH1F('dRelnoHLT','deltaR with ele no HLT',6,0,1.2)
        self.dRmuHLT=TH1F('dRmuHLT','deltaR with muon HLT',6,0,1.2)
        self.dRmuHLTmatch=TH1F('dRmuHLTmatch','deltaR with muon HLT matching',6,0,1.2)
        self.dRelHLT=TH1F('dRelHLT','deltaR with ele HLT',6,0,1.2)
        self.dRelHLTmatch=TH1F('dRelHLTmatch','deltaR with ele HLT matching',6,0,1.2)
    def write(self):
        self.file.Write()

def deltR(l1,l2):
    pi=3.1415926536
    de=l1.eta()-l2.eta()
    dp=l1.phi()-l2.phi()
    while dp>pi: dp-=2*pi
    while dp<-pi: dp+=2*pi
    return (de**2+dp**2)**.5

class XZZTrgEff(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(XZZTrgEff, self).__init__(cfg_ana, cfg_comp, looperName)
        self.trgeff=TrgEffHists('/'.join([self.dirName,'trgeff.root']))
        self.eleHLT=cfg_ana.eleHLT
        self.muHLT=cfg_ana.muHLT
    def declareHandles(self):
        super(XZZTrgEff, self).declareHandles()
        self.handles['trgresults']=AutoHandle(("TriggerResults","","HLT"),"edm::TriggerResults")
        self.handles['selectedtrg']=AutoHandle('selectedPatTrigger','std::vector<pat::TriggerObjectStandAlone>')
    def beginLoop(self,setup):
        super(XZZTrgEff,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('events with mu no HLT')
        count.register('events with ele no HLT')
        count.register('events pass mu HLT')
        count.register('events pass mu HLT and matching')
        count.register('events pass ele HLT')
        count.register('events pass ele HLT and matching')
    def process(self,event):
        self.readCollections( event.input )
        Zll = min(event.LL,key = lambda x: abs(x.M()-91.118))
        deltr = deltR(Zll.leg1,Zll.leg2)
        names = event.input.object().triggerNames(self.handles['trgresults'].product())
        eleob=[]
        muob=[]
        for i in self.handles['selectedtrg'].product():
            i.unpackPathNames(names)
            pNames=list(i.pathNames())
            if [pN for pN in pNames if self.eleHLT in pN]:eleob.append(i)
            if [pN for pN in pNames if self.muHLT in pN]:muob.append(i)
        if abs(Zll.leg1.pdgId())==11:
            self.trgeff.dRelnoHLT.Fill(deltr)
            self.counters.counter('events').inc('events with ele no HLT')
            if eleob:
                self.trgeff.dRelHLT.Fill(deltr)
                self.counters.counter('events').inc('events pass ele HLT')
                lmatch=[1 for i in eleob if deltR(Zll.leg1,i)<.3]+[1 for i in eleob if deltR(Zll.leg2,i)<.3]
                if lmatch:
                    self.trgeff.dRelHLTmatch.Fill(deltr)
                    self.counters.counter('events').inc('events pass ele HLT and matching')
        if abs(Zll.leg1.pdgId())==13:
            self.trgeff.dRmunoHLT.Fill(deltr)
            self.counters.counter('events').inc('events with mu no HLT')
            if muob:
                self.trgeff.dRmuHLT.Fill(deltr)
                self.counters.counter('events').inc('events pass mu HLT')
                lmatch=[1 for i in muob if deltR(Zll.leg1,i)<.3]+[1 for i in muob if deltR(Zll.leg2,i)<.3]
                if lmatch:
                    self.trgeff.dRmuHLTmatch.Fill(deltr)
                    self.counters.counter('events').inc('events pass mu HLT and matching')
        return True
    def write(self,setup):
        super(XZZTrgEff, self).write(setup)
        self.trgeff.write()

