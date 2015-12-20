from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
#from PhysicsTools.Heppy.physicsutils.genutils import isNotFromHadronicShower, realGenMothers, realGenDaughters

class XZZGenAnalyzer( Analyzer ):
    """ Only select X->ZZ->2l2nu events

       """

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(XZZGenAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
 
    def declareHandles(self):
        super(XZZGenAnalyzer, self).declareHandles()
        self.mchandles['genParticles'] = AutoHandle( 'prunedGenParticles', 'std::vector<reco::GenParticle>' )
                
    def beginLoop(self,setup):
        super(XZZGenAnalyzer,self).beginLoop(setup)


    def fillGenLeptons(self, event, particle, isTau=False, sourceId=25):
        """Get the gen level light leptons (prompt and/or from tau decays)"""

        for i in xrange( particle.numberOfDaughters() ):
            dau = GenParticle(particle.daughter(i))
            dau.sourceId = sourceId
            id = abs(dau.pdgId())
            moid = 0;
            if dau.numberOfMothers() > 0:
                moid = abs(dau.mother().pdgId())
            if id in [11,13]:
                event.genLeptons.append(dau)
            elif id in [12,14]:
                event.genNeutrinos.append(dau)

    def makeMCInfo(self, event):
        verbose = getattr(self.cfg_ana, 'verbose', False)
        rawGenParticles = self.mchandles['genParticles'].product() 
        
        event.genZBosons = []
        event.genLeptons = []
        event.genNeutrinos = []
        
        event.genZBosons = [ p for p in event.genParticles if (p.pdgId() == 23) and p.numberOfDaughters() > 0 and abs(p.daughter(0).pdgId()) != 23 ]

        for zboson in event.genZBosons:
            for i in xrange( zboson.numberOfDaughters() ):
                dau = GenParticle(zboson.daughter(i))
                dau.sourceId = zboson.pdgId()
                if id in [11,13]:
                    event.genLeptons.append(dau)
                elif id in [12,14]:
                    event.genNeutrinos.append(dau)
     

        if self.cfg_ana.verbose:
            print "N gen Z bosons: "+event.genZBosons.size()
            print "N gen Leptons: "+event.genLeptons.size()
            print "N gen neutrinos: "+event.genNeutrinoss.size()

    def process(self, event):
        self.readCollections( event.input )

        # if not MC, nothing to do
        if not self.cfg_comp.isMC: 
            return True
        # do MC level analysis
        self.makeMCInfo(event)
        return True

import PhysicsTools.HeppyCore.framework.config as cfg
setattr(XZZGenAnalyzer,"defaultConfig",
    cfg.Analyzer(XZZGenAnalyzer,
        # Print out debug information
        verbose = False,
    )
)
