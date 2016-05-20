n=0
PS=""
#for i in `grep -o "http://dashb-cms-job-task.cern.ch/dashboard/request.py/ftsfilestatus?jobId=[0123456789]\+" TaskMonitoring.html`; do
for i in `grep -o "http://dashb-cms-job-task.cern.ch/dashboard/request.py/ftsfilestatus?jobId=[0123456789]\+" TaskMonitoring_50-60.html`; do
    rm -f TMP_${n}.html
    wget $i -O TMP_${n}.html
    NAME=`grep -o "srm.*.root" TMP_${n}.html`
    if [[ "$NAME" == "" ]]; then
        NAME=`grep -o "gsiftp.*.root" TMP_${n}.html`
    fi
    #gfal-copy --force $NAME file:////$PWD/ &
    nam=`basename $NAME`
    if [[ `eos ls /eos/cms/store/caf/user/mdjordje/Cirkovic/hydjet/14-03-2017/50-60/$nam` == "" ]]; then
        gfal-copy --force $NAME root://eoscms.cern.ch//eos/cms/store/caf/user/mdjordje/Cirkovic/hydjet/14-03-2017/50-60/$nam &
    fi
    PS="$PS $!"
    if [[ "$n" == "10" ]]; then
        wait $PS
        n=0
        PS=""
    else
        n=$((n + 1))
    fi
done
