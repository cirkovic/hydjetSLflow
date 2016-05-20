cp ../OUTPUT_22-04-2016/output_2_250_*_all.root .
for i in 0-5 0-10 10-20 20-30 30-40 40-50 50-60;
do
    mv output_2_250_${i}_all.root output_2_o250_${i}_all.root
done

