./import_centr_folders.sh
./run_all.sh
python read_JSON_err_3_deltaEtaCut_proc.py
python dat2json.py
./run_EFF_VS_NO_EFF_all.sh
