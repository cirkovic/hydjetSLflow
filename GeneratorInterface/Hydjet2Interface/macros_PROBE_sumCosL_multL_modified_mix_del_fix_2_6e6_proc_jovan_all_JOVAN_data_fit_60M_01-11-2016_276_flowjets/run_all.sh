INPUT=`cat INPUT.txt`
cases=`cat ${INPUT}/cases.txt`
centralities=`cat ${INPUT}/ocentralities.txt`

#switches="0 1 2 3 4"
switches=$cases
deta="2.0"
#centralities=$centralities
#centralities="10_20"
#centralities="30_40"

PSs=""
for j in $switches;
do
    for k in ${deta};
    do
        cd ${j}/${k}
        for i in $centralities;
        do
            python ../../FULL_RUN.py $i 2>&1 | tee ../../OUTPUT_${j}_${i}_${k}.txt &
            PSs="$PSs $!"
        done
    cd ../..
    done
done

wait $PSs

for j in $switches;
do
    for k in $deta;
    do
        for i in $centralities;
        do
            sed -i -e 's/\[?1034h/\n/g' OUTPUT_${j}_${i}_${k}.txt
        done
    done
done
