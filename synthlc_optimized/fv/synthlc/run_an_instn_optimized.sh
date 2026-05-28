#!/usr/bin/bash
if [ -z $1 ];
then
    echo "Pass an argument such as as \`./run_an_instn_demo.sh LW.sv\`"
    exit
else
    echo "===> Processing: $1"
    fnm="$1"
fi

./step1_run_instn.sh $fnm
./step2_run_instn.sh $fnm
./step3_run_instn.sh $fnm
./step4_run_instn.sh $fnm
./step5_run_instn.sh $fnm
