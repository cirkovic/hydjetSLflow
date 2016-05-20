CENTRALITIES=`cat centralities.txt`
OCENTRALITIES=`cat ocentralities.txt`

cents=($CENTRALITIES)
ocents=($OCENTRALITIES)

declare -A dict
I=0
for cent in $CENTRALITIES; do
    dict+=( [${cent}]=${ocents[I]} )
    I=$(( I + 1 ))
done

for cent in "${!dict[@]}"; do
    echo "$cent - ${dict[$cent]}"
done

