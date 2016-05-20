INPUT=`cat INPUT.txt`
cases=`cat ${INPUT}/cases.txt`
centralities=`cat ${INPUT}/ocentralities.txt`

for j in $cases; do
    for k in 2.0;
    do
        #for i in 00_02 00_05 00_10 10_20 20_30 30_40 40_50 50_60; do
        for i in $centralities; do
            rm -rf ${j}_np/${k}/${i}/${i};
            if [ "$1" == "1" ]; then
                rm -f ${j}_np/${k}/${i}/out_*.root
            fi
            rm -f ${j}_np/${k}/prompt_${i}.json
        done
    done
done
rm -f OUTPUT_*.txt
