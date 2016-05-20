rm *.root

#INDIRinit=previous
INDIR=out
#INDIR=out_old

#CENTRALITIES="0-02 0-5 0-10 10-20 20-30 30-40 40-50 50-60"
#CENTRALITIES="30-40"
#SWITCHES="0 1 2 3 4"
#CENTRALITIES="0-02"
CENTRALITIES="50-60"
SWITCHES="0 2"
deltaEtaCuts="1.0 1.5 2.0 2.5 3.0"

for s in $SWITCHES;
do
    for c in $CENTRALITIES;
    do
        for deltaEtaCut in $deltaEtaCuts;
        do
            INFILES=""
            #NPFX=output_${s}_500_${c}
            NPFX=output_new_${s}_500_${c}_${deltaEtaCut}
            #INFILES=`ls ${INDIRinit}/output_${s}_500_${c}_all.root`
            INFILES=""
            N=0
            for i in `ls ${INDIR}/${NPFX}_*.root`;
            do
                #if [ "$N" -lt "188" ]; then
                #if [ "$N" -lt "187" ]; then
                if [ true ]; then
                #if [ "$N" -lt "375" ]; then
                    INFILES="$INFILES $i"
                fi
                N=$(( N + 1 ))
            done
            echo $INFILES
            hadd -k -f ${NPFX}_all.root $INFILES &
        done
    done
done

