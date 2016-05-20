#cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
#eval `scramv1 runtime -sh`
#cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test


#source /cvmfs/cms.cern.ch/crab3/crab.sh
#voms-proxy-init --voms cms --valid 192:00

#crab getoutput -d crab_projects/${1} --xrootd > getoutput_${1}.txt

N=99

#IFS=', ' read -r -a array <<< `crab getoutput -d crab_projects/${1} --xrootd`
IFS=', ' read -r -a array <<< `cat filelist.txt`

#echo "${array[0]}"

hadd_arg=""
i=0

for element in "${array[@]}"
do
    hadd_arg="${hadd_arg} ${element}"
    if [[ "$i" == "$N" ]]; then
        #echo ${hadd_arg}
        #echo
        sh crab_getoutput_job.sh ${hadd_arg}
        i=0
        hadd_arg=""
    else
        i=$(( i + 1 ))
    fi
done

if [[ "$i" != "0" ]]; then
        #echo ${hadd_arg}
        #echo
        sh crab_getoutput_job.sh ${hadd_arg}
        i=0
        hadd_arg=""
fi

