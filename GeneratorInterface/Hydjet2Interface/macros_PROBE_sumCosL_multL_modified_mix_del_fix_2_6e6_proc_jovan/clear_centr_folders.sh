for j in 0 1 2 3 4; do
    for i in 00_02 00_05 00_10 10_20 20_30 30_40 40_50 50_60; do
        rm -rf ${j}/${i}/${i};
        if [ "$1" == "1" ]; then
            rm -f ${j}/${i}/out_*.root
        fi
    done
done
rm OUTPUT_*.txt
