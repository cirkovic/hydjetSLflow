sh clear_centr_folders.sh 1
#for i in 00_05 00_10 10_20 20_30 30_40 40_50 50_60; do cp ../test/OUTPUT/out_${i}.root ${i}; done
#for i in 30_40; do cp ../test/OUTPUT_13-04-2016/out_${i}.root ${i}; done
#for j in 0 1 2 3 4; do
for j in 2;
do
    for k in 2.0
    do
        for i in 00_05 05_10 10_15 15_20 20_25 25_30 30_35 35_40 40_50 50_60 60_70 70_80;
        do
            cp `cat INPUT.txt`out_${j}_${i}.root ${j}/${k}/${i}/out_${i}.root;
        done
    done
done

