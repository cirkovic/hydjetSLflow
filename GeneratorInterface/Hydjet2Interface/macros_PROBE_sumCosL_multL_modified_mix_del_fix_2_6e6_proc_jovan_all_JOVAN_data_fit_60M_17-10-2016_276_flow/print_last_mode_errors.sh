echo "*********"
for i in `ls 2/*/*/*/data_n2/errors/mode1_error.dat`; do echo $i; tail -1 $i; echo; done
echo "*********"
for i in `ls 2/*/*/*/data_n2/errors/mode2_error.dat`; do echo $i; tail -1 $i; echo; done
echo "*********"
for i in `ls 2/*/*/*/data_n3/errors/mode1_error.dat`; do echo $i; tail -1 $i; echo; done
echo "*********"
for i in `ls 2/*/*/*/data_n3/errors/mode2_error.dat`; do echo $i; tail -1 $i; echo; done
echo "*********"

