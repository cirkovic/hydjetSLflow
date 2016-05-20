#CRABF=crab_20160725_145934;
#CRABL=160725_130004;
#LAB=4000_2_40-50_2.0_502;

CRABF=crab_20160725_145903;
CRABL=160725_125931;
LAB=4000_2_40-50_2.0_276;

while [ true ]; do
    while [ "`bjobs -J ${CRABF} | wc -l`" -gt "0" ]; do
        sleep 60;
    done;
    sh crab_getoutput_new_1.sh ${CRABF} ${CRABL} ${LAB};
done

