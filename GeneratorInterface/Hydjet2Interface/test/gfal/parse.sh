n=0
PS=""
for i in `grep -o "http://dashb-cms-job-task.cern.ch/dashboard/request.py/ftsfilestatus?jobId=[0123456789]\+" TaskMonitoring.html`; do
    rm -f tmp_${n}.html
    wget $i -O tmp_${n}.html
    NAME=`grep -o "srm.*.root" tmp_${n}.html`
    gfal-copy --force $NAME file:////$PWD/ &
    PS="$PS $!"
    if [[ "$n" == "10" ]]; then
        wait $PS
        exit
        n=0
        PS=""
    else
        n=$((n + 1))
    fi
done
