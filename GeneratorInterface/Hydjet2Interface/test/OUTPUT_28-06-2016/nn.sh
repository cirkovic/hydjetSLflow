VAR=`ls /tmp/cirkovic/crab_20160602_122610/results/ | head -1`
#echo ${VAR}
#echo ${VAR/_*.root/_all.root}

NN=""
IFS='_' read -ra ADDR <<< "$VAR"
unset ADDR[${#ADDR[@]}-1]
j=0
for i in "${ADDR[@]}"; do
    if [[ $j == "0" ]]; then
        NN="${i}"
    else
        NN="${NN}_${i}"
    fi
    j=$(( j+1 ))
done
NN="${NN}_all.root"

echo $NN

