THISFOLDER1=`pwd`
#rm -rf ${1}
mkdir ${1}
THISFOLDER=${THISFOLDER1}/${1}
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd ${THISFOLDER}


source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

#crab getoutput -d crab_projects/${1} --xrootd > getoutput_${1}.txt

NP=10000
#N=100
N=128
#N=75
#N=50
Q=8nh

#while [[ true ]]; do
#    PROMPT=`crab getoutput -d ${THISFOLDER1}/crab_projects/${1} --xrootd`
#    #echo $PROMPT
#    if [ $? -ne 0 ]; then
#        continue
#    fi
#    #if [ "$PROMPT" != *"The server answered with an error."* ] && [ "$PROMPT" != *"Operation timed out after"* ] ; then
#    if [ "$PROMPT" != *"The server answered with an error."* ] ; then
#        break
#    fi
#done

PROMPT=""
for ip in `seq 1 $NP`; do
    PROMPT="$PROMPT root://cms-xrd-global.cern.ch//store/user/cirkovic/CRAB_PrivateMC/${1}/${2}/0000/output_${3}_${ip}.root"
done

IFS=', ' read -r -a array <<< $PROMPT

#echo "${array[0]}"

hadd_arg=""
i=0

for element in "${array[@]}"
do
    hadd_arg="${hadd_arg} ${element}"
    if [[ "$i" == "$((N-1))" ]]; then

        FINNAM=`echo ${hadd_arg} | awk '{print $1;}'`
        FINNAM=`basename $FINNAM`
        Nevt=0
        if [ -f $FINNAM ]; then
            Nevt=`python ${THISFOLDER1}/getNevt.py ${THISFOLDER}/$FINNAM`;
        fi

        Nroot=`echo ${hadd_arg} | wc -w`
        evt=4000
        evt=$(( evt * Nroot ))
        if [ "$Nevt" -lt "$evt" ]; then
            bsub -q ${Q} -J ${1} ${THISFOLDER1}/crab_getoutput_job_new_1.sh ${THISFOLDER} ${hadd_arg}
        fi

        i=0
        hadd_arg=""
    else
        i=$(( i + 1 ))
    fi
done

if [[ "$i" != "0" ]]; then

        FINNAM=`echo ${hadd_arg} | awk '{print $1;}'`
        FINNAM=`basename $FINNAM`
        Nevt=0
        if [ -f $FINNAM ]; then
            Nevt=`python ${THISFOLDER1}/getNevt.py ${THISFOLDER}/$FINNAM`;
        fi

        Nroot=`echo ${hadd_arg} | wc -w`
        evt=4000
        evt=$(( evt * Nroot ))
        if [ "$Nevt" -lt "$evt" ]; then
            bsub -q ${Q} -J ${1} ${THISFOLDER1}/crab_getoutput_job_new_1.sh ${THISFOLDER} ${hadd_arg}
        fi

        i=0
        hadd_arg=""
fi

