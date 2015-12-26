from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsutils.genutils import *
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters

class XZZGenAnalyzer( Analyzer ):
    """ Only select X->ZZ->2l2nu events

       """

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(XZZGenAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

        self.filter = getattr(self.cfg_ana, 'filter', "None")
 
    def declareHandles(self):
        super(XZZGenAnalyzer, self).declareHandles()
        self.mchandles['genParticles'] = AutoHandle( 'prunedGenParticles', 'std::vector<reco::GenParticle>' )
                
    def beginLoop(self,setup):
        super(XZZGenAnalyzer,self).beginLoop(setup)

        self.counters.addCounter('XZZGenReport')
        self.count = self.counters.counter('XZZGenReport')
        self.count.register('XZZ2l2nu Events')
        self.count.register('XZZ2l2j Events')
        self.count.register('pass events')


    def makeMCInfo(self, event):
        verbose = getattr(self.cfg_ana, 'verbose', False)
        rawGenParticles = self.mchandles['genParticles'].product() 

        selectedGenParticles = []
        event.genZBosons = []
        event.genLeptons = []
        event.genElectrons = []
        event.genMuons = []
        event.genNeutrinos = []
        event.genJets = []

        event.genZBosons = [ p for p in rawGenParticles if (p.pdgId() == 23) and p.numberOfDaughters() > 0 and abs(p.daughter(0).pdgId()) != 23 ]

        for zboson in event.genZBosons:
            selectedGenParticles.append(zboson)
            for i in xrange( zboson.numberOfDaughters() ):
                dau = zboson.daughter(i)
                dauid = dau.pdgId()
                if abs(dauid) in [11,13]:
                    event.genLeptons.append(dau)
                    selectedGenParticles.append(dau)
                    if abs(dauid)==11: event.genElectrons.append(dau)
                    if abs(dauid)==13: event.genMuons.append(dau)
                elif abs(dauid) in [12,14,16]:
                    event.genNeutrinos.append(dau)
                    selectedGenParticles.append(dau)
                elif abs(dauid) in range(7):
                    event.genJets.append(dau)
 
        event.genParticles = selectedGenParticles    
        
        if len(event.genZBosons)>=2 and len(event.genLeptons)>=2 and len(event.genNeutrinos)>=2:
            event.genIsXZZ2l2nu = True
        else: 
            event.genIsXZZ2l2nu = False
 
        if len(event.genZBosons)>=2 and len(event.genLeptons)>=2 and len(event.genJets)>=2:
            event.genIsXZZ2l2j = True
        else:
            event.genIsXZZ2l2j = False


        if event.genIsXZZ2l2nu:
            self.count.inc('XZZ2l2nu Events') 

        if event.genIsXZZ2l2j:
            self.count.inc('XZZ2l2j Events')

        if self.cfg_ana.verbose and event.genIsXZZ2l2nu:
            print "N gen Z bosons: "+str(len(event.genZBosons))
            print "N gen Leptons: "+str(len(event.genLeptons))
            print "N gen neutrinos: "+str(len(event.genNeutrinos))

    def process(self, event):
        self.readCollections( event.input )

        # if not MC, nothing to do
        if not self.cfg_comp.isMC: 
            return True
        # do MC level analysis
        self.makeMCInfo(event)
        
        # no gen filter
        if self.filter == "None":
            return True
        # filter
        if self.filter=="ZZ2mu":
            if len(event.genMuons)>=2: 
                self.count.inc('pass events')
                return True
        elif self.filter=="ZZ2el":
            if len(event.genElectrons)>=2:
                self.count.inc('pass events')
                return True
        elif self.filter=="ZZ2l2nu":
            if event.genIsXZZ2l2nu:
                self.count.inc('pass events')
                return True

        # false if use filter but not pass any
        return False


import PhysicsTools.HeppyCore.framework.config as cfg
setattr(XZZGenAnalyzer,"defaultConfig",
    cfg.Analyzer(XZZGenAnalyzer,
        # Print out debug information
        verbose = False,
    )
)
