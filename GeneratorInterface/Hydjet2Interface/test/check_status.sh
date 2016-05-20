#array=( crab_20160521_164135 crab_20160521_164143 crab_20160521_164152 crab_20160521_164200 crab_20160521_164209 crab_20160521_164216 crab_20160521_164227 crab_20160521_164237 )
#array=( crab_20160521_223007 crab_20160521_223020 crab_20160521_223029 crab_20160521_223036 crab_20160521_223043 crab_20160521_223054 crab_20160521_223103 crab_20160521_223120 )
array=( crab_20160521_232259 crab_20160521_232314 crab_20160521_232322 crab_20160521_232328 crab_20160521_232338 crab_20160521_232347 crab_20160521_232404 crab_20160521_232412 )

PSs=""
for i in "${array[@]}"
do
    crab status -d crab_projects/${i} --verboseErrors > status_${i}.txt &
    PSs="$PSs $!"
    sleep 2
done

wait $PSs

rm -f status_all.txt;
for i in "${array[@]}"
do
    cat status_${i}.txt >> status_all.txt;
done

cat status_all.txt

