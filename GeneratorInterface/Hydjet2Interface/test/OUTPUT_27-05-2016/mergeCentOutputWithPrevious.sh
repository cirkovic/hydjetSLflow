rm *.root

INDIRinit=previous
INDIR=out

CENTRALITIES="0-5 0-10 10-20 20-30 30-40 40-50 50-60"
#CENTRALITIES="30-40"
#SWITCHES="0 1 2 3 4"
SWITCHES="2"

for s in $SWITCHES;
do
    for c in $CENTRALITIES;
    do
        INFILES=""
        NPFX=output_${s}_250_${c}
        INFILES=`ls ${INDIRinit}/${NPFX}_all.root`
        #NPFX=output_${s}_500_${c}
        #N=0
        for i in `ls ${INDIR}/${NPFX}_*.root`;
        do
            #if [ "$N" -lt "188" ]; then
            INFILES="$INFILES $i"
            #fi
            #N=$(( N + 1 ))
        done
        echo $INFILES
        hadd -k -f ${NPFX}_all.root $INFILES &
    done
done
