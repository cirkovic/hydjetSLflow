sh clear_centr_folders_np.sh 1
#for i in 00_05 00_10 10_20 20_30 30_40 40_50 50_60; do cp ../test/OUTPUT/out_${i}.root ${i}; done
#for i in 30_40; do cp ../test/OUTPUT_13-04-2016/out_${i}.root ${i}; done
#for j in 0 1 2 3 4; do

INPUT=`cat INPUT.txt`
cases=`cat ${INPUT}/cases.txt`
centralities=`cat ${INPUT}/ocentralities.txt`

for j in $cases;
do
    for k in 2.0
    do
        for i in $centralities;
        do
            mkdir -p ${j}_np/${k}/${i}
            cp `cat INPUT.txt`out_${j}_${i}.root ${j}_np/${k}/${i}/out_${i}.root;
        done
    done
done

