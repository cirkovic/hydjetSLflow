WORK=${1}
CRABF=${2}
RANGE=${3}
IFS='-' read -ra ADDR <<< "$RANGE"
begin="${ADDR[0]}"
end="${ADDR[1]}"
NR=$((end-begin+1))
NEVT=$((NR*4000))

echo $NR $NEVT

#exit

#echo $WORK $CRABF $RANGE

THISFOLDER=${WORK}/${CRABF}
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd ${THISFOLDER}

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

MKTEMP=`mktemp -d`
cp -r ${WORK}/crab_projects/${CRABF} ${MKTEMP}
cp ${WORK}/getNevt ${MKTEMP}

#for i in `seq 1 3`;
if [ ! -f ${THISFOLDER}/$output ]; then
    Nrfs=0
else
    #Nrfs=`${WORK}/getNevt ${THISFOLDER}/$output`
    Nrfs=`${MKTEMP}/getNevt ${THISFOLDER}/$output`
fi

while [ true ];
do
    #for i in `seq 1 3`; do
    rm -f crab.log
    rm -f ${MKTEMP}/${CRABF}/crab.log
    echo crab getoutput -d ${MKTEMP}/${CRABF} --jobids=${RANGE} #--outputpath=${MKTEMP} #--checksum=no
    crab getoutput -d ${MKTEMP}/${CRABF} --jobids=${RANGE} #--outputpath=${MKTEMP} #--checksum=no
    #done

    Nrfs1=`ls ${MKTEMP}/${CRABF}/results/*.root | wc -l`

    if [ "$Nrfs1" -gt "$Nrfs" ]; then
        output=`ls ${MKTEMP}/${CRABF}/results/*.root | head -1`
        output=`basename $output | sed "s/\(.*\)_/\1_${RANGE}.root /"`
        output=`echo $output | awk '{print $1;}'`
        hadd -f -k ${MKTEMP}/$output ${MKTEMP}/${CRABF}/results/*.root
        mv ${MKTEMP}/$output ${THISFOLDER}
        #nevt=`${WORK}/getNevt ${THISFOLDER}/$output`
        nevt=`${MKTEMP}/getNevt ${THISFOLDER}/$output`
        if [ "${nevt}" == "${NEVT}" ]; then
        #if [ true ]; then
            exit
        fi
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
