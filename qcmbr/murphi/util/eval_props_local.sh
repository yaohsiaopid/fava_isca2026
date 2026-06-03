#!/bin/bash
# all_inputs = {stage: glob_wildcards(f"build/{stage}/out/{{filename}}.m") for stage in STAGES}
# all_outputs = {stage: expand(f"build/{stage}/_build/{{filename}}.txt", filename=all_inputs[stage].filename) for stage in STAGES}
TIMEUTIL=/usr/bin/time
if [ "$(uname -s)" = "Darwin" ]; then
    echo "J"
    TIMEUTIL=gtime
fi
# INCLUDE_PATH=/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include
INCLUDE_PATH=/Users/yaohsiao/work/HeteroGen/CMurphi/include
step_dirname=""
no_overwrite=0
while getopts "s:n" opt; do
  case $opt in
    s) step_dirname="$OPTARG" ;;
    n) no_overwrite=1 ;;
    \?) usage ;;
  esac
done

if [ -z "$step_dirname" ]; then
  echo "Error: Stage name must be provided with -s."
fi
INPUT_DIR="build/${step_dirname}/out"
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory not found: $INPUT_DIR"
    exit 1
fi

echo "-> ${no_overwrite}"
# Enumerate all basenames of .m files (e.g., "prop_1", "prop_2")

TESTS=$(find "$INPUT_DIR" -name "*.m" -exec basename {} .m \;)

OUTPUTDIR="build/${step_dirname}/_build"

TESTS_TO_RUN=""
if [ "$no_overwrite" -eq 1 ]; then
    echo "No-overwrite mode enabled. Checking for completed tests..."
    for t in $TESTS; do
        if [ -f "${OUTPUTDIR}/${t}.txt" ]; then
            echo "Skipping completed test: $t"
        else
            TESTS_TO_RUN="${TESTS_TO_RUN} $t"
        fi
    done
else
    TESTS_TO_RUN=$TESTS
fi

if [ -z "$TESTS_TO_RUN" ]; then
    echo "All tests are already complete. Nothing to do."
    exit 0
fi

if [ ! -d $OUTPUTDIR ]; then
    mkdir -p  $OUTPUTDIR
fi
run_single_test() {
    basename=$1
    output_log="${OUTPUTDIR}/${basename}.txt"
    echo "" > $output_log
    err_log="${OUTPUTDIR}/${basename}.err.log"
    input="build/${step_dirname}/out/${basename}.m"
    mu ${input} &> $err_log
    res="build/${step_dirname}/out/${basename}.cpp"
    if [ -f $res ]; then 
        output_cpp="${OUTPUTDIR}/${basename}.cpp"
        mv ${res} ${output_cpp}
        echo "--> ${output_cpp}"
        output_bin="${OUTPUTDIR}/${basename}"
        # echo "${INCLUDE_PATH}"
        # g++ -Wno-delete-abstract-non-virtual-dtor -Wno-uninitialized -Wno-comment -Wno-dangling-else -Wno-deprecated-declarations -I"${INCLUDE_PATH}" "${output_cpp}" -o "${output_bin}"
        g++ -I"${INCLUDE_PATH}" ${output_cpp} -o ${output_bin} >/dev/null 2>&1
        # g++ -g -I"${INCLUDE_PATH}" ${output_cpp} -o ${output_bin}
        # run 
        # timeout? 
        # $TIMEUTIL -f "Time: %e seconds" "$output_bin" -m8192 -tv >>"$output_log" 2>&1 || true
        timeout 5m $TIMEUTIL -f "Time: %e seconds" "$output_bin" -m8192 -tv >>"$output_log" 2>&1 || true
        # /usr/bin/time -o ${time_log} -f "Time: %e seconds" ${output_bin} -m8192 > ${output_log} || true
        cp $input "${OUTPUTDIR}/${basename}.m"
    else 
        echo "ERROR COMPILE" >> $err_log
    fi 
}

export -f run_single_test
export step_dirname OUTPUTDIR INCLUDE_PATH TIMEUTIL

# --halt now,fail=1 

parallel --jobs 1 --bar run_single_test ::: $TESTS_TO_RUN

#echo "Found tests to process for stage '$step_dirname':"
#echo "$TESTS"
#for t in $TESTS
#do
#    echo "--> $t"
#done 
#echo "---"
#exit 0



