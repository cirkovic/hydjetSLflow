rm prompt.txt

echo "*********"                                                                           >> prompt.txt
for i in `ls 2_np/*/*/*/data_n2/modes/mode1.dat`; do echo $i; tail -1 $i; echo; done       >> prompt.txt
echo "*********"                                                                           >> prompt.txt
for i in `ls 2_np/*/*/*/data_n2/modes/mode2.dat`; do echo $i; tail -1 $i; echo; done       >> prompt.txt
echo "*********"                                                                           >> prompt.txt
for i in `ls 2_np/*/*/*/data_n3/modes/mode1.dat`; do echo $i; tail -1 $i; echo; done       >> prompt.txt
echo "*********"                                                                           >> prompt.txt
for i in `ls 2_np/*/*/*/data_n3/modes/mode2.dat`; do echo $i; tail -1 $i; echo; done       >> prompt.txt
echo "*********"                                                                           >> prompt.txt

echo "*********"                                                                           >> prompt.txt
for i in `ls 2/*/*/*/data_n2/errors/mode1_error.dat`; do echo $i; tail -1 $i; echo; done   >> prompt.txt
echo "*********"                                                                           >> prompt.txt
for i in `ls 2/*/*/*/data_n2/errors/mode2_error.dat`; do echo $i; tail -1 $i; echo; done   >> prompt.txt
echo "*********"                                                                           >> prompt.txt
for i in `ls 2/*/*/*/data_n3/errors/mode1_error.dat`; do echo $i; tail -1 $i; echo; done   >> prompt.txt
echo "*********"                                                                           >> prompt.txt
for i in `ls 2/*/*/*/data_n3/errors/mode2_error.dat`; do echo $i; tail -1 $i; echo; done   >> prompt.txt
echo "*********"                                                                           >> prompt.txt

#sed -i 's/.dat\n/.dat\ /g' prompt.txt
sed ':a;N;$!ba;s/.dat\n/.dat /g' prompt.txt > prompt1.txt
mv prompt1.txt prompt.txt


