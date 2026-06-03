# ...existing code...
#!/bin/bash
set -e

INCLUDE_PATH=/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include
# INCLUDE_PATH=/Users/yaohsiao/work/HeteroGen/CMurphi/include
# New: optional plain flag
PLAIN=0
MODE_ARG="65536"

usage() {
  echo "Usage: $0 [-p] [-m value] <mfile>"
  echo "  -m    string argument"
  echo "  -p    plain mode (sets PLAIN=1)"
  exit 1
}

# Parse options
while getopts "m:ph" opt; do
  case "$opt" in
    m) MODE_ARG="$OPTARG" ;;
    p) PLAIN=1;;
    h) usage ;;
    *) usage ;;
  esac
done
shift $((OPTIND-1))

MFILE=$1
if [ -z "$MFILE" ] || [ ! -f "$MFILE" ]; then
  echo "empty file"
  exit 0
fi

mkdir -p sandbox_build
cp "$MFILE" sandbox_build/
T=$(basename "$MFILE")
PF=${T%.*}
NM=sandbox_build/${PF}.m
PREFIX=sandbox_build/${PF}
OUT=${PREFIX} && SRC=${PREFIX}.cpp
mu "$NM"
g++ -I${INCLUDE_PATH} "$SRC" -o "$OUT"
# &> /dev/null
# echo "J"
OUTLOG=$(basename $MFILE .m)
# ${PREFIX} -m16384 -p5 -td | tee sandbox_build/$OUTLOG.txt
# ${PREFIX} -m131072 -vdfs -ndl -p5 -tv | tee t.txt
# ${PREFIX} -m131072 -ndl -p5 -tv | tee t2.txt
${PREFIX} -m${MODE_ARG} -ndl -p5 -tv | tee sandbox_build/$OUTLOG.txt
# ${PREFIX} -m262144 -ndl -p5 -tv | tee sandbox_build/$OUTLOG.txt
# ${PREFIX} -m65536 -ndl -p5 -tv | tee sandbox_build/$OUTLOG.txt

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
