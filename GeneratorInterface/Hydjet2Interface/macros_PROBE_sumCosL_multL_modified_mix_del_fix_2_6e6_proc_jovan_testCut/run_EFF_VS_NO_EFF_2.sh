for s in 0 2; do
    for deta in 1.0 1.5 2.0 2.5 3.0; do
        root -l -b -q "EFF_VS_NO_EFF_2.C(\"${s}\", \"${deta}\")" &
    done
done
