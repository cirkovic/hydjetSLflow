#for s in 0 2; do
for s in 0; do
    #for deta in 1.0 1.5 2.0 2.5 3.0; do
    for deta in 0.0; do
        #root -l -b -q "EFF_VS_NO_EFF_0.C(\"${s}\", \"${deta}\")" &
        #root -l -b -q "EFF_VS_NO_EFF_1.C(\"${s}\", \"${deta}\")" &
        root -l -b -q "EFF_VS_NO_EFF_2.C(\"${s}\", \"${deta}\")" &
        root -l -b -q "EFF_VS_NO_EFF_3.C(\"${s}\", \"${deta}\")" &
        #root -l -b -q "EFF_VS_NO_EFF_4.C(\"${s}\", \"${deta}\")" &
        #root -l -b -q "EFF_VS_NO_EFF_5.C(\"${s}\", \"${deta}\")" &
    done
done
