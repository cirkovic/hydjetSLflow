for cent in 0-02 0-5 0-10 10-20 20-30 30-40 40-50 50-60; do
    #cp crabConfig_276_${c}.py crabConfig_502_${c}.py
    for ene in 276 502; do
    #for e in 502; do
        #vim crabConfig_${e}_${c}.py
        #diff crabConfig_276_${c}.py crabConfig_502_${c}.py
        #crab submit -c crabConfig_${e}_${c}.py
        #sh job_new_my_pt_mult_ene.sh test Nevt=16 s=2 c=${cent} deltaEtaCut=2.0 energy=${ene}
        crab submit -c crabConfig_${ene}_${cent}.py
    done
done

