#!/bin/bash

Nev=$1
s=$2
c=$3 #default 0-5
deltaEtaCut=$4
j=$5

cmsRun -j FrameworkJobReport_${j}.xml testHydjet_new_crab_my_pt_mult_502.py $Nev $s $c $deltaEtaCut $j #&& mv ${WORKDIR}/output_*.root $CURRDIR
