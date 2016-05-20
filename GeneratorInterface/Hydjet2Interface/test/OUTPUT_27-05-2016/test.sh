N=0
M=0
for i in `seq 0 200`;
do
    echo $i
    if [ "$N" -lt "188" ]; then
        M=$(( M + 1 ))
    fi
    N=$(( N + 1 ))
done
echo $N $M
