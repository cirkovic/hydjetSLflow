INPUT=`cat INPUT.txt`

cp ${INPUT}/fout_2_0-02_2.json FIT/2/2.0/n2/00_02.json
cp ${INPUT}/fout_2_0-5_2.json FIT/2/2.0/n2/00_05.json
cp ${INPUT}/fout_2_0-10_2.json FIT/2/2.0/n2/00_10.json
cp ${INPUT}/fout_2_10-20_2.json FIT/2/2.0/n2/10_20.json
cp ${INPUT}/fout_2_20-30_2.json FIT/2/2.0/n2/20_30.json
cp ${INPUT}/fout_2_30-40_2.json FIT/2/2.0/n2/30_40.json
cp ${INPUT}/fout_2_40-50_2.json FIT/2/2.0/n2/40_50.json
cp ${INPUT}/fout_2_50-60_2.json FIT/2/2.0/n2/50_60.json

cp ${INPUT}/fout_2_0-02_3.json FIT/2/2.0/n3/00_02.json
cp ${INPUT}/fout_2_0-5_3.json FIT/2/2.0/n3/00_05.json
cp ${INPUT}/fout_2_0-10_3.json FIT/2/2.0/n3/00_10.json
cp ${INPUT}/fout_2_10-20_3.json FIT/2/2.0/n3/10_20.json
cp ${INPUT}/fout_2_20-30_3.json FIT/2/2.0/n3/20_30.json
cp ${INPUT}/fout_2_30-40_3.json FIT/2/2.0/n3/30_40.json
cp ${INPUT}/fout_2_40-50_3.json FIT/2/2.0/n3/40_50.json
cp ${INPUT}/fout_2_50-60_3.json FIT/2/2.0/n3/50_60.json

for i in `find FIT -name "*.json"`; do
sed -i "s/'/\"/g" ${i}
done

