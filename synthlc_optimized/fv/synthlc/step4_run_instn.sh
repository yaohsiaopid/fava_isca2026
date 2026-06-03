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
## STEP 4
########## 
cd $INAME
INAME_DIR=$(realpath .)

echo "
================================================================================
STEP 4 at $(pwd) $(date)
================================================================================
"

DIR=xIftIntrinsic
#PYSCRPT=xRunSpv
PYSCRPT=xRunIFT
confirmed="y"
if [ -d "${DIR}" ]; then
    echo "Directory exists $INAME/$DIR. Redo step? [y/n]"
    read confirmed
fi
if [ $confirmed == "y" ]; then
    #JOB="spv_rtl2mupath_taint_rs1"
    JOB="ift_intr_rtl2mupath_taint_both_rs1_rs2"
    JOB1="ift_intr_rtl2mupath_taint_rs1"
    JOB2="ift_intr_rtl2mupath_taint_rs2"

    SVFILE=$(realpath ${DIR})/${JOB}.sv
    TCLFILE=$(realpath ${DIR})/${JOB}.tcl

    SVFILE1=$(realpath ${DIR})/${JOB1}.sv
    TCLFILE1=$(realpath ${DIR})/${JOB1}.tcl

    SVFILE2=$(realpath ${DIR})/${JOB2}.sv
    TCLFILE2=$(realpath ${DIR})/${JOB2}.tcl


    # Taint both operands
    cp -r ../${DIR} .
    cd ${DIR}; python3 ${PYSCRPT}.py gen ${fileprefix} taint_both_rs1_rs2; cd ../../..    
    if [[ -f "$SVFILE" ]]; then
        ./RUN_JG_ift.sh -j ${INAME_DIR}/${DIR} -t ${TCLFILE} -s ${SVFILE} -h src_ift/hdl.f -f src_ift/cellift_top_rewrite.sv -p src_ift/common_header.sv -g ${gui}
    fi

    # Taint RS1 only
    cd ${INAME_DIR}/${DIR}; python3 ${PYSCRPT}.py gen_per_field ${fileprefix} taint_rs1; cd ../../..
    if [[ -f "$SVFILE1" ]]; then
        ./RUN_JG_ift.sh -j ${INAME_DIR}/${DIR} -t ${TCLFILE1} -s ${SVFILE1} -h src_ift/hdl.f -f src_ift/cellift_top_rewrite.sv -p src_ift/common_header.sv -g ${gui}
    fi

    # Taint RS2 only
    cd ${INAME_DIR}/${DIR}; python3 ${PYSCRPT}.py gen_per_field ${fileprefix} taint_rs2; cd ../../..
    if [[ -f "$SVFILE2" ]]; then
        ./RUN_JG_ift.sh -j ${INAME_DIR}/${DIR} -t ${TCLFILE2} -s ${SVFILE2} -h src_ift/hdl.f -f src_ift/cellift_top_rewrite.sv -p src_ift/common_header.sv -g ${gui}
    fi
fi

# Post process HB property results
cd ${INAME_DIR}/${DIR};
python3 ${PYSCRPT}.py pp; 
#python3 ${PYSCRPT}.py stats; 
cd ../
