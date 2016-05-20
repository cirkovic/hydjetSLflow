#!/bin/bash

JOBIDS="--jobids=1-11"

cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test

TEMP=`mktemp -d`
mkdir -p ${TEMP}/${1}/results
ln -sf ${TEMP}/${1}/results crab_projects/${1}/results

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

rm crab_projects/${1}/crab.log
crab getoutput -d crab_projects/${1} $JOBIDS

N=`ls crab_projects/${1}/results/ | wc -l`
BREAK=false
for i in `seq 1 10`; do
    rm crab_projects/${1}/crab.log
    crab getoutput -d crab_projects/${1} $JOBIDS
    if [ "`ls crab_projects/${1}/results/ | wc -l`" -gt "$N" ]; then
        N=`ls crab_projects/${1}/results/ | wc -l`
    else
        BREAK=true
    fi
    if [ "`ls crab_projects/${1}/results/*.root | wc -l`" -gt "0" ]; then
        hadd -k -f ${2}/`ls crab_projects/${1}/results/ | head -1`_${1} `ls crab_projects/${1}/results/*`
        mv ${2}/`ls crab_projects/${1}/results/ | head -1`_${1} ${2}/`ls crab_projects/${1}/results/ | head -1`
    fi
    if [[ $BREAK ]]; then
        break
    fi
done

