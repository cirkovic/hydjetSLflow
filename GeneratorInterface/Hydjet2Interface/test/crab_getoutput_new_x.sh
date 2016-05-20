THISFOLDER1=`pwd`
rm -rf ${1}
mkdir ${1}
THISFOLDER=${THISFOLDER1}/${1}
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
eval `scramv1 runtime -sh`
cd ${THISFOLDER}


source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

#crab getoutput -d crab_projects/${1} --xrootd > getoutput_${1}.txt

#N=100
N=128
#N=75
#N=50
Q=8nh

while [[ true ]]; do
    PROMPT=`crab getoutput -d ${THISFOLDER1}/crab_projects/${1} --xrootd`
    #echo $PROMPT
    if [ $? -ne 0 ]; then
        continue
    fi
    #if [ "$PROMPT" != *"The server answered with an error."* ] && [ "$PROMPT" != *"Operation timed out after"* ] ; then
    if [ "$PROMPT" != *"The server answered with an error."* ] ; then
        break
    fi
done

IFS=', ' read -r -a array <<< $PROMPT

#echo "${array[0]}"

hadd_arg=""
i=0

for element in "${array[@]}"
do
    hadd_arg="${hadd_arg} ${element}"
    if [[ "$i" == "$((N-1))" ]]; then
        bsub -q ${Q} ${THISFOLDER1}/crab_getoutput_job_new_1.sh ${THISFOLDER} ${hadd_arg}
        i=0
        hadd_arg=""
    else
        i=$(( i + 1 ))
    fi
done

if [[ "$i" != "0" ]]; then
        bsub -q ${Q} ${THISFOLDER1}/crab_getoutput_job_new_1.sh ${THISFOLDER} ${hadd_arg}
        i=0
        hadd_arg=""
fi

