#echo $@

WORK=${1}
CRABF=${2}
RANGE=${3}

#echo $WORK $CRABF $RANGE

THISFOLDER=${WORK}/${CRABF}
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd ${THISFOLDER}

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

MKTEMP=`mktemp -d`

#for i in `seq 1 3`;
Nrfs=0
while [ true ];
do
    for i in `seq 1 3`; do
        rm -f ${WORK}/crab_projects/${CRABF}/crab.log
        echo crab getoutput -d ${WORK}/crab_projects/${CRABF} --jobids=${RANGE} --outputpath=${MKTEMP} #--checksum=no
        crab getoutput -d ${WORK}/crab_projects/${CRABF} --jobids=${RANGE} --outputpath=${MKTEMP} #--checksum=no
    done

    Nrfs1=`ls ${MKTEMP}/*.root | wc -l`

    if [ "$Nrfs1" -gt "$Nrfs" ]; then
        output=`ls ${MKTEMP}/*.root | head -1`
        output=`basename $output | sed "s/\(.*\)_/\1_${RANGE}.root /"`
        output=`echo $output | awk '{print $1;}'`
        hadd -f -k ${MKTEMP}/$output ${MKTEMP}/*.root
        mv ${MKTEMP}/$output ${THISFOLDER}
    fi

    Nrfs=$Nrfs1

done

#if [ "`ls ${MKTEMP}/*.root | wc -l`" -gt "0" ]; then
#    output=`ls ${MKTEMP}/*.root | head -1`
#    output=`basename $output | sed "s/\(.*\)_/\1_${RANGE}.root /"`
#    output=`echo $output | awk '{print $1;}'`
#    hadd -f -k ${MKTEMP}/$output ${MKTEMP}/*.root
#    mv ${MKTEMP}/$output ${THISFOLDER}
#fi
