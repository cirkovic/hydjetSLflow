rm *.root

Nevt=5000
#N=$((10000000+Nevt*2000))
s=0
c=( 0-02 0-5 0-10 10-20 20-30 30-40 40-50 50-60 )
deltaEtaCut=2.0
#first=( crab_20160521_223007 crab_20160521_223020 crab_20160521_223029 crab_20160521_223036 crab_20160521_223043 crab_20160521_223054 crab_20160521_223103 crab_20160521_223120 )
#second=( crab_20160521_232259 crab_20160521_232314 crab_20160521_232322 crab_20160521_232328 crab_20160521_232338 crab_20160521_232347 crab_20160521_232404 crab_20160521_232412 )
#first=( crab_20160523_205234 crab_20160523_205248 crab_20160523_205255 crab_20160523_205334 crab_20160523_205344 crab_20160523_205351 crab_20160523_205359 crab_20160523_205408 )
#second=( crab_20160523_121253 crab_20160523_121310 crab_20160523_121321 crab_20160523_121329 crab_20160523_121338 crab_20160523_121347 crab_20160523_121402 crab_20160523_121411 )
#first=( crab_20160524_075428 crab_20160524_075441 crab_20160524_075449 crab_20160524_075457 crab_20160524_075505 crab_20160524_075514 crab_20160524_075523 crab_20160524_075532 )
first=( crab_20160527_122326 crab_20160527_122401 crab_20160527_122416 crab_20160527_122427 crab_20160527_122439 crab_20160527_122448 crab_20160527_122458 crab_20160527_122509 )
first=( crab_20160528_071402 crab_20160528_071420 crab_20160528_071429 crab_20160528_071440 crab_20160528_071448 crab_20160528_071456 crab_20160528_071510 crab_20160528_071518 )


for i in `seq 0 7`;
do
    #hadd -k -f output_${N}_${s}_${c[$i]}_${deltaEtaCut}.root `ls /tmp/cirkovic/${first[$i]}/results/output_${Nevt}_${s}_${c[$i]}_${deltaEtaCut}_*.root /tmp/cirkovic/${second[$i]}/results/output_${Nevt}_${s}_${c[$i]}_${deltaEtaCut}_*.root` &
    #bsub -q 8nm hadd -k -f output_${N}_${s}_${c[$i]}_${deltaEtaCut}.root `ls /tmp/cirkovic/${first[$i]}/results/output_${Nevt}_${s}_${c[$i]}_${deltaEtaCut}_*.root /tmp/cirkovic/${second[$i]}/results/output_${Nevt}_${s}_${c[$i]}_${deltaEtaCut}_*.root`
    #hadd -k -f output_$((2*N))_${s}_${c[$i]}_${deltaEtaCut}.root `ls /tmp/cirkovic/${first[$i]}/results/output_${Nevt}_${s}_${c[$i]}_${deltaEtaCut}_*.root /tmp/cirkovic/${second[$i]}/results/output_${Nevt}_${s}_${c[$i]}_${deltaEtaCut}_*.root` output_6M/output_${N}_${s}_${c[$i]}_${deltaEtaCut}.root &
    hadd -k -f output_all_${s}_${c[$i]}_${deltaEtaCut}.root `ls /tmp/cirkovic/${first[$i]}/results/output_${Nevt}_${s}_${c[$i]}_${deltaEtaCut}_*.root` &
done

