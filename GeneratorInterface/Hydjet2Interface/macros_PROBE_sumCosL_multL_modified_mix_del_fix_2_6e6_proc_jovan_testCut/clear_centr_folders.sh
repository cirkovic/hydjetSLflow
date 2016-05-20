for j in 0 1 2 3 4; do
    for k in 1.0 1.5 2.0 2.5 3.0; do
        for i in 00_02 00_05 00_10 10_20 20_30 30_40 40_50 50_60; do
            rm -rf ${j}/${k}/${i}/${i};
            if [ "$1" == "1" ]; then
                rm -f ${j}/${k}/${i}/out_*.root
            fi
        done
    done
done
rm OUTPUT_*.txt
