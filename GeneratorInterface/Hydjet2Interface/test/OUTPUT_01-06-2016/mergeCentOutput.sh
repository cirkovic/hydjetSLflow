rm -f *.root

#Nevt=5000
#Nevt=4500
s=2
#c=( 0-02 0-5 0-10 10-20 20-30 30-40 40-50 50-60 )
c=( 0-5 5-10 10-15 15-20 20-25 25-30 30-35 35-40 40-50 50-60 60-70 70-80 )
deltaEtaCut=2.0
#first=( crab_20160601_132214 crab_20160601_132233 crab_20160601_133024 crab_20160601_132355 crab_20160601_132405 crab_20160601_132450 crab_20160601_132503 crab_20160601_132512 crab_20160601_132521 crab_20160601_132544 crab_20160601_132608 crab_20160601_132618 )
#first=( crab_20160602_111021 crab_20160601_132214 crab_20160601_132233 crab_20160601_133024 crab_20160601_132355 crab_20160601_132405 crab_20160601_132450 crab_20160601_132503 crab_20160601_132512 crab_20160601_132521 crab_20160601_132544 crab_20160601_132608 crab_20160601_132618 )
first=( crab_20160601_132214 crab_20160601_132233 crab_20160601_133024 crab_20160601_132355 crab_20160601_132405 crab_20160601_132450 crab_20160601_132503 crab_20160601_132512 crab_20160601_132521 crab_20160601_132544 crab_20160601_132608 crab_20160601_132618 )
#second=( crab_20160602_111021 crab_empty crab_empty crab_empty crab_empty crab_empty crab_empty crab_empty crab_empty crab_empty crab_empty crab_empty )
second=( crab_20160602_111021 crab_20160602_122340 crab_20160602_122424 crab_20160602_122440 crab_20160602_122501 crab_20160602_122518 crab_20160602_122531 crab_20160602_122544 crab_20160602_122557 crab_20160602_122610 crab_20160602_122621 crab_20160602_122633 )

PSs=""
#for i in `seq 0 7`;
for i in `seq 0 11`;
do
    #hadd -k -f output_20M/output_all_${s}_${c[$i]}_${deltaEtaCut}.root `ls /tmp/cirkovic/${first[$i]}/results/output_${Nevt}_${s}_${c[$i]}_${deltaEtaCut}_*.root` &
    #hadd -k -f output_20M/output_all_${s}_${c[$i]}_${deltaEtaCut}.root `ls /tmp/cirkovic/${first[$i]}/results/output_*_${s}_${c[$i]}_${deltaEtaCut}_*.root` &
    hadd -k -f output_20M/output_all_${s}_${c[$i]}_${deltaEtaCut}.root `ls ../crab_projects/${first[$i]}/results/output_*_${s}_${c[$i]}_${deltaEtaCut}_*.root` `ls ../crab_projects/${second[$i]}/results/output_*_${s}_${c[$i]}_${deltaEtaCut}_*.root` &
    PSs="$PSs $!"
done



(
    while [ true ]; do
        none=true
        for p in $PSs; do
            if [ -e /proc/$p ]; then
                none=false
            fi
        done
        if $none ; then
            break
        fi
        sleep 1
    done
    for i in `seq 0 11`; do
        touch output_20M/output_all_${s}_${c[$i]}_${deltaEtaCut}.root
    done
    echo DONE
) &
