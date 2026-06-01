#!/usr/bin/bash
# non-interference case
# heuristic only handle undetermined cases line 435
set -e 
set -o pipefail

PWD=$(pwd)
PWD_PREFIX=$(basename ${PWD})
# assumption/opcdoe for the instn
INSTNDIR=opcodes_gen_all
# run over all
INSTN_FILES=$(ls $INSTNDIR)

fnm=""
gui="0"
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -i|--insn)
    fnm="$2"
    shift # past argument
    shift # past value
    ;;
    -g|--gui)
    gui="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done

if [[ -z "$fnm" ]]; then
    echo "Error: -i/--insn option is required"
    exit 1
fi

filename=$(basename $fnm)
fileprefix="${filename%.*}"

INAME="i_${fileprefix}_out" 


INSTN="$INSTNDIR/$fnm"
echo "=========== INSTN ============="
echo "- Directory: $INAME"
echo "- Instruction file: $INSTN"
cat $INSTN
echo "==============================="



# Shared by all instructions 
if [ ! -f "xGenPerfLocDfg/dfg_e.txt" ]; then
    exit
fi 
echo "========== DFG E prepared ========== "


FV_UNITDIR=$(realpath ../../..)


########## 
## STEP 2
########## 
cd $INAME
INAME_DIR=$(realpath .)

echo "
================================================================================
STEP 2 at $(pwd) $(date)
================================================================================
"

DIR=xCoverCandidateHBEdges
PYSCRPT=xCoverCandidateHBEdges
confirmed="y"
if [ -d "${DIR}" ]; then
    echo "Directory exists $INAME/$DIR. Redo step? [y/n]"
    read confirmed
fi
if [ $confirmed == "y" ]; then
    JOB="rtl2mupath_candidate_HB"

    SVFILE=$(realpath ${DIR})/${JOB}.sv
    TCLFILE=$(realpath ${DIR})/${JOB}.tcl

    # Generate SV and TCL for HB properties
    cp -r ../${DIR} .
    cd ${DIR}; python3 ${PYSCRPT}.py gen; cd ..

    # Run Jasper to get HB property results
    cd ../..
    ./RUN_JG.sh -j ${INAME_DIR}/${DIR} -s ${SVFILE} -t ${TCLFILE} -g ${gui} 
fi


# Post process HB property results
cd ${INAME_DIR}/${DIR};
python3 ${PYSCRPT}.py pp; 
#python3 ${PYSCRPT}.py stats; 
cd ../
