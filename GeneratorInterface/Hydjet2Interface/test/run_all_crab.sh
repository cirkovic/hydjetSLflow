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

#Nj=3000
Nj=1000
Nj=6

#for s in 0 2
for s in 0
do
    for c in 0-02 0-5 0-10 10-20 20-30 30-40 40-50 50-60
    #for c in 0-5 50-60
    do
        #for deta in 1.0 1.5 2.0 2.5 3.0
        for deta in 2.0
        do
            #crab submit -c crabConfig_all.py General.Nj=${Nj} General.switch=${s} General.cent=${c} General.deltaEtaCut=${deta}
            #crab submit -c crabConfig_all.py Data.totalUnits=${Nj} JobType.scriptArgs="5000,${s},${c},${deltaEtaCut}"
            crab submit -c crabConfig_all.py Parameters.Nj=${Nj} Parameters.Nepj=80 Parameters.switch=${s} Parameters.cent=${c} Parameters.deltaEtaCut=${deta}
        done
    done
done

