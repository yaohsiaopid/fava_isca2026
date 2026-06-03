#!/bin/bash
set -e 
# /cafe/u/yaohsiao/sandbox/check_suite/rtlcheck/tests/x86tso/amd3.test 
# amd3.tsocc.uarch 
TEST=$1
U=$2
OPT=$3
B=$(basename $TEST)
OUT_SMT=./t.smt2 
echo $OUT_SMT
#amd3.tsocc.constrain.smt2 
/usr/local/bin/pipecheck -i $TEST -m $U -o $OUT_SMT -smt $OPT
python3 smt2_model_nodes.py  $OUT_SMT $OUT_SMT.gv $U | tee r.log
../../util/gg.sh $OUT_SMT.gv 
