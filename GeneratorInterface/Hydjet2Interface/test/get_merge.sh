#!/bin/bash

cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test

TEMP=`mktemp -d`
mkdir -p ${TEMP}/${1}/results
ln -sf ${TEMP}/${1}/results crab_projects/${1}/results

#echo "CIRKOVIC begin"
#pwd
#echo ${1}
#echo ${TMP}
#ls -latr ${TEMP}/${1}
#ls -latr crab_projects/${1}/results
##pwd
#echo "CIRKOVIC end"

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

#echo crab_projects/${1}
#echo crab getoutput -d crab_projects/${1}
#crab getoutput -d crab_projects/${1} --jobids=1-11
#which crab
#/cvmfs/cms.cern.ch/crab3/slc6_amd64_gcc493/cms/crabclient/3.3.1606-comp/bin/crab getoutput -d crab_projects/${1} --jobids=1-11

#exit
N=10
LOOP=true
JOBIDS="--jobids=1-11"
while [[ $LOOP ]]; do
    for i in `seq 1 60`; do
        crab getoutput -d crab_projects/${1} $JOBIDS
        if [ "`ls crab_projects/${1}/results/ | wc -l`" -gt "$N" ]; then
            N=`ls crab_projects/${1}/results/ | wc -l`
            break
        fi
        echo WAITING...
        sleep 60;
    done

    hadd -k -f output_batch/`ls crab_projects/${1}/results/ | head -1`_tmp `ls crab_projects/${1}/results/*`
    mv output_batch/`ls crab_projects/${1}/results/ | head -1`_tmp output_batch/`ls crab_projects/${1}/results/ | head -1`
done

