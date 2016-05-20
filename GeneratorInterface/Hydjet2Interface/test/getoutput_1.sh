source /cvmfs/cms.cern.ch/crab3/crab.sh

array=( crab_20160521_232347 crab_20160521_232259 crab_20160521_232412 crab_20160521_232404 crab_20160521_232338 crab_20160521_232314 crab_20160521_232328 crab_20160521_232322 crab_20160521_223054 crab_20160521_223103 crab_20160521_223020 crab_20160521_223036 crab_20160521_223043 crab_20160521_223029 crab_20160521_223120 crab_20160521_223007 )

while [ true ]; do

    for j in "${array[@]}"
    do
        i="/tmp/cirkovic/${j}/results"
        ids=""
        for k in `seq 1 600`; do
            if ! [ -f ${i}/*_${k}.root ]; then
                if [ "$ids" == "" ]; then
                    ids=$k
                else
                    ids="$ids,$k"
                fi
            fi
        done
        if [[ "$ids" != "" ]]; then
            crab getoutput -d crab_projects/${j} --jobids $ids &
        fi
    done

    if [[ `jobs` != "" ]]; then
        for job in `jobs -p`
        do
            wait $job
        done
    else
        sleep 60
    fi

done










#crab getoutput -d crab_projects/crab_20160521_164227 --checksum=no
##crab getoutput -d crab_projects/crab_20160521_164216 --checksum=no
##crab getoutput -d crab_projects/crab_20160521_164135 --checksum=no
#crab getoutput -d crab_projects/crab_20160521_164237 --checksum=no
##crab getoutput -d crab_projects/crab_20160521_164152 --checksum=no
##crab getoutput -d crab_projects/crab_20160521_164143 --checksum=no
##crab getoutput -d crab_projects/crab_20160521_164200 --checksum=no
##crab getoutput -d crab_projects/crab_20160521_164209 --checksum=no

