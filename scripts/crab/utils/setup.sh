#!/bin/bash
# source /cvmfs/cms.cern.ch/cmsset_default.sh
# export SCRAM_ARCH=slc6_amd64_gcc530
# eval `scramv1 runtime -sh`
.  /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init -voms cms --valid 79:00
# If you have certificate difficulties, maybe worth trying: export X509_USER_PROXY=/tmp/x509up_u26160
