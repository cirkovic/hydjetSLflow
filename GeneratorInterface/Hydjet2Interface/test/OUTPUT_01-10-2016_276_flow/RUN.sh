find `cat OPATH.txt` -name "*.png" | xargs rm

PSs=""

( python drawAndEditTemplatesL_proc.py ) &
PSs="$PSs $!"

( python plot_delta_eta_phi_proc.py ) &
PSs="$PSs $!"

wait $PSs

python print_pt.py ../../macros_PROBE_sumCosL_multL_modified_mix_del_fix_2_6e6_proc_jovan_all_JOVAN_data_fit_40M_01-10-2016_276_flow/pt_values.h

