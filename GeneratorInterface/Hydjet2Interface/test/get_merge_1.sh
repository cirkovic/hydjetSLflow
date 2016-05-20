#!/bin/bash

cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test

TEMP=`mktemp -d`
mkdir -p ${TEMP}/${1}/results
ln -sf ${TEMP}/${1}/results crab_projects/${1}/results

echo "CIRKOVIC begin"
pwd
echo ${1}
echo ${TMP}
ls -latr ${TEMP}/${1}
ls -latr crab_projects/${1}/results
pwd
echo "CIRKOVIC end"

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

echo crab_projects/${1}
echo crab getoutput -d crab_projects/${1}
which crab

while [[ true ]]; do
    echo crab getoutput -d crab_projects/${1}
    crab getoutput -d crab_projects/${1}
    exit
    if (( `ls crab_projects/${i}/results/ | wc -l` > 2000 )); then
        break
    fi
    sleep 60;
done

hadd -k -f output_batch/`ls crab_projects/${1}/results/ | head -1` `ls crab_projects/${1}/results/*`

