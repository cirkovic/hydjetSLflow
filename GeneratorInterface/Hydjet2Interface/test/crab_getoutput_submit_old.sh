WORK=`pwd`
#CRABF=crab_20160725_145903
CRABF=${1}
#rm -rf ${CRABF}
mkdir ${CRABF}
N=10000
n=100
for i in `seq 1 $n $N`; do
    begin=$((i))
    end=$((i+n-1))
    NR=$((end-begin+1))
    NEVT=$((NR*4000))

    output=`ls ${CRABF}/*.root | head -1`
    output=`basename $output | sed "s/\(.*\)_/\1_${begin}-${end}.root /"`
    output=`echo $output | awk '{print $1;}'`
    if [ ! -f ${CRABF}/$output ]; then
        #echo bsub -q 8nh crab_getoutput_job.sh $WORK $CRABF -${begin}-${end}
        #sh crab_getoutput_job.sh $WORK $CRABF ${begin}-${end}
        bsub -q 1nd -J ${CRABF} crab_getoutput_job.sh $WORK $CRABF ${begin}-${end}
        #break
    else
        #echo $output
        if [ "`python ${WORK}/getNevt.py ${CRABF}/$output`"="${NEVT}" ]; then
            continue
        else
            #sh crab_getoutput_job.sh $WORK $CRABF ${begin}-${end}
            bsub -q 1nd -J ${CRABF} crab_getoutput_job.sh $WORK $CRABF ${begin}-${end}
        fi
    fi
done

