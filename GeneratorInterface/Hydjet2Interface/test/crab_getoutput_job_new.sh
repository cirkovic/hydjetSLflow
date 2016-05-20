THISFOLDER=${1}
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd ${THISFOLDER}

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

MKTEMP=`mktemp -d`

echo hadd -k -f ${MKTEMP}/`basename ${2}` ${@:2}

while [[ true ]]; do

    hadd -f ${MKTEMP}/`basename ${2}` ${@:2}

    EXITCODE=$?
    echo EXITCODE: ${EXITCODE}
    if [ ${EXITCODE} -eq 0 ]; then
        break
    fi

done

mv ${MKTEMP}/`basename ${2}` ${THISFOLDER}

