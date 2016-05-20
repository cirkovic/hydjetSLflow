find `cat OPATH.txt` -name "*.png" | xargs rm

PSs=""

( python drawAndEditTemplatesL_proc.py ) &
PSs="$PSs $!"

( python plot_delta_eta_phi_proc.py ) &
PSs="$PSs $!"

wait $PSs

exit

#python print_pt.py ../../macros_PROBE_sumCosL_multL_modified_mix_del_fix_2_6e6_proc_jovan_all_JOVAN_data_fit_60M_17-10-2016_276_flowjets/pt_values.h
python print_pt.py ../../macros_PROBE_sumCosL_multL_modified_mix_del_fix_2_6e6_proc_jovan_all_JOVAN_data_fit_60M_11-03-2017_276_flowjets/pt_values_2.h

