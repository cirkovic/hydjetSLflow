source /cvmfs/cms.cern.ch/crab3/crab.sh

#voms-proxy-init -voms cms
voms-proxy-init --voms cms --valid 192:00

#cd /afs/cern.ch/work/c/cirkovic/HYDJET/CMSSW_7_6_0_pre1/src/
#cd /afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src
#eval `scramv1 runtime -sh`
#cd /afs/cern.ch/work/c/cirkovic/HYDJET/CMSSW_7_6_0_pre1/src/GeneratorInterface/Hydjet2Interface/test

#cmsRun testHydjet_new_crab.py 2 2 0 50-60 2.0
#cmsRun testHydjet_new_crab.py 2 2 0 50-60 2.0
#crab submit -c testHydjet_new_crab.py 2 2 0 50-60 2.0
#crab submit -c crabConfig_tutorial_MC_generation.py
#for i in `seq 1 8`;
for i in `seq 1 8`;
do
    crab submit -c crabConfig_${i}.py
done
