#!/bin/bash

cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test

TEMP=`mktemp -d`
mkdir -p ${TEMP}/${1}/results
ln -sf ${TEMP}/${1}/results crab_projects/${1}/results

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

while [[ true ]]; do
    rm crab_projects/${1}/crab.log
    crab getoutput -d crab_projects/${1}
    hadd -k -f ${2}/`ls crab_projects/${1}/results/ | head -1`_${1} `ls crab_projects/${1}/results/*`
    mv ${2}/`ls crab_projects/${1}/results/ | head -1`_${1} ${2}/`ls crab_projects/${1}/results/ | head -1`
done

