INPUT=`cat INPUT.txt`
cases=`cat ${INPUT}/cases.txt`
centralities=`cat ${INPUT}/ocentralities.txt`

for j in $cases; do
    for k in 2.0;
    do
        for i in $centralities; do
            rm -rf ${j}/${k}/${i}/${i};
            if [ "$1" == "1" ]; then
                rm -f ${j}/${k}/${i}/out_*.root
            fi
            rm -f ${j}/${k}/prompt_${i}.json
        done
    done
done
rm -f OUTPUT_*.txt
