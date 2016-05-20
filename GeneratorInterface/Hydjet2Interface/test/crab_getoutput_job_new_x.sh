echo $@

THISFOLDER=${1}
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd ${THISFOLDER}

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

MKTEMP=`mktemp -d`
N=`nproc`

begin=2
PSs=""
while [[ ! $end -gt "$#" ]]; do
    end=$((begin+N))
    fout=${MKTEMP}/`basename ${@:begin:1}`
    echo hadd -f $fout ${@:$begin:$N}
    (hadd -f $fout ${@:$begin:$N} ; echo $? > ${MKTEMP}/somefile) & PSs="$PSs $!"
    begin=$((end))
done

wait $PSs

if [ "`awk '{ sum += $1 } END { print sum }' ${MKTEMP}/somefile`" == "0" ]; then
    finname=${MKTEMP}/`basename ${2/.root/_all.root}`
    hadd -f $finname ${MKTEMP}/*.root
    mv $finname ${THISFOLDER}
fi

#while [[ true ]]; do
#
#    hadd -f ${MKTEMP}/`basename ${2}` ${@:2}
#
#    EXITCODE=$?
#    echo EXITCODE: ${EXITCODE}
#    if [ ${EXITCODE} -eq 0 ]; then
#        break
#    fi
#
#done

#mv ${MKTEMP}/`basename ${2}` ${THISFOLDER}

