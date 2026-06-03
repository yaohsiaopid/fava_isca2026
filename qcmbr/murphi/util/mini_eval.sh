#!/bin/bash

TIMEUTIL=/usr/bin/time
if [ "$(uname -s)" = "Darwin" ]; then
    echo "J"
    TIMEUTIL=gtime
fi

INCLUDE_PATH=/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include
# INCLUDE_PATH=/Users/yaohsiao/work/HeteroGen/CMurphi/include
# New: optional plain flag
PLAIN=0

usage() {
  echo "Usage: $0 <mfile>"
  echo "  -f <basename> -s <stepname> -p    plain mode (sets PLAIN=1)"
  exit 1
}

PROOF=0
TAR="build"
# Parse options
while getopts "nphf:s:d:" opt; do
  case "$opt" in
    n) PROOF=1;;
    p) PLAIN=1;;
    h) usage ;;
    # o) OUTFF="$OPTARG";;
    f) basename="$OPTARG";;
    s) step_dirname="$OPTARG";;
    d) TAR="$OPTARG";;
    *) usage ;;
  esac
done


OUTPUTDIR="${TAR}/${step_dirname}/_build"
if [ ! -d $OUTPUTDIR ]; then
  mkdir -p $OUTPUTDIR
fi
output_log="${OUTPUTDIR}/${basename}.txt"
echo "" > $output_log
err_log="${OUTPUTDIR}/${basename}.err.log"
input="${TAR}/${step_dirname}/out/${basename}.m"
mu ${input} &>> $err_log
res="${TAR}/${step_dirname}/out/${basename}.cpp"
if [ -f $res ]; then 
  output_cpp="${OUTPUTDIR}/${basename}.cpp"
  mv ${res} ${output_cpp}
  output_bin="${OUTPUTDIR}/${basename}"
  g++ -I/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include ${output_cpp} -o ${output_bin}
  # run 
  # timeout? 
  # timeout 15m  /usr/bin/time -f "Time: %e seconds" "$output_bin" -m16384 -tv >>"$output_log" 2>&1 || true

  #( timeout 8m  /usr/bin/time -f "Time: %e seconds" "$output_bin" -m32768 -td ) &>> $output_log 
  # (timeout 5m $TIMEUTIL -f "Time: %e seconds" "$output_bin" -m32768 -tv >>"$output_log" 2>&1) || true 
  # timeout 5m $TIMEUTIL -f "Time: %e seconds" "$output_bin" -m32768 -tv >>"$output_log" 2>&1

  # (( timeout 10m /usr/bin/time -f "Time: %e seconds" "$output_bin" -m32768 -tv ) &>> "$output_log") || true
  # Ensure output_log is an absolute path or correctly relative to where python runs
  # { timeout 10m /usr/bin/time -f "Time: %e seconds" "$output_bin" -m32768 -tv ; } >> "$output_log" 2>&1 || true
  if [ -f ${output_bin} ]; then
     # stdbuf -oL -eL timeout 10m /usr/bin/time -f "Time: %e seconds" "$output_bin" -m32768 -tv  >> "$output_log" 
     while :; do
       if [ "$PROOF" -eq 0 ]; then
         stdbuf -oL -eL timeout 5m /usr/bin/time -f "Time: %e seconds" "$output_bin" -m32768 -tv  >> "$output_log"
       else
        #  stdbuf -oL -eL timeout 3h /usr/bin/time -f "Time: %e seconds" "$output_bin" -m131072 -tv  >> "$output_log"
          stdbuf -oL -eL timeout 5h /usr/bin/time -f "Time: %e seconds" "$output_bin" -m65536  -tv  >> "$output_log"
       fi
       log_size=$(stat -c%s "$output_log" 2>/dev/null || echo 0)
       if [ "$log_size" -gt 1 ]; then
         break
       fi
     done
    # /usr/bin/time -o ${time_log} -f "Time: %e seconds" ${output_bin} -m8192 > ${output_log} || true
  else
    echo "no executable"
  fi
  cp $input "${OUTPUTDIR}/${basename}.m"
  echo "$output_log"
fi 
# echo $OUTFF
# shift $((OPTIND-1))
# 
# # MFILE=$1
# if [ -z "$MFILE" ] || [ ! -f "$MFILE" ]; then
#   echo "empty file"
#   exit 0
# fi
# 
# mkdir -p build
# cp "$MFILE" build/
# T=$(basename "$MFILE")
# PF=${T%.*}
# NM=build/${PF}.m
# PREFIX=build/${PF}
# OUT=${PREFIX} && SRC=${PREFIX}.cpp
# mu "$NM"
# g++ -I${INCLUDE_PATH} "$SRC" -o "$OUT"
# # echo "J"
# 
# if [ -z "$OUTFF" ]; then
# ${PREFIX} -m16384 -p5 -td | tee t.txt
# else 
# ${PREFIX} -m32768 -p5 -td > $OUTFF
# fi

## You can inspect PLAIN if needed:
## echo "PLAIN=$PLAIN"
## ...existing code...
## ...existing code...
##!/bin/bash
#set -e
#
## New: optional plain flag
#PLAIN=false
#
#usage() {
#  echo "Usage: $0 [-p] <mfile>"
#  echo "  -p    plain mode (sets PLAIN=true)"
#  exit 1
#}
#
## Parse options
#while getopts "ph" opt; do
#  case "$opt" in
#    p) PLAIN=true ;;
#    h) usage ;;
#    *) usage ;;
#  esac
#done
#shift $((OPTIND-1))
#
#MFILE=$1
#if [ -z "$MFILE" ] || [ ! -f "$MFILE" ]; then
#  echo "empty file"
#  exit 0
#fi
#
#mkdir -p build
#cp "$MFILE" build/
#T=$(basename "$MFILE")
#PF=${T%.*}
#NM=build/${PF}.m
#python3 preproc.py "$NM"
#PREFIX=build/${PF}
#OUT=${PREFIX} && SRC=${PREFIX}.cpp
#mu "$NM"
#g++ -g -I/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include "$SRC" -o "$OUT"
#echo "J"
#${PREFIX} -m8192 -td | tee t.txt
#
## You can inspect PLAIN if needed:
## echo "PLAIN=$PLAIN"
## ...existing code...
