find `cat OPATH.txt` -name "*.png" | xargs rm

PSs=""

( python drawAndEditTemplatesL_proc.py ) &
PSs="$PSs $!"

( python plot_delta_eta_phi_proc.py ) &
PSs="$PSs $!"

wait $PSs

