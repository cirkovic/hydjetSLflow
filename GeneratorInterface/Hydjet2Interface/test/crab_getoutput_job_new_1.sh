echo $@

THISFOLDER=${1}
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd ${THISFOLDER}

FINNAM=`basename ${2/.root/_all.root}`
#Nevt=`python ../getNevt.py $FINNAM`;

#Narg=$#
#Nroot=$(( Narg - 1 ))
#evt=4000
#evt=$(( evt * Nroot ))
#if [ "$Nevt" == "$evt" ]; then
#    exit
#fi

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

MKTEMP=`mktemp -d`
N=`nproc`

begin=2
PSs=""
while [[ ! $end -gt "$#" ]]; do
    end=$((begin+N))
    fout=${MKTEMP}/`basename ${@:begin:1}`
    echo hadd -f -k $fout ${@:$begin:$N}
    (hadd -f -k $fout ${@:$begin:$N} ; echo $? > ${MKTEMP}/somefile) & PSs="$PSs $!"
    begin=$((end))
done

wait $PSs

if [ "`awk '{ sum += $1 } END { print sum }' ${MKTEMP}/somefile`" == "0" ]; then
    finname=${MKTEMP}/${FINNAM}
    hadd -f -k $finname ${MKTEMP}/*.root
    mv $finname ${THISFOLDER}
fi

