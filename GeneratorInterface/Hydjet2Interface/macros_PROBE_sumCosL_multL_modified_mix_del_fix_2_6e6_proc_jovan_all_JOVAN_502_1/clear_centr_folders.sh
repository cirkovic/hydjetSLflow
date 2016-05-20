for j in 0 1 2 3 4; do
    for k in 2.0;
    do
        for i in 00_05 05_10 10_15 15_20 20_25 25_30 30_35 35_40 40_50 50_60 60_70 70_80; do
            rm -rf ${j}/${k}/${i}/${i};
            if [ "$1" == "1" ]; then
                rm -f ${j}/${k}/${i}/out_*.root
            fi
        done
    done
done
rm OUTPUT_*.txt
