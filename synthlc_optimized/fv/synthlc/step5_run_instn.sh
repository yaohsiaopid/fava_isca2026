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

cp $INSTNDIR/$fnm "${INAME}/idef.sv"


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
## STEP 5
########## 
cd $INAME
INAME_DIR=$(realpath .)

echo "
================================================================================
STEP 5 at $(pwd) $(date)
================================================================================
"

DIR=xIftDynamic
PYSCRPT=xRunIFT
confirmed="y"
if [ -d "${DIR}" ]; then
    echo "Directory exists $INAME/$DIR. Redo step? [y/n]"
    read confirmed
fi
if [ $confirmed == "y" ]; then
    
    # Taint both operands
    JOB="ift_dyn_rtl2mupath_taint_both_rs1_rs2"
    TCLFILE=${INAME_DIR}/${DIR}/${JOB}.tcl

    # Generate SV and TCL for HB properties
    cp -r ../${DIR} .
    cd ${DIR}; python3 ${PYSCRPT}.py gen ${fileprefix} taint_both_rs1_rs2; cd ../../..

    # Loop over every .sv file found in the directory and run Jasper
    for SVFILE in $(realpath ${INAME_DIR}/${DIR})/${JOB}*.sv; do

        echo "=== Running job: ${JOB} ==="
        echo "    SV file:  ${SVFILE}"
        echo "    TCL file: ${TCLFILE}"

        ./RUN_JG_ift.sh -j ${INAME_DIR}/${DIR} -t ${TCLFILE} -s ${SVFILE} \
            -h src_ift/hdl.f -f src_ift/cellift_top_rewrite.sv \
            -p src_ift/common_header.sv -g ${gui}
    done


    # Taint RS1 only
    JOB="ift_dyn_rtl2mupath_taint_rs1"
    #TCLFILE=${INAME_DIR}/${DIR}/${JOB}.tcl

    # Generate SV and TCL for HB properties
    cd ${INAME_DIR}/${DIR}; python3 ${PYSCRPT}.py gen_per_field ${fileprefix} taint_rs1; cd ../../..

    # Loop over every .sv file found in the directory and run Jasper
    for SVFILE in $(realpath ${INAME_DIR}/${DIR})/${JOB}*.sv; do
        TCLFILE="${SVFILE%.sv}.tcl"

        echo "=== Running job: ${JOB} ==="
        echo "    SV file:  ${SVFILE}"
        echo "    TCL file: ${TCLFILE}"

        ./RUN_JG_ift.sh -j ${INAME_DIR}/${DIR} -t ${TCLFILE} -s ${SVFILE} \
            -h src_ift/hdl.f -f src_ift/cellift_top_rewrite.sv \
            -p src_ift/common_header.sv -g ${gui}
    done


    # Taint RS2 only
    JOB="ift_dyn_rtl2mupath_taint_rs2"
    #TCLFILE=${INAME_DIR}/${DIR}/${JOB}.tcl

    # Generate SV and TCL for HB properties
    cd ${INAME_DIR}/${DIR}; python3 ${PYSCRPT}.py gen_per_field ${fileprefix} taint_rs2; cd ../../..
    
    # Loop over every .sv file found in the directory and run Jasper
    for SVFILE in $(realpath ${INAME_DIR}/${DIR})/${JOB}*.sv; do
        TCLFILE="${SVFILE%.sv}.tcl"

        echo "=== Running job: ${JOB} ==="
        echo "    SV file:  ${SVFILE}"
        echo "    TCL file: ${TCLFILE}"

        ./RUN_JG_ift.sh -j ${INAME_DIR}/${DIR} -t ${TCLFILE} -s ${SVFILE} \
            -h src_ift/hdl.f -f src_ift/cellift_top_rewrite.sv \
            -p src_ift/common_header.sv -g ${gui}
    done
fi


# Post process HB property results
cd ${INAME_DIR}/${DIR};
python3 ${PYSCRPT}.py pp; 
cd ../
