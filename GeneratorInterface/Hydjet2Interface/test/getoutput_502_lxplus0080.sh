source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 192:00

#array=( crab_20160601_132214 crab_20160601_132233 crab_20160601_133024 crab_20160601_132355 crab_20160601_132405 crab_20160601_132450 crab_20160601_132503 crab_20160601_132512 crab_20160601_132521 crab_20160601_132544 crab_20160601_132608 crab_20160601_132618 )
#array=( crab_20160602_111021 crab_20160601_132214 crab_20160601_132233 crab_20160601_133024 crab_20160601_132355 crab_20160601_132405 crab_20160601_132450 crab_20160601_132503 crab_20160601_132512 crab_20160601_132521 crab_20160601_132544 crab_20160601_132608 crab_20160601_132618 )
#array=( crab_20160601_132214 crab_20160601_132233 crab_20160601_133024 crab_20160601_132355 crab_20160601_132405 crab_20160601_132450 crab_20160601_132503 crab_20160601_132512 crab_20160601_132521 crab_20160601_132544 crab_20160601_132608 crab_20160601_132618 crab_20160602_111021 crab_20160602_122340 crab_20160602_122424 crab_20160602_122440 crab_20160602_122501 crab_20160602_122518 crab_20160602_122531 crab_20160602_122544 crab_20160602_122557 crab_20160602_122610 crab_20160602_122621 crab_20160602_122633 )
array=( crab_20160606_223519 crab_20160606_223449 crab_20160606_223551 )

while [ true ];
do
    #PSs=""
    for i in "${array[@]}"
    do
        if [ "$1" == "1" ]; then
            rm -rf crab_projects/${i}/results /tmp/cirkovic/${i}/results
            mkdir -p /tmp/cirkovic/${i}/results
            ln -s /tmp/cirkovic/${i}/results crab_projects/${i}/results
        else
            crab getoutput -d crab_projects/${i}
            #PSs="$PSs $!"
        fi
    done
    if [ "$1" == "1" ]; then
        break;
    fi
    wait $PSs
done

