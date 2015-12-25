#!/bin/sh

#http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH

pip install --install-option="--prefix=$HOME/.local" brilws

pip show brilws

brilcalc -h

briltag -h

brilcalc lumi -h

brilcalc beam -h


