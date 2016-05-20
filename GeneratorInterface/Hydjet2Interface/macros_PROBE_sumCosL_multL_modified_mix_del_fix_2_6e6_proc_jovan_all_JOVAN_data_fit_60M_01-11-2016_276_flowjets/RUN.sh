cp -f `cat INPUT.txt`cases.txt cases.txt
cp -f `cat INPUT.txt`centralities.txt centralities.txt
cp -f `cat INPUT.txt`ocentralities.txt ocentralities.txt

./import_centr_folders.sh
./import_centr_folders_np.sh

for c in `cat ocentralities.txt`; do
    cp Parameters_xx_xx.json Parameters_${c}.json
    sed -i s/xx_xx/${c}/g Parameters_${c}.json
done

./run_all.sh
./run_all_np.sh
python read_JSON_err_3_deltaEtaCut_proc.py
python dat2json.py
python dat2json_np.py
sh importFitInfo.sh
./run_EFF_VS_NO_EFF_all.sh
./run_EFF_VS_NO_EFF_all_new.sh
#./run_EFF_VS_NO_EFF_all_new.sh
./Print_to_file_last_modes_errors_np.sh
python draw_integral_plot.py
