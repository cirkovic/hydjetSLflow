#!/bin/bash

Nevt=$2
s=$3
c=$4
deltaEtaCut=$5

#echo $Nevt $s $c $deltaEtaCut

IFS='=' read -ra ARG <<< "$Nevt"
Nevt="${ARG[1]}"

IFS='=' read -ra ARG <<< "$s"
s="${ARG[1]}"

IFS='=' read -ra ARG <<< "$c"
c="${ARG[1]}"

IFS='=' read -ra ARG <<< "$deltaEtaCut"
deltaEtaCut="${ARG[1]}"

#echo $Nevt $s $c $deltaEtaCut

PSs=""
OUTPUTFILES=""

Njpw=`nproc`
Njpw=1
#echo $Nevt $Njpw
for j in `seq 0 $((Njpw - 1))`;
do
    if [ "$j" -lt "$((Njpw - 1))" ]; then
        Nev=$((Nevt/Njpw))
    else
        Nev=$((Nevt-j*Nev))
    fi
    #echo $j $Nev
    sh subjob_new_my_502_1.sh $Nev $s $c $deltaEtaCut $j &
    OUTPUTFILES="$OUTPUTFILES output_${Nev}_${s}_${c}_${deltaEtaCut}_${j}.root"
    PSs="$PSs $!"
done

#exit

wait $PSs

OUTPUTFILE=output_${Nevt}_${s}_${c}_${deltaEtaCut}.root

hadd -f $OUTPUTFILE $OUTPUTFILES

cp `ls -t FrameworkJobReport_*.xml | head -1` FrameworkJobReport.xml
#cp `ls -S FrameworkJobReport_*.xml | head -1` FrameworkJobReport.xml

#cmsRun -j FrameworkJobReport.xml -p PSet.py
#cmsRun -j FrameworkJobReport.xml -p pset.py
