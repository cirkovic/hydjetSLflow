Nevt=$1
s=$2
c=$3
deltaEtaCut=$4

echo $Nevt $s $c $deltaEtaCut

IFS='=' read -ra ARG <<< "$1"
Nevt="${ARG[1]}"

IFS='=' read -ra ARG <<< "$2"
s="${ARG[1]}"

IFS='=' read -ra ARG <<< "$3"
c="${ARG[1]}"

IFS='=' read -ra ARG <<< "$4"
deltaEtaCut="${ARG[1]}"

echo $Nevt $s $c $deltaEtaCut
