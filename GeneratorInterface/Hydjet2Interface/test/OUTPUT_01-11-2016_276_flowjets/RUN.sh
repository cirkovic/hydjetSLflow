find `cat OPATH.txt` -name "*.png" | xargs rm -f
find `cat OPATH.txt` -name "*.pdf" | xargs rm -f

for c in `cat cases.txt`; do
    cp -f centralities.txt `cat OPATH.txt`/2/${c}
    rm -rf `cat OPATH.txt`1/${c}/*
    for cent in `cat centralities.txt`; do
        cp -rf `cat OPATH.txt`/1/x-x `cat OPATH.txt`/1/${c}/${cent}
    done
done

PSs=""

( python drawAndEditTemplatesL_proc.py ) &
PSs="$PSs $!"

( python plot_delta_eta_phi_proc.py ) &
PSs="$PSs $!"

wait $PSs

python print_pt.py ../../macros_PROBE_sumCosL_multL_modified_mix_del_fix_2_6e6_proc_jovan_all_JOVAN_data_fit_60M_01-11-2016_276_flowjets/pt_values.h

