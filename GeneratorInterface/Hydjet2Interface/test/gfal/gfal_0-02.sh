n=0
PS=""
#for i in `grep -o "http://dashb-cms-job-task.cern.ch/dashboard/request.py/ftsfilestatus?jobId=[0123456789]\+" TaskMonitoring.html`; do
for i in `grep -o "http://dashb-cms-job-task.cern.ch/dashboard/request.py/ftsfilestatus?jobId=[0123456789]\+" TaskMonitoring_0-02.html`; do
    rm -f tmp_${n}.html
    wget $i -O tmp_${n}.html
    NAME=`grep -o "srm.*.root" tmp_${n}.html`
    if [[ "$NAME" == "" ]]; then
        NAME=`grep -o "gsiftp.*.root" TMP_${n}.html`
    fi
    #gfal-copy --force $NAME file:////$PWD/ &
    nam=`basename $NAME`
    if [[ `eos ls /eos/cms/store/caf/user/mdjordje/Cirkovic/hydjet/14-03-2017/0-02/$nam` == "" ]]; then
        gfal-copy --force $NAME root://eoscms.cern.ch//eos/cms/store/caf/user/mdjordje/Cirkovic/hydjet/14-03-2017/0-02/$nam &
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
