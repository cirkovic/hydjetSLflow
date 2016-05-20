sh job_new.sh test Nevt=80 s=2 c=0-10 deltaEtaCut=2.0 &
sh job_new.sh test Nevt=120 s=2 c=0-02 deltaEtaCut=1.0 &
sh job_new.sh test Nevt=40 s=2 c=0-10 deltaEtaCut=1.0 &

top -b -d 1 -M -u cirkovic 2>&1 | tee top_prompt.txt
grep "Mem:" top_prompt.txt
