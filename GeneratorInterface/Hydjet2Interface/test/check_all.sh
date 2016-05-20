while [ true ];
do
    sheadall=""
    strall=""
    for i in cirkovic@lxplus101 cirkovic@lxplus0027 cirkovic@lxplus008 cirkovic@lxplus0088 cirkovic@lxplus0075; do
        shead=""
        str=""
        for j in `ssh $i ls -d /tmp/cirkovic/crab_*`; do
            shead="$shead `ssh $i ls ${j}/results/*.root | head -1`"
            str="$str `ssh $i ls ${j}/results/*.root | wc -l`"
        done
        sheadall="$sheadall $shead"
        strall="$strall $str"
    done
    #echo $sheadall
    echo $strall
    #echo
done

