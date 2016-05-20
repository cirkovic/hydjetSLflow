./import_centr_folders.sh
./import_centr_folders_np.sh
./run_all.sh
./run_all_np.sh
python read_JSON_err_3_deltaEtaCut_proc.py
python dat2json.py
python dat2json_np.py
sh importFitInfo.sh
./run_EFF_VS_NO_EFF_all.sh
#./run_EFF_VS_NO_EFF_all_new.sh
./Print_to_file_last_modes_errors_np.sh
python draw_integral_plot.py
