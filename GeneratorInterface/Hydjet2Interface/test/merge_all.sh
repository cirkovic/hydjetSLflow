for i in `ls -d crab_20160*`; do
    LS=`ls ${i}/output_4000_*.root`;
    LS1=`ls ${i}/output_4000_*.root | head -1`;
    #echo hadd -k -f ${i}/all_`basename ${LS1}` ${LS1}
    hadd -k -f ${i}/all_`basename ${LS1}` ${LS} &
done
