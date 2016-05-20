cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test

source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

TMP=`mktemp -d`
mkdir -p ${TMP}/${1}/results

crab getoutput -d crab_projects/${1} --outputpath=${TMP}/${1}/results

cd ${TMP}/${1}/results

VAR=`ls output_*.root | head -1`

NN=""
IFS='_' read -ra ADDR <<< "$VAR"
unset ADDR[${#ADDR[@]}-1]
j=0
for i in "${ADDR[@]}"; do
    if [[ $j == "0" ]]; then
        NN="${i}"
    else
        NN="${NN}_${i}"
    fi
    j=$(( j+1 ))
done
NN="${NN}_all.root"

hadd -k -f ${NN} `ls output_*.root`

mkdir /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test/OUTPUT_01-06-2016/output_dir/${1}
mv ${NN} /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test/OUTPUT_01-06-2016/output_dir/${1}/${NN}

