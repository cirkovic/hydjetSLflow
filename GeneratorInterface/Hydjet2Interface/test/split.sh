N=8
#begin=2
#end=$((begin+N))
#echo hadd -k -f ${MKTEMP}/`basename $begin` ${@:$begin:$N}
#begin=$((end))
#end=$((begin+N))
#echo hadd -k -f ${MKTEMP}/`basename $begin` ${@:$begin:$N}
begin=2
while [[ ! $end -gt "$#" ]]; do
end=$((begin+N))
echo hadd -k -f ${MKTEMP}/`basename $begin` ${@:$begin:$N}
begin=$((end))
done
#echo hadd -k -f ${MKTEMP}/`basename $((2+N+1))` ${@:2+$N+1}
