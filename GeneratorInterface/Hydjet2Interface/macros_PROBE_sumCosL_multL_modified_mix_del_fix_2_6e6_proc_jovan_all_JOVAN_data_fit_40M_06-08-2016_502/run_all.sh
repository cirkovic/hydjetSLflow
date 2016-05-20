#switches="0 1 2 3 4"
switches="2"
deta="2.0"
centralities="00_02 00_05 00_10 10_20 20_30 30_40 40_50 50_60"
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
