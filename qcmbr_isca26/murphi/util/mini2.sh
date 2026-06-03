# ...existing code...
#!/bin/bash
set -e

# New: optional plain flag
PLAIN=0

usage() {
  echo "Usage: $0 <mfile>"
  echo "  -p    plain mode (sets PLAIN=1)"
  exit 1
}

mem=131072
# Parse options
while getopts "phm:" opt; do
  case "$opt" in
    p) PLAIN=1;;
    h) usage ;;
    m) mem="$OPTARG";;
    *) usage ;;
  esac
done
shift $((OPTIND-1))

MFILE=$1
if [ -z "$MFILE" ] || [ ! -f "$MFILE" ]; then
  echo "$MFILE"
  echo "empty file"
  exit 0
fi

mkdir -p build
cp "$MFILE" build/
T=$(basename "$MFILE")
PF=${T%.*}
NM=build/${PF}.m
PREFIX=build/${PF}
OUT=${PREFIX} && SRC=${PREFIX}.cpp
mu "$NM"
g++ -g -I/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include "$SRC" -o "$OUT"
echo "J"
# ${PREFIX} -m131072 -pn -td | tee t.txt
BNM=$(basename $MFILE)
BNM=${BNM%.*}
# ${PREFIX} -m48000 -p5 -tv | tee ${BNM}.txt
# ${PREFIX} -m65536 -p5 -tv | tee ${BNM}.txt
${PREFIX} -m${mem} -p5 -tv | tee t.txt

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
